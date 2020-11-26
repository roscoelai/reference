## Cheatsheet

### R

#### Get all filepaths from specified folder(s)

```r
get.filepaths <- function(..., prefix = NULL) {
  folderpaths <- unlist(list(...))
  if (!is.null(prefix)) folderpaths <- file.path(prefix, folderpaths)
  list.files(folderpaths, full.names = TRUE)
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
all.duplicated <- function(x) x[duplicated(x) | duplicated(x, fromLast=TRUE)]
```

#### Forward fill

```r
ffill <- function(x) {
  notna <- which(!is.na(x))
  rep(x[notna], times = diff(c(notna, length(x) + 1)))
}
```

#### Read all sheets in an Excel Workbook

```r
read.xlsx.all <- function(filepath, ...) {
  sheetnames <- readxl::excel_sheets(filepath)
  sheetnames <- setNames(sheetnames, sheetnames)
  lapply(sheetnames, function(sheetname) {
    readxl::read_xlsx(filepath, sheet = sheetname, ...)
  })
}
```

#### Wrappers

```r
pretty.cbind <- function(...) tibble::as_tibble(cbind(...))

pretty.merge <- function(...) tibble::as_tibble(merge(...))

wide2long <- function(df, value = "value", name = "name", idvar = NULL) {
  if (is.null(idvar)) idvar <- names(df)[1]
  n.idvars <- setdiff(names(df), idvar)
  
  df <- reshape(
    data = as.data.frame(df), 
    varying = n.idvars, 
    v.names = value, 
    timevar = name, 
    idvar = idvar, 
    times = n.idvars, 
    direction = "long"
  )
  
  df <- tibble::as_tibble(df)
  df
}
```

#### Hope we never have to use these...

```r
xlsx.date <- function(x) as.Date(x, origin = "1899-12-30")

xlsx.datetime <- function(x) as.POSIXct(x * 86400, origin = "1899-12-30", tz = "GMT")
```

#### Why is this here? Nvm, remove after leveling up...

```r
join.lists <- function(...) do.call(c, ...)
```
