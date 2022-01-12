#!/usr/bin/env Rscript

# util.R
# 2022-01-12

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
    message("Problem reading database.\nOriginal error message:\n", e)
  }, finally = {
    dbDisconnect(conn)
  })
  if (is.null(dfs))
    return(NULL)
  if (to_tibble && "tibble" %in% loadedNamespaces())
    dfs <- lapply(dfs, as_tibble)
  dfs
}

write_db <- function(dfs, filepath, overwrite = FALSE, append = FALSE) {
  if (is.null(names(dfs)))
    stop("Tables must have names.")
  conn <- dbConnect(SQLite(), filepath)
  Map(function(name, df) {
    dbWriteTable(conn, name, df, overwrite = overwrite, append = append)
  }, names(dfs), dfs)
  dbDisconnect(conn)
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


