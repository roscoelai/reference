# REDCap Cheatsheet

The uninitiated might have some difficulty appreciating some of the pointers here. To get initiated, consider this course on [Data Management for Clinical Research](https://www.coursera.org/learn/clinical-data-management) on Coursera offered by Vanderbilt University.

<hr />

## Instrument Design

### `@DEFAULT` gotchas
- Default values are only loaded when a _brand new_ form record is created
- Default values will not be loaded on a pre-existing form record
- It makes sense, but have to consider order of operations

### Implementing lookup tables
- There is a limit to nested `if()` functions
  - '256'?
  - More like 80+
  - Linear nested `if()`s will quickly hit the limit for large tables
  - There are a few possible strategies to handle such cases:
    - Nested `if()`s rearranged in complete/balanced binary tree form, instead of linear
      - Height reduced from `n` to `log(n)`
      - Converting from linear to branched significantly reduces lag
    - Linear combination of indicator variables multiplied by step heights (<- **this looks the most promising**)
      - Avoid calls to `if()`
      - Can micro-optimize by combining with balanced binary tree, but will become very unreadable
      - Only works for numeric values
    - Piecewise linear/polynomial regression, expressions written using Horner's method
      - Challenging to find an equation that ends up close enough to all points
      - Usually have to break the domain into pieces
      - Higher-order equations tend to require coefficients with more decimal places
      - Only works for numeric values
  - All alternatives will probably be harder to read compared to linear nested `if()`s 😞
  - Please avoid writing equations by hand
    - Read the look up table(s) from _e.g._ a spreadsheet and make the computer generate the formula(e)

### Logic gotchas
- `[var1] > [var2] + 2` is **_not_** the same as `[var1] - [var2] > 2`
  - This one is really pushing it...

### Variable names (or field names, column names)

- Rules
  - Only _lower case_ letters, numbers, and underscores allowed
  - Must begin with a lower case letter
  - Must be unique
  - Ideally no more than 26 characters
  - Variable names cannot be changed in production
- Recommendations
  - Use underscores to separate parts of the variable name
  - Prefix all variables in an instrument with an abbreviation of the instrument name
    - Different instruments might share abbreviations, so might need alternatives
  - Followed by `_v2`, `_v3`, _etc._ for later versions
    - Try not to have more than 9 versions
    - So version 1.1 can be represented by `_v11`, and version 2.2 by `_v22`, _etc._
    - `.` is not a valid character (this is not R), and we don't want to abuse `_`
  - Followed by an abbreviation of the section name (if there are sections)
  - Might have to include a number somewhere if there are repetitions
  - For individual questions, place a "q" before question numbers
    - This will allow selecting/filtering columns using the regular expression `_q\\d+`
  - Suffixes for descriptive fields used so far: `_tbl`, `_inst`, `_disp`

### Form names (or instrument names)

- There is a display name, and an actual name (the one used for calculations, conditional logic, piping, _etc._)
- Rules for the actual name are similar to variable names
  - Only _lower case_ letters, numbers, and underscores allowed
    - Spaces will be replaced with underscores, all other characters will be removed
  - Will begin with a lower case letter
  - Will be unique
    - Random characters will be added if there is a clash
  - Will have no more than 50 characters
    - Extra characters will be removed
- The default display name takes the actual name, replaces underscores with spaces, and uses title case
  - This is done when importing an instrument using a .zip file
  - The result is almost always incorrect
  - You will almost always have to fix it manually
- In development mode, changing the display name will change the actual name (subject to the rules above)
- In production mode, changing the display name will not affect the actual name (so please don't put `demo_` in the name - it will be stuck there)
  - Do not change form names for forms that have collected data

### Field labels

- Variable names are (soft) limited to 26 characters and unlikely to give a clear self-description
- Field labels contain the actual text that gets displayed, and allow more detailed descriptions
- Field labels should contain the answers when looking up the data dictionary and asking what variables mean
- Field labels might contain inline styling/formatting required by some instruments
  - Might become harder to read because of the HTML tags

### HTML elements

- Containers
  - `<div>`
    - When in doubt, use `<div>`
    - One exception: Custom text to display at top of survey queue &mdash; use `<p>` instead
  - `<p>`
    - Avoid using with "indentations" (_i.e._ `style="margin: 0 0 0 10%;"`), font size gets affected for some reason
  - `<span>`
    - The preferred option when text is guaranteed to be one line
    - Error messages are displayed properly
  - `<font>`
    - Most likely used as `<font color="red">...</font>`
    - Useful to reduce volume of HTML
- Others
  - `<strong>/<b>`, `<em>/<i>`, `<u>`
  - `<br />`, `<hr />`
  - `<h1>`, ..., `<h6>`
  - ...

### Unbold

- `style="font-weight: normal;"` or `style="font-weight: lighter;"`

### Indentation

- One level of indentation with
  - `style="margin: 0 0 0 10%;"` (for non-descriptive fields)
  - `style="margin: 0 0 0 5%;"` (for descriptive fields)
- + 10% (or 5%) for each additional level of indentation

### Newlines (or line breaks)

- Newlines will mess up the data dictionary, avoid or replace with `<br />` if possible
- Avoid newlines in
  - Field labels
    - Or activate the Rich Text Editor if you refuse to comply
  - Branching logic
  - Calculated field
  - Action tags
- Newlines in survey queue logic is OK, and highly recommended! :thumbsup:
  - That is, until they implement some way to export the survey queue logic

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

<hr />

## Operators and functions

### Comparison operators

- `=` and `<>`
  - Quote all values (including integers)
    - There is an advantage for branching logic of `[var] = '0'` over `[var] = 0`
    - For other integers, there should be no difference
- `<`, `>`, `<=`, and `>=`
  - _Do not_ quote anything
- Comparing dates
  - Must use `datediff()`, or it will be a string comparison

### Calculations

- Summation of variables
  - `[var_1] + [var_2] + ... + [var_n]` will not ignore blanks
  - `sum([var_1], [var_2], ..., [var_n])` will ignore blanks
- `datediff()`
  - Signature: `datediff([date1], [date2], "units", "date format", Return Signed Value)`
  - Most likely use: `datediff([date1], [date2], 'd', true)`
  - Calculation is `[date2] - [date1]`, results returned in the unit specified
  - _Always return signed values_
    - _Especially_ when using `datediff("today", [date2], 'd', true)`, where `[date2]` is in the future
    - May not be necessary if `[date2]` is _always_ greater (or lesser) than `[date1]`
  - "today"
    - Avoid using it if possible
    - If using it, avoid storing values that depend on calculations involving it
    - If storing values that depend on it... haiz... [be prepared](https://www.youtube.com/watch?v=zPUe7O3ODHQ&t=138s) for inaccuracies
- Less stress on Rule H
  - Round off all values with decimal places
  - How many decimal places? Someone should know about the [uncertainty of the measurements](https://www.youtube.com/watch?v=GtOGurrUPmQ&t=280s)
