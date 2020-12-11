## Cheatsheet

### R

#### Filter all duplicated values

```r
all.duplicated <- function(x) duplicated(x) | duplicated(x, fromLast=TRUE)
```

#### Forward fill

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

```r
replace.map <- function(x, mapping) {
  mask <- x %in% names(mapping)
  x[mask] <- mapping[x[mask]]
  x
}
```

#### Dealing with Excel files

```r
library(data.table)
library(openxlsx)
# library(readxl)

xlsx.date <- function(x) {
  as.Date(x, origin = "1899-12-30")
}

xlsx.datetime <- function(x) {
  as.POSIXct(x * 86400, origin = "1899-12-30", tz = "GMT")
}

xread <- function(...) {
  # data.table::as.data.table(readxl::read_xlsx(...))
  data.table::as.data.table(openxlsx::read.xlsx(...))
}

xread.all <- function(filepath, ...) {
  # sheetnames <- readxl::excel_sheets(filepath)
  sheetnames <- openxlsx::getSheetNames(filepath)
  sheetnames <- setNames(sheetnames, sheetnames)
  lapply(sheetnames, function(sheetname) {
    xread(filepath, sheet = sheetname, ...)
  })
}

save.one.xlsx <- function(DTs, filepath, firstActiveCol = 2, ...) {
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

dbread.all <- function(filepath) {
  con <- DBI::dbConnect(RSQLite::SQLite(), filepath)
  
  tables <- DBI::dbListTables(con)
  tables <- setNames(tables, tables)
  tables <- lapply(tables, function(table) DBI::dbReadTable(con, table))
  
  DBI::dbDisconnect(con)
  
  tables
}

dbwrite.all <- function(DTs, filepath, ...) {
  con <- DBI::dbConnect(RSQLite::SQLite(), filepath)
  
  mapply(function(name, DT) {
    DBI::dbWriteTable(con, name, DT, ...)
  }, names(DTs), DTs)
  
  DBI::dbDisconnect(con)
}
```

#### Reshape

```r
library(tibble)

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

```r
outer.rbind <- function(...) {
  Reduce(function(x, y) {
    x[setdiff(names(y), names(x))] <- NA
    y[setdiff(names(x), names(y))] <- NA
    rbind(x, y)
  }, ...)
}
```
