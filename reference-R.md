# Useful Functions in R

## Commonly used

### `pacman::`

```r
if (!require("pacman", quietly = TRUE)) install.packages("pacman")
pacman::p_load(...)
```

### Replace using named vector

```r
replace_map <- function(x, mapping, canonicalize = FALSE) {
  #' Replace using named vector to map old values to new values
  #' 
  #' @description Replace values in a vector using a named vector to map old 
  #' values to new values. Values not specified will be left unchanged.
  #' 
  #' @param x character. The vector with values to replace
  #' @param mapping character. The named vector that maps old values to new 
  #' values, old values are set as the names
  #' @param standardize logical. Trim whitespace and lowercase all values 
  #' Defaults to FALSE
  #' 
  #' @usage replace_map(x, mapping, standardize = FALSE)
  #' 
  #' @return The vector with replaced values.
  #' 
  #' @examples
  #' replace_map(c("a1", "a2", "a3"), c(`a1` = "b1", `a2` = "b2"))
  
  if (canonicalize) x <- tolower(trimws(x))
  mask <- x %in% names(mapping)
  x[mask] <- mapping[x[mask]]
  x
}
```

### SQLite

```r
pacman::p_load("DBI", "RSQLite")

read_db <- function(filepath, tables = NULL, to_tibble = TRUE) {
  con <- dbConnect(SQLite(), filepath)
  if (is.null(tables)) tables <- dbListTables(con)
  if (is.null(names(tables))) tables <- setNames(tables, tables)
  dfs <- lapply(tables, \(table) dbReadTable(con, table))
  dbDisconnect(con)
  if (to_tibble && "tibble" %in% loadedNamespaces())
    dfs <- lapply(dfs, as_tibble)
  dfs
}

write_db <- function(dfs, filepath, overwrite = FALSE, append = FALSE) {
  con <- dbConnect(SQLite(), filepath)
  Map(function(name, df) {
    dbWriteTable(con, name, df, overwrite = overwrite, append = append)
  }, names(dfs), dfs)
  dbDisconnect(con)
}
```

### Excel dates

```r
xdate <- function(x) {
  as.Date(x, origin = "1899-12-30")
}

xdatetime <- function(x, tz = "UTC") {
  as.POSIXct(x * 86400, origin = "1899-12-30", tz = tz)
}
```

### Convert data frame/column(s) to numeric

```r
as_numeric_vec <- function(vec) {
  if (is.factor(vec))
    vec <- as.character(vec)
  tryCatch({
    as.numeric(vec)
  }, warning = function(w) {
    vec
  })
}

as_numeric_df <- function(df) {
  data.frame(lapply(df, as_numeric_vec))
}
```

### Message box

```r
msgbox <- function(title, message, icon = "info", type = "ok", ...) {
  tcltk::tkmessageBox(
    title = title,
    message = message,
    icon = icon,
    type = type,
    ...
  )
}
```

## Archive (for educational purposes?)

### Excel with `data.table::`

```r
xread <- function(xlsxFile, ...) {
  df <- openxlsx::read.xlsx(xlsxFile, ...)
  DT <- data.table::as.data.table(df)
  DT
}

xread_all <- function(xlsxFile, sheets = NULL, ...) {
  if (is.null(sheets))
    sheets <- openxlsx::getSheetNames(xlsxFile)
  if (is.null(names(sheets)))
    sheets <- setNames(sheets, sheets)
  dfs <- lapply(sheets, function(sheet) {
    openxlsx::read.xlsx(xlsxFile, sheet = sheet, ...)
  })
  DTs <- lapply(dfs, data.table::as.data.table)
  DTs
}

xwrite <- function(x, file, ...) {
  # Can't think of a better way yet, just edit directly for now
  
  openxlsx::write.xlsx(
    x,
    file = file,
    headerStyle = openxlsx::createStyle(textDecoration = "bold"),
    firstActiveRow = 2,
    firstActiveCol = 2,
    colWidths = "auto",
    ...
  )
}
```

### Forward fill (simple)

```r
ffill_simple <- function(x) {
  notna_idx <- which(!is.na(x))
  rep(x[notna_idx], times = diff(c(notna_idx, length(x) + 1)))
}
```

### All duplicated instances

```r
duplicated_all <- function(x) {
  duplicated(x) | duplicated(x, fromLast = TRUE)
}
```

### Get all filepaths from specified folder(s)

```r
get.filepaths <- function(...) {
  flds <- unlist(list(...))
  setdiff(
    list.files(flds, full.names = TRUE),
    list.dirs(flds, full.names = TRUE, recursive = FALSE)
  )
}
```

### Whitespace to CSV

`data.table::` is _much faster_ for large files

```r
library(data.table)
library(tools)

whitespace.to.csv <- function(filepath) {
  DT <- data.table::fread(filepath, header = TRUE)
  new.filepath <- paste0(tools::file_path_sans_ext(filepath), ".csv")
  data.table::fwrite(DT, new.filepath)
}
```

### Reshape

- Only if `data.table::` is not available
- Otherwise, use `dcast()` and `melt()`
- For base R, better to learn how to do it manually
  - _e.g._ `grep()` and `rbind()`, or `split()`/`by()` and `merge()`, ...

```r
wide2long <- function(df, idvar, name = "name", value = "value", ...) {
  n.idvars <- setdiff(names(df), idvar)
  
  reshape(
    data = as.data.frame(df),
    varying = n.idvars,
    v.names = value,
    timevar = name,
    idvar = idvar,
    times = n.idvars,
    direction = "long",
    ...
  )
}

long2wide <- function(df, idvar, groups, sep = '.', ...) {
  reshape(
    data = as.data.frame(df),
    timevar = groups,
    idvar = idvar,
    direction = "wide",
    sep = sep,
    ...
  )
}
```

### 'Union' `rbind` for dataframes that do not have matching columns

Only if `data.table::` is not available  
Otherwise, use `rbind()`  

```r
outer.rbind <- function(...) {
  Reduce(function(x, y) {
    x[setdiff(names(y), names(x))] <- NA
    y[setdiff(names(x), names(y))] <- NA
    rbind(x, y)
  }, ...)
}
```
