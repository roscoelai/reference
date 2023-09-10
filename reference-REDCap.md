# REDCap Reference Page

This document started out as a collection of pointers for instrument design. Its goal is to minimize pain and regret in the future.

It has since started brancing out to other topics, so might be a little disorganized at the moment.

There are trivial details behind the workings of REDCap that you might not be aware about. The author is aware of some of them, because the author has made these mistakes before. Hopefully by sharing, you don't have to go through the five stages of grief.

- The uninitiated might have some difficulty appreciating some of the pointers here
- To get initiated, consider this course on [Data Management for Clinical Research](https://www.coursera.org/learn/clinical-data-management) on Coursera offered by Vanderbilt University

---

### Sections
- Instrument Design
    - Basic
    - Intermediate
    - Advanced
- Reports
- Survey Queue

---

# Instrument Design

## Basic

### Names

> Deciding on names is more difficult than you think.  
> You will spend more time here than expected, but it will be time well spent.

#### Forms (_a.k.a._ Instruments, ...)

##### There are 2 names
1. One that is displayed on the screen when visiting the website (let's call this "display name")
2. One that exists in the database (let's call this "form name", because the data dictionary also refers to it as such)

##### Rules for form names
- 50 characters or less (any excess will be truncated, beware!)
- Permitted characters: `0123456789_abcdefghijklmnopqrstuvwxyz`
- First character must be one of: `abcdefghijklmnopqrstuvwxyz`
- The display name will allow more than this, but in the form name
    - spaces will be replaced with underscores
    - other characters will be removed (take note of `-`, `&`, `(`, and `)`)
    - truncation after 50 characters
- Must be unique
    - If there is a clash, characters will be appended (silently)

##### How to set form names?
1. Under the "Form Name" column in the data dictionary
    - Must follow the rules
3. Rename instrument name (the display name) in the online designer
    - Rules for display name are more permissive (for display after all)
    - The form name will take the display name and (silently) transform it to conform to form name rules
    - Only in development mode
    - In production mode, this will not change the form name
    - _i.e._ _permanent_, so try not to have `demo_` in the form name

##### What happens when uploading .zips?
- The default display name will <ins>not</ins> be the form name
- Underscores will be replaced with spaces, the final string will be in title case
- Correction might be necessary
- _e.g._
    - Online designer: `My Awesome Questionnaire (MAQ)` (intended display name)
    - Data dictionary: `my_awesome_questionnaire_maq`
    - After uploading .zip: `My Awesome Questionnaire Maq`
    - Rename online after upload: `My Awesome Questionnaire (MAQ)`

##### Do not change form names after collecting data
- Just don't do it

---

#### Variables (_a.k.a._ Fields, Columns, ...)

##### Rules
- 26 characters or less (REDCap might accept more, but don't do it!)
- Permitted characters: `0123456789_abcdefghijklmnopqrstuvwxyz`
- First character must be one of: `abcdefghijklmnopqrstuvwxyz`
- REDCap will enforce uniqueness (so don't be alarmed when pop-ups appear)
- Cannot be changed in production

##### Conventions
- Prefix with acronym of the form name
- Separate parts with underscores
- Unfortunately, underscores might have to perform double-duty as replacements for `.`s also
- If possible, maintain/reserve the pattern `_q[0-9]+` for specifying individual raw items in SAQs
    - This will be **very helpful** in the future
    - CRF fields, if not numbered, might use more descriptive names
- _e.g._
    - `maq_q1`, `maq_q2`, ..., `maq_q123`
    - `maq_q5_1_2_1`, `maq_q5_1_2_2`, ...

---

### Field attributes

#### Field labels
- What participants actually see
- What someone might look for in the data dictionary
- When displayed on forms and surveys, REDCap has a default style
- Text are bold by default
- To make it un-bold would take some work
- HTML will be rendered in the browser, but will appear as text in the data dictionary

### Basic HTML

> Might be good to take a course on basic HTML/CSS to learn about the different elements and attributes.

#### Some commonly used elements
- Basic: `<h1>, <h2>, ..., <h6>`, `<br>`, `<hr>`, `<p>`
- Formatting: `<b>`, `<em>`, `<i>`, `<strong>`, `<u>`
- Styles and semantics: `<div>`, `<span>`

#### Some commonly used attributes
- Perhaps just `style` will do for now

#### How to unbold?
- `<p style="font-weight: normal;">Some unbolded text.</p>`
- `<span style="font-weight: normal;">Some unbolded text.</span>`
- `<span style="font-weight: lighter;">Some unbolded text.</span>`

#### How to indent?
- `<p style="margin: 0 0 0 10%;">Non-descriptive field indent level 1.</p>`
- `<p style="margin: 0 0 0 20%;">Non-descriptive field indent level 2.</p>`
- `<p style="margin: 0 0 0 5%;">Descriptive field indent level 1.</p>`
- `<p style="margin: 0 0 0 10%;">Descriptive field indent level 2.</p>`

#### How to insert a line break (newline)?
- `<br>`
- If unsure, use the Rich Text Editor
- Do <ins>not</ins> use raw literal line breaks in any field attributes (it messes up the data dictionary)
    - Field labels
    - Calculated field
    - Branching logic
    - Action tags

#### References
- [HTML Element Reference - By Category](https://www.w3schools.com/tags/ref_byfunc.asp)
- [CSS Reference](https://www.w3schools.com/cssref/index.php)

---

### Comparisons

| Operator | Alias | Description           | Recommendation                                     | Example                                |
|:--------:|:-----:|:---------------------:|:--------------------------------------------------:|:--------------------------------------:|
| `=`      | `eq`  | Equal                 | Quote values (including numbers, _especially_ `0`) | `[var] = '0'` (instead of `[var] = 0`) |
| `<>`     | `ne`  | Not equal             | Quote values (including numbers, _especially_ `0`) | `[var] = '0'` (instead of `[var] = 0`) |
| `<`      | `lt`  | Less than             | Values will likely be numbers, _do **not** quote_  | `[var] < 1`                            |
| `>`      | `gt`  | Greater than          | Values will likely be numbers, _do **not** quote_  | `[var] > 2`                            |
| `<=`     | `le`  | Less than or equal    | Values will likely be numbers, _do **not** quote_  | `[var] <= 3`                           |
| `>=`     | `ge`  | Greater than or equal | Values will likely be numbers, _do **not** quote_  | `[var] >= 4`                           |

#### Why use `[var] = '0'` instead of `[var] = 0`?

Suppose you had a Yes/No question (where Yes = 1 and No = 0) with a follow up question that should only appear when "No" is selected. If you wrote `[var] = 0` as the branching logic, the follow up question <u>will be visible</u> until the participant selects "Yes". So `[var] = 0` will also be considered true if no selection had been made yet. The author only has experience of this particular scenario. In other cases, not quoting numbers should be fine.

#### Comparing dates

If your dates are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant, string comparisions should be fine, and you are free to use any of the operators above. Otherwise, you must use the `datediff()` function.

---

### Calculations

#### Summation

There are two general ways to add values from fields together:
1. `[var_1] + [var_2] + ... + [var_n]`
2. `sum([var_1], [var_2], ..., [var_n])`

The difference comes in how they deal with [NaN](https://en.wikipedia.org/wiki/NaN)s. `1.` will propagate `NaN`s while `2.` will ignore `NaN`s.

If you are calculating a subscale that involves adding values together, and no missing values can be tolerated, then use `1.`. If any of the variables are blank, the final result will also be blank.

If you are calculating a subscale that involves adding values together, and some missing values are expected, then use `2.`. Any blank variables will be ignored, and the rest will be summed up.

If in doubt, use `1.` most of the time. Even if all the fields involved are set as required fields, a participant might only complete the SAQ partially. If `2.` were used, the subscale score will not be blank, and might be incorrect. Do <ins>**not**</ins> use `1.` when the fields involved are hidden behind gatekeeper questions. In that case, some of them might be expected to be blank, so use `2.` instead.

#### `datediff()`

The function signature is: `datediff([date1], [date2], "units", returnSignedValue)`
- Subtraction is [noncommutative](https://en.wikipedia.org/wiki/Commutative_property), thus the order of operands is important
- The operation is `[date2] - [date1]`
- The string `"today"` or `"now"` can be used in place of `[date1]` or `[date2]`
    - Discouraged by the community
    - Strongly discouraged (officially) to be used in calculated fields (if you choose to ignore this advice, be prepared for the consequences)
    - Might be useful in other places (_i.e._ survey queue, dashboard, reports, ...)
- `units`
    - `"y"` years (1 year = 365.2425 days)
    - `"M"` months (1 month = 30.44 days)
    - `"d"` days
    - `"h"` hours
    - `"m"` minutes
    - `"s"` seconds
- `returnSignedValue` is `false` by default
    - Leave it if you are sure the dates never cross
    - Otherwise, strongly encouraged to set it to `true`
- _e.g._ `datediff([date1], [date2], 'd', true)`

#### Rounding off decimal numerals

A problem that might crop up when checking for incorrect values for calculated fields (Rule H) is decimal numerals with different values, but at very low decimal places (12th and 13th have been seen before). If time permits, read up on [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754). The community recommendation is to round off such values to some number of decimal places.

How many decimal places?

Instrument builders may not have the authority to make this decision. Whoever has authority over the measurement should have knowledge about its [uncertainty](https://www.youtube.com/watch?v=GtOGurrUPmQ&t=280s):

[![uncertainty](https://img.youtube.com/vi/GtOGurrUPmQ/1.jpg)](https://www.youtube.com/embed/GtOGurrUPmQ?start=280&end=300)

---

## Intermediate

### `@DEFAULT` gotchas
- Default values are only loaded when a _brand new_ form record is created
- Default values will not be loaded on a pre-existing form record
- It makes sense, but have to consider order of operations

### Embedded fields

- If it involves tables, use the Rich Text Editor to help
  - Adjust attributes in the HTML source code
  - Most important would be column widths
  - For larger tables, optimize with a few rows first
  - Reduce the volume of HTML by deciding where to apply styles
- Embedding to a checkbox field
  - _Will not work with enhanced buttons_ &mdash; the field(s) will not appear
  - _i.e._ a checkbox field with an "Other(s)" option cannot have _both_ an embedded field and enhanced buttons activated
    - _Choose one_

### Non-standard characters

- Watch out for these &mdash; They might disappear, or be replaced with a box/hyphen/question mark
  - Tip: Avoid using Excel to edit CSV
- Some listed below:

HTML       | Symbol
:---------:|:--------:
`&mdash;`  | &mdash;
`&ge;`     | &ge;
`&eacute;` | &eacute;

### Logic gotchas
- `[var1] > [var2] + 2` is **_not_** the same as `[var1] - [var2] > 2`
  - This one confounded for a very long time...

---

## Advanced

### Implementing lookup tables

#### Can we implement lookup tables in REDCap instruments (where there's no analog to `VLOOKUP`)?

**Yes.**

But a `O(n)` implementation will likely not work, or be _very inefficient_ if it did. You must implement at least a `O(log n)` solution, or ideally a `O(1)` solution.

##### Details you probably don't care about (until you _do_)
- PHP might have a maximum function nesting level of 256
- The `if()` function in REDCap likely makes function calls itself, likely around the order of 3
- So we can practically nest about 80 levels of `if()` calls maximum

##### Strategies

###### Linear nested `if()`s (`O(n)`)
- `if([var] = 0, 0, if([var] = 1, 1, if([var] = 2, 4, if([var] = 3, 9, ..., if([var] = 79, 6241, if([var] = 80, 6400, ""))...))))`
- If nested linearly, we can only map about 80 values before REDCap throws an error
- And it will be slow if it does work

###### Binary tree nested `if()`s (`O(log n)`)
- `if([var] < 64, if([var] < 32, if([var] < 16, if([var] < 8, if([var] < 4, if([var] < 2, if([var] < 1, 0, 1), if([var] < 3, 4, 9)), ...)))))`
- If nested in a binary tree, we could go up to 2<sup>80</sup> (it is a _very_ big number), and _much_ faster
- The speedup is not theoretical, we have tried, and it's noticeable at the level of human perception
- But as you can see, it is not so intuitive to write (or read)

###### Linear/Polynomial equations (`O(1)`?)
- We might be able to do even better with a single equation
- We don't need to make `if()` calls
- If the points to map fall close enough to a straight line, use linear regression
- It's also possible to go up to polynomial using Horner's method
- The most likely cases so far are staircase functions, which are simpler but more tedious
- Equations can be constructed programatically, rather than being written by hand

---

# Reports

### Names (again)

> Told you it's important.  
> Perhaps not as important as variable or form names, but this will affect the file names of exports.
> You can rename files, sure, but when exporting en masse, this can cause a lot of frustration.

### Report naming gotchas
- Things to consider when deciding the report names
- Reports downloaded from REDCap will have auto-generated file names
- At least for CSV files, the rules seem to be as follows:
  - let `<project name>` refer to the project name with non-alphanumeric characters (including spaces) removed, truncated to <ins>**the first 20 characters**</ins>
    - _e.g._ `"[My Fancy Tag] My Awesome Project" -> "MyFancyTagMyAwesomeP"`
  - let `<report name>` refer to the report name with non-alphanumeric characters (including spaces) removed, truncated to <ins>**the first 20 characters**</ins>
    - _e.g._ `"Really Important Report of Important Instrument V2.5" -> "ReallyImportantRepor"`
    - _e.g._ `"Important Report Ver 2.5 (some extra words)" -> "ImportantReportVer25"`
  - `<timestamp>` is of the format `YYYY-mm-dd_HHMM`
  - `<project name>-<report name>-DATA-<timestamp>.csv` for raw data
    - `"MyFancyTagMyAwesomeP-ImportantReportVer25-DATA-2109-12-31_1159.csv"`
  - `<project name>-<report name>-DATA_LABELS-<timestamp>.csv` for labels
    - `"MyFancyTagMyAwesomeP-ImportantReportVer25-DATA_LABELS-2109-12-31_1159.csv"`
  - There will be no spaces
  - Any distinguishing features, especially <ins>**version numbers**</ins>, should be <ins>within the first 20 characters</ins> of the report name (not counting spaces), otherwise all reports downloaded will have the same name and may need to be manually renamed

---

# Survey Queue

The following can be run from console after activating the Survey Queue set up pop-up window.

### "Export" survey queue rules

There is no such function at the moment, so here's a workaround:

```js
const els = document.querySelectorAll('[id^="sqtr-"]');
const rows = [];
const delim = ",";

for (const el of els) {
    let title = el.querySelector("td:nth-child(2)");
    let condlogic = el.querySelector('[id^="sqcondlogic-"]');
    let title_text = title.innerText.replaceAll(/\s+-\s+/g, delim);
    let cond_text = condlogic.innerHTML.replaceAll("&lt;", "<").replaceAll("&gt;", ">").replaceAll('"', '""');
    rows.push(`${title_text}${delim}"${cond_text}"`)
}

let res = rows.join("\n");
res
```

Right-click, select `Copy string contents`, paste in Notepad, and save as a .csv file.

### Find-and-replace

```js
const textareas = document.getElementsByTagName("textarea");
const regex = / some regex pattern /;

for (const el of textareas) {
    if (el.innerHTML.match(regex)) {
        // console.log(el.innerHTML);
        el.innerHTML = el.innerHTML.replace(regex, "");
    }
}
```

---


