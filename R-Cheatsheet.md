## Cheatsheet

### R

#### Filter all duplicated values

For display only, most of the time.

```r
all.duplicated <- function(x) duplicated(x) | duplicated(x, fromLast=TRUE)
```

#### Forward fill

Not the most robust, but simple.

```r
ffill <- function(x) {
  notna.idx <- which(!is.na(x))
  rep(x[notna.idx], times = diff(c(notna.idx, length(x) + 1)))
}
```

#### Get all filepaths from specified folder(s)

```r
get.filepaths <- function(...) {
  flds <- unlist(list(...))
  setdiff(
    list.files(flds, full.names = TRUE),
    list.dirs(flds, full.names = TRUE, recursive = FALSE)
  )
}
```

#### Replace with named vector

_Is there something simpler...?_

```r
replace.map <- function(x, mapping, standardize = FALSE) {
  if (standardize) x <- tolower(trimws(x))
  mask <- x %in% names(mapping)
  x[mask] <- mapping[x[mask]]
  x
}
```

#### Excel

```r
library(data.table)
library(openxlsx)

xlsx.date <- function(x) {
  as.Date(x, origin = "1899-12-30")
}

xlsx.datetime <- function(x) {
  as.POSIXct(x * 86400, origin = "1899-12-30", tz = "GMT")
}

xread <- function(...) {
  data.table::as.data.table(openxlsx::read.xlsx(...))
}

xread.all <- function(filepath, sheetnames = NULL, ...) {
  if (is.null(sheetnames)) {
    sheetnames <- openxlsx::getSheetNames(filepath)
    sheetnames <- setNames(sheetnames, sheetnames)
  }
  lapply(sheetnames, function(sheetname) {
    xread(filepath, sheet = sheetname, ...)
  })
}

write.one.xlsx <- function(DTs, filepath, firstActiveCol = 2, ...) {
  openxlsx::write.xlsx(
    DTs,
    file = filepath,
    headerStyle = openxlsx::createStyle(textDecoration = "bold"),
    firstActiveRow = 2,
    firstActiveCol = firstActiveCol,
    colWidths = "auto",
    ...
  )
}
```

#### SQLite

```r
library(DBI)
library(RSQLite)

dbread.tbls <- function(filepath, tables = NULL) {
  con <- DBI::dbConnect(RSQLite::SQLite(), filepath)
  
  if (is.null(tables)) tbls <- DBI::dbListTables(con) else tbls <- tables
  
  tbls <- setNames(tbls, tbls)
  tbls <- lapply(tbls, function(tbl) DBI::dbReadTable(con, tbl))
  
  DBI::dbDisconnect(con)
  
  tbls
}

dbwrite.all <- function(DTs, filepath, ...) {
  con <- DBI::dbConnect(RSQLite::SQLite(), filepath)
  
  mapply(function(name, DT) {
    DBI::dbWriteTable(con, name, DT, ...)
  }, names(DTs), DTs)
  
  DBI::dbDisconnect(con)
}
```

#### Message box

```r
library(tcltk)

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

#### Whitespace to CSV

`data.table::` is much faster for large files.

```r
library(data.table)
library(tools)

whitespace.to.csv <- function(filepath) {
  DT <- data.table::fread(filepath, header = TRUE)
  new.filepath <- paste0(tools::file_path_sans_ext(filepath), ".csv")
  data.table::fwrite(DT, new.filepath)
}
```

#### Reshape

This is too painful. Incorporate `data.table::` and use `dcast()` and `melt()`.

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

#### 'Union' `rbind` for dataframes that do not have matching columns

Refer to the documentation if using `data.table::rbind()` instead.

```r
outer.rbind <- function(...) {
  Reduce(function(x, y) {
    x[setdiff(names(y), names(x))] <- NA
    y[setdiff(names(x), names(y))] <- NA
    rbind(x, y)
  }, ...)
}
```
