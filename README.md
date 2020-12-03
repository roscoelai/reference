## Cheatsheet

### R

#### Get all filepaths from specified folder(s)

```r
get.filepaths <- function(..., prefix = NULL) {
  only.files <- function(x) x <- x[!file.info(x)$isdir]
  
  folderpaths <- unlist(list(...))
  if (!is.null(prefix)) folderpaths <- file.path(prefix, folderpaths)
  only.files(list.files(folderpaths, full.names = TRUE))
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

#### Replace/Rename

```r
replace.map <- function(x, mapping) {
  mask <- x %in% names(mapping)
  x[mask] <- mapping[x[mask]]
  x
}

rename.map <- function(x, mapping) {
  names(x) <- replace.map(names(x), mapping)
  x
}
```

#### Reshape

```r
library(tibble)

wide2long <- function(df, idvar, name = "name", value = "value", ...) {
  n.idvars <- setdiff(names(df), idvar)
  
  df <- reshape(
    data = as.data.frame(df),
    varying = n.idvars,
    v.names = value,
    timevar = name,
    idvar = idvar,
    times = n.idvars,
    direction = "long",
    ...
  )
  
  df <- tibble::as_tibble(df)
  df
}

long2wide <- function(df, idvar, groups, sep = '.', ...) {
  df <- reshape(
    data = as.data.frame(df),
    timevar = groups,
    idvar = idvar,
    direction = "wide",
    sep = sep,
    ...
  )
  
  df <- tibble::as_tibble(df)
  df
}
```

#### Read all sheets in an Excel Workbook

```r
library(readxl)

read.xlsx.all <- function(filepath, ...) {
  sheetnames <- readxl::excel_sheets(filepath)
  sheetnames <- setNames(sheetnames, sheetnames)
  lapply(sheetnames, function(sheetname) {
    readxl::read_xlsx(filepath, sheet = sheetname, ...)
  })
}
```

#### Save one Excel Workbook

```r
library(openxlsx)

save.one.xlsx <- function(dfs, filepath, firstActiveCol = 2, ...) {
  openxlsx::write.xlsx(
    dfs,
    file = filepath,
    headerStyle = openxlsx::createStyle(textDecoration = "bold"),
    firstActiveRow = 2,
    firstActiveCol = firstActiveCol,
    colWidths = "auto",
    ...
  )
}
```

#### Other wrappers

```r
library(tibble)

pretty.cbind <- function(...) tibble::as_tibble(cbind(...))

pretty.merge <- function(...) tibble::as_tibble(merge(...))
```

#### Hope we never have to use these...

```r
xlsx.date <- function(x) {
  as.Date(x, origin = "1899-12-30")
}

xlsx.datetime <- function(x) {
  as.POSIXct(x * 86400, origin = "1899-12-30", tz = "GMT")
}
```

#### Why is this here? Nvm, remove after leveling up...

```r
join.lists <- function(...) do.call(c, ...)
```
