#!/usr/bin/env Rscript

# util.R
# 2022-01-20

if (!require("pacman", quietly = TRUE)) install.packages("pacman")
pacman::p_load("data.table", "DBI", "RSQLite", "tibble")

read_db <- function(filepath, tables = NULL, to_tibble = TRUE) {
  if (!file.exists(filepath))
    stop("'", filepath, "' does not exist.")
  dfs <- tryCatch({
    conn <- dbConnect(SQLite(), filepath)
    if (is.null(tables))
      tables <- dbListTables(conn)
    if (is.null(names(tables)))
      tables <- setNames(tables, tables)
    lapply(tables, dbReadTable, conn = conn)
  }, error = \(e) {
    stop("Problem reading database.\nOriginal error message:\n", e)
  }, finally = {
    dbDisconnect(conn)
  })
  if (to_tibble && "tibble" %in% loadedNamespaces())
    dfs <- lapply(dfs, as_tibble)
  dfs
}

write_db <- function(dfs, filepath, overwrite = FALSE, append = FALSE) {
  if (is.null(names(dfs)))
    stop("Tables must have names.")
  tryCatch({
    conn <- dbConnect(SQLite(), filepath)
    Map(function(name, df) {
      dbWriteTable(conn, name, df, overwrite = overwrite, append = append)
    }, names(dfs), dfs)
    message("'", filepath, "' successfully written.")
  }, error = \(e) {
    message("Problem writing database.\nOriginal error message:\n", e)
  }, finally = {
    dbDisconnect(conn)
  })
}

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


