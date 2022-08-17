#!/usr/bin/env Rscript
#
# util.R
# 2022-08-17

if (!require("pacman", quietly = TRUE)) install.packages("pacman")

pacman::p_load(
  "data.table",
  "DBI",
  "readxl",
  "RSQLite",
  "tibble"
)

# util -------------------------------------------------------------------------

util <- {list(
  as_xlsx_date = function(x) {
    as.Date(as.numeric(x), origin = "1899-12-30")
  },
  
  check_is_named_list = function(x) {
    if (!is(x, "list")) {
      stop("Input must be a list.")
    } else if (is.null(names(x))) {
      stop("Input must be named.")
    }
  },
  
  check_file_md5 = function(filepath, ref_md5, force = FALSE) {
    file_md5 <- tools::md5sum(filepath)
    if (file_md5 != ref_md5) {
      msg <- paste0(
        "\x1b[91mMD5 mismatch\x1b[0m:",
        "\nfilepath = \x1b[95m", filepath, "\x1b[0m",
        "\nwant = \x1b[92m", ref_md5, "\x1b[0m",
        "\ngot = \x1b[93m", file_md5, "\x1b[0m"
      )
      if (force) warning(msg)
      else stop(msg)
    }
  },
  
  #' Combine data frames that have aligned columns.
  combine_dfs_simple = function(..., ref_idx = 1) {
    datafs <- list(...)
    ref_colnames <- colnames(datafs[[ref_idx]])
    for (i in seq_along(datafs)) {
      colnames(datafs[[i]]) <- ref_colnames
    }
    do.call("rbind", datafs)
  },
  
  #' Combine data frames that have common columns.
  combine_dfs_inner = function(...) {
    datafs <- list(...)
    common_colnames <- Reduce(intersect, lapply(datafs, colnames))
    for (i in seq_along(datafs)) {
      datafs[[i]] <- datafs[[i]][, common_colnames]
    }
    do.call("rbind", datafs)
  },
  
  #' Tabulate values for each column in a data frame.
  count_values = function(dataf, threshold = 20) {
    res <- lapply(dataf, table, useNA = "always")
    mask <- lengths(res) > threshold
    res[mask] <- lapply(res[mask], \(x) {
      l <- list()
      l[["n_categories"]] <- length(x)
      l[[sprintf("first %d", threshold)]] <- x[1:threshold]
      l
    })
    res
  },
  
  #' Convert all date/datetime columns in a data frame to strings.
  datetimes_to_text = function(dataf) {
    for (i in seq_along(dataf)) {
      if (is(dataf[[i]], "POSIXct")) {
        dataf[[i]] <- ifelse(
          dataf[[i]] >= as.POSIXct("1900-01-01", tz = "UTC"),
          strftime(dataf[[i]], "%Y-%m-%d", tz = "UTC"),
          strftime(dataf[[i]], "%H:%M", tz = "UTC")
        )
      }
    }
    dataf
  },
  
  #' Drop duplicated records from data frame.
  dedup = function(dataf, idx_col = "subjid") {
    dataf[!duplicated(dataf[[idx_col]]), ]
  },
  
  #' Drop columns with too many missing values.
  drop_empty_columns = function(dataf, threshold = NULL) {
    if (is.null(threshold) || is.na(threshold) || threshold > nrow(dataf)) {
      threshold <- nrow(dataf)
    }
    is_empty_column <- apply(is.na(dataf), 2, \(x) sum(x) >= threshold)
    dataf[, !is_empty_column]
  },
  
  #' Calculate proportion of missing values in each column.
  empty_frac = function(dataf, threshold = 0) {
    res <- vapply(dataf, \(x) mean(is.na(x)), FUN.VALUE = numeric(1))
    res[res > threshold]
  },
  
  #' Calculate proportion of missing values in each column for each data frame.
  empty_fracs = function(dfs, threshold = 0) {
    res <- lapply(dfs, util$empty_frac, threshold = threshold)
    res[lengths(res) > 0]
  },
  
  get_colnames = function(dfs, keys, exclude = "subjid") {
    setdiff(unlist(lapply(dfs[keys], names)), exclude)
  },
  
  #' Extract relevant rows from data dictionary.
  get_dd = function(dataf, dd, column = "Variable") {
    dd[dd[[column]] %in% colnames(dataf), ]
  },
  
  left_join = function(dataf1, dataf2, by = "subjid") {
    dataf <- merge(dataf1, dataf2, by = by, all.x = TRUE)
    if ("tibble" %in% loadedNamespaces()) dataf <- as_tibble(dataf)
    dataf
  },
  
  #' Read all tables in database, separate data dictionary if identified.
  load_from_sqlite = function(filepath, datadict_name = "DataDict") {
    dfs <- util$read_db(filepath)
    dd <- NULL
    if (!is.null(datadict_name)) {
      dd <- dfs[[datadict_name]]
      dfs <- dfs[names(dfs) != datadict_name]
    }
    list("dfs" = dfs, "dd" = dd)
  },
  
  outer_join = function(dataf1, dataf2, by = "subjid") {
    dataf <- merge(dataf1, dataf2, by = by, all = TRUE)
    if ("tibble" %in% loadedNamespaces()) dataf <- as_tibble(dataf)
    dataf
  },
  
  #' Read from SQLite database.
  read_db = function(filepath, tables = NULL, to_tibble = TRUE) {
    if (!file.exists(filepath)) stop(filepath, " does not exist.")
    dfs <- tryCatch({
      con <- dbConnect(SQLite(), filepath)
      if (is.null(tables)) tables <- dbListTables(con)
      if (is.null(names(tables))) names(tables) <- tables
      lapply(tables, \(table) dbReadTable(con, table))
    }, finally = dbDisconnect(con))
    if (to_tibble && "tibble" %in% loadedNamespaces())
      dfs <- lapply(dfs, as_tibble)
    dfs
  },
  
  #' Automatically recode columns with valid REDCap options strings in the 
  #' given data dictionary. Attempt to convert to numeric type if possible. 
  #' Set `labels_to_values = FALSE` for reverse recoding.
  redcap_df_auto_recode = function(
    dataf,
    dd,
    mcq_pattern = "^[0-9].*,",
    dd_idx = "Variable",
    dd_options = "Options",
    labels_to_values = TRUE
  ) {
    #' Cannot use `\\|` as the pattern for questions with only 1 option.
    #' `^[0-9].*,` might have issues if values do not start with a number.
    is_mcq <- grepl(mcq_pattern, dd[[dd_options]])
    lookups <- structure(
      lapply(
        dd[[dd_options]][is_mcq],
        redcap_options_to_vector,
        labels_to_values = labels_to_values
      )
      , names = dd[[dd_idx]][is_mcq]
    )
    if(!all(names(lookups) %in% colnames(dataf))) stop(
      "ERROR: Mismatch between names:"
      , "\n  Lookup names: ", toString(names(lookups))
      , "\n  Column names: ", toString(colnames(dataf))
    )
    for (k in names(lookups)) {
      dataf[[k]] <- util$replace_map(dataf[[k]], lookups[[k]])
      tryCatch(
        dataf[[k]] <- as.numeric(dataf[[k]])
        , warning = \(w) dataf[[k]]
      )
    }
    dataf
  },
  
  #' Automatically recode columns with only `Yes` or `No` (or `NA`) values 
  #' to `1` and `0`, respectively. Similarly for columns with only `Checked` 
  #' or `Unchecked` (or `NA`) values. This should be done _after_ passing 
  #' through the data dictionary first, since some question might code `Yes` 
  #' and `No` with non-standard values.
  redcap_df_auto_recode_yncu = function(dataf) {
    lookups <- list(
      "yn" = c("Yes" = 1, "No" = 0),
      "cu" = c("Checked" = 1, "Unchecked" = 0)
    )
    for (k in names(dataf)) {
      x <- dataf[[k]]
      for (lookup in lookups) {
        if (all(x[!is.na(x)] %in% names(lookup))) {
          dataf[[k]] <- as.numeric(util$replace_map(x, lookup))
          break
        }
      }
    }
    dataf
  },
  
  #' Convert REDCap options string into a named vector for recoding purposes. 
  #' Set `labels_to_values = FALSE` for reverse recoding.
  redcap_options_to_vector = function(s, labels_to_values = TRUE) {
    #' Option choices are split by " | ".
    choices <- unlist(strsplit(s, " \\| "))
    #' Assume labels-to-values first, since it's possible to not have labels.
    sub_exprs <- sub("(.+?),\\s*(.*)", "`\\2` = '\\1'", choices)
    #' If there are no labels, copy the values as labels.
    sub_exprs <- sub("`` = '(.+)'", "`\\1` = '\\1'", sub_exprs)
    #' Convert double quotes `"` to single quotes `'`.
    sub_exprs <- gsub('"', "'", sub_exprs)
    #' Swap positions if doing values-to-labels.
    if (!labels_to_values)
      sub_exprs <- sub("`(.*)` = '(.+)'", "`\\2` = '\\1'", sub_exprs)
    #' Create string expression of named vector and try to parse it.
    expr_str <- paste(sub_exprs, collapse = ", ")
    expr_str <- sprintf("c(%s)", expr_str)
    tryCatch(
      eval(parse(text = expr_str))
      , error = \(e) stop(e, "\n", s, "\n", expr_str)
    )
  },
  
  #' Read XLSX file containing data exported from REDCap. Each file is expected 
  #' to have 2 sheets: `Data` and `DataDict`.
  redcap_read_xlsxs = function(
    dir_path,
    include_pattern = "^[^~$].*xlsx$",
    exclude_pattern = NULL,
    key_pattern = NULL,
    space_to_underscore = TRUE,
    show_list_only = FALSE
  ) {
    dp <- dir_path
    ip <- include_pattern
    ep <- exclude_pattern
    file_paths <- list.files(dp, ip, full.names = TRUE, recursive = TRUE)
    if (!is.null(ep)) file_paths <- file_paths[!grepl(ep, file_paths)]
    
    keys <- file_paths
    if (!is.null(key_pattern)) keys <- sub(key_pattern, "\\1", keys)
    if (space_to_underscore) keys <- gsub("\\s", "_", keys)
    names(file_paths) <- keys
    
    if (show_list_only) return(file_paths)
    
    dfs <- lapply(file_paths, readxl::read_xlsx, sheet = "Data")
    dds <- lapply(file_paths, readxl::read_xlsx, sheet = "DataDict")
    
    list("dfs" = dfs, "dds" = dds)
  },
  
  #' Replace using named vector to map old values to new values.
  replace_map = function(x, mapping) {
    mask <- x %in% names(mapping)
    x[mask] <- mapping[x[mask]]
    x
  },
  
  #' Save a figure.
  save_fig = function(fig, filepath, width = 1760, height = 990) {
    png(filepath, width = width, height = height)
    print(fig)
    dev.off()
  },
  
  #' Save a list of figures.
  save_figs = function(figs, dirpath, prefix, width = 1760, height = 990) {
    util$check_is_named_list(figs)
    if (!dir.exists(dirpath)) dir.create(dirpath, recursive = TRUE)
    for (name in names(figs)) {
      filename <- sprintf("%s_%s.png", prefix, name)
      filepath <- file.path(dirpath, filename)
      png(filepath, width = width, height = height)
      print(figs[[name]])
      dev.off()
    }
  },
  
  #' Split data frame into train and test sets.
  train_test_split = function(dataf, test_size = 0.1, random_state = 1729) {
    n <- nrow(dataf)
    set.seed(random_state)
    is_test <- seq_len(n) %in% sample.int(n, n * test_size)
    list("train" = dataf[!is_test, ], "test" = dataf[is_test, ])
  },
  
  #' Write data frames to SQLite database.
  write_db = function(dfs, filepath, overwrite = FALSE) {
    util$check_is_named_list(dfs)
    if (file.exists(filepath) && !overwrite) stop(filepath, " already exists.")
    if (file.exists(filepath)) file.remove(filepath)
    message("Writing file: ", filepath)
    con <- dbConnect(SQLite(), filepath)
    for (name in names(dfs)) {
      dbWriteTable(con, name, dfs[[name]])
    }
    dbDisconnect(con)
    message("MD5: ", tools::md5sum(filepath))
  }
)}



db_to_csvs <- function(filepath, output = NULL, verbose = TRUE) {
  dfs <- read_db(filepath)
  
  if ("data.table" %in% loadedNamespaces())
    writer <- fwrite
  else if ("readr" %in% loadedNamespaces())
    writer <- write_csv
  else
    writer <- write.csv
  
  dirpath <- output
  if (is.null(dirpath) || !dir.exists(dirpath))
    dirpath <- paste0(tools::file_path_sans_ext(filepath), "_csvs")
  if (!dir.exists(dirpath))
    dir.create(dirpath)
  
  for (name in names(dfs)) {
    filename <- paste0(name, ".csv")
    filepath <- file.path(dirpath, filename)
    writer(dfs[[name]], filepath, na = "")
    if (verbose)
      message("File written: ", filepath)
  }
}

replace_map <- function(x, mapping, canonicalize = FALSE) {
  if (canonicalize)
    x <- tolower(trimws(x))
  mask <- x %in% names(mapping)
  x[mask] <- mapping[x[mask]]
  x
}

#' Generate Step Function Expression
#'
#' Given corresponding numeric vectors of input and output values, create a 
#' string representation of the step function (sum of indicator variables, 
#' possibly multiplied by varying step heights). The expression will be 
#' optimized by factoring step height.
#' 
#' @param x a numeric vector of input values.
#' @param y a numeric vector of the corresponding output values.
#' @param var_name character string for the variable name.
#' @param strict if `TRUE`, stop if `x` is not sorted.
#' @param warn if `TRUE`, print a warning if `x` is auto-sorted.
#'
#' @return string containing the step function expression/equation/formula.
#'
#' @examples
#' x <- c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
#' y <- c(50, 51, 55, 60, 67, 75, 82, 89, 96, 103, 110, 117, 123, 130, 136, 142)
#' step_fn_expr(x, y)
step_fn_expr <- function(x, y, var_name = "x", strict = FALSE, warn = TRUE) {
  if (length(x) != length(y))
    stop("Vectors must be the same length.",
         "\n- length(x) = ", length(x),
         "\n- length(y) = ", length(y))
  if (!(is.numeric(x) && is.numeric(y)))
    stop("Vectors must be numeric.",
         "\n- is.numeric(x) = ", is.numeric(x),
         "\n- is.numeric(y) = ", is.numeric(y))
  
  order_x <- order(x)
  if (any(order_x != seq_along(x))) {
    if (strict)
      stop("Vectors must be sorted (ascending `x`, with corresponding `y`).",
           "\n- x = ", toString(x),
           "\n- y = ", toString(y),
           "\n  Set `strict = FALSE` to do so automatically.")
    if (warn)
      warning("Vectors will be auto-sorted (ascending `x`).\n",
              "\n- old x = ", toString(x),
              "\n- old y = ", toString(y), "\n",
              "\n- new x = ", toString(x[order_x]),
              "\n- new y = ", toString(y[order_x]), "\n")
    x <- x[order_x]
    y <- y[order_x]
  }
  
  # Calculate the step heights (differences between consecutive `y` values). 
  # Assume start point of 0 to find the first step height.
  step_heights <- diff(c(0, y))
  
  # Group `x` values by their associated step heights. Remove the group 
  # associated with a step height of 0 (we don't need those terms). The groups 
  # will naturally be ordered according to ascending step height, so re-order 
  # them based on the first value of each group.
  x_groups <- split(x, step_heights)
  x_groups <- x_groups[names(x_groups) != "0"]
  ord <- order(unlist(lapply(x_groups, \(x) x[1])))
  x_groups <- x_groups[ord]
  
  # Create indicators
  inds <- lapply(x_groups, \(x) sprintf("(%s >= %s)", var_name, x))
  
  # Groups of more than 1 indicator need to be added together, with parentheses
  to_sum <- lengths(inds) > 1
  inds[to_sum] <- inds[to_sum] |>
    lapply(\(x) sprintf("(%s)", paste(x, collapse = " + ")))
  
  # Multiply each group by their respective step sizes (unless it's 1)
  step1 <- names(inds) == "1"
  inds[!step1] <- inds[!step1] |>
    paste("*", names(x_groups)[!step1])
  
  # Sum all groups together
  paste(inds, collapse = " + ")
}


