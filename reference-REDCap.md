# REDCap Cheatsheet

Most of the points here are not beginner-level, and might require some experience designing instruments (and banging heads against tables/walls) for a better appreciation. Many of these can be safely disregarded for most validated instruments. Otherwise, this would (hopefully) help to avoid some pitfalls.

## Names

### Variable names (Field names)

- Standard rules apply, but it's slightly stricter here:
  - Only letters, numbers, and underscores
  - Letters must _(will)_ be lower case
  - Must _(Will)_ begin with a letter
  - Does not already exist (not already taken by another variable)
  - No more than 26 characters (discouraged, but still allowed)
- Suggestions:
  - Start with an abbreviation of the instrument name
    - Best if it's recognized/universal/standardized
    - Might be a problem if there are multiple instruments with the same abbreviation
  - Use underscores to separate parts of the variable name, or to substitute dots
  - Other conventions as necessary:
    - _e.g._ "_tbl" suffix for tables, or "_desc" or "_inst" suffixes for descriptive fields, place a "q" before question numbers
  - ...
- Variable names cannot be changed in production, so any bad decisions made will persist to the end of the instrument's lifecycle

### Form names (Instrument names)

- What is displayed online can be adjusted by the user(s)
- The _real_ name has to follow rules:
  - Only letters, numbers, and underscores
  - Letters _will_ be lower case
  - _Will_ begin with a letter
  - Illegal characters _will_ be removed
  - **_WILL HAVE_ no more than 50 characters**
    - Long names will be truncated to 50 characters
    - Multiple instruments with very long, almost identical names only differing at the end... will not fare well
- Default display names of uploaded instruments will be in title case
  - Abbreviations (supposed to be all capitals) may need to be fixed
  - Brackets and/or hyphens may need to be restored
- How to edit form names online
  - In development
    - Changing the instrument name in the online designer will immediately create a new name that follows the rules above
  - In production
    - _Impossible_ &mdash; Changing the instrument name in the online designer will only affect the display
    - The only way is to modify the instrument or project data dictionary and upload
- Unlike variable names, form names can be changed in production, but that would be a terrible idea, so any bad decisions made will most likely persist to the end of the form's lifecycle

Do we need good variable/form names? No. We could give random characters to everything, as long as there are no duplicates. But doing so will make everything else intractable. We will _want_ good names.

## Field labels (WIP)

- ...

### HTML elements to contain text

- Usually used when we need to apply inline style during instrument design
  - `<div>`
    - Recommended for most cases when dealing with a block of text, _e.g._ for indentation
  - `<p>`
    - Most likely `<div>` will be preferred, because it has been observed that `<p>` may have inconsistent font styles with different indentation levels &mdash; Specifically, smaller font sizes for deeper indentation levels, which is a surprise
    - There are some cases where `<p>` will have to be used over `<div>`, _e.g._ custom messages in the survey queue page &mdash; Using `<div>` with long sentences may result in text overflowing out of the header region and even the viewport
  - `<span>`
    - Usually for short phrases or sentences
    - Using this for block indentation would be a terrible mistake
  - `<font>`
    - Might be more convenient in some cases, _e.g._
      - `<font color="red">` vs. `<span style="color: red;">`
  - Inline styles can also be specified on other elements such as `<strong>`, `<em>`, `<u>`, `<b>`, `<i>`, _etc._

### Newlines/Line breaks

- Avoid newlines &mdash; They will mess up the data dictionary
  - Number of lines in the data dictionary will not correspond with the number of fields
  - May use newlines when first creating a field, because it's easier to read
  - But once finalized, replace all newlines with `<br />`
- Creating a nicely formatted HTML table within a field label will produce a messed up field label, because all the newlines will accumulate above the table, resulting in a massive blank space
  - Solve by removing all the newlines
  - HTML code will be less readable

### Indentation

- Currently using `<... style="margin: 0 0 0 10%;">` for one level of indentation for non-descriptive fields
- +10% for each level of indentation
- Descriptive fields will require the percentage to be halved for a similar (approximate) indentation level

### Unbold

- `<... style="font-weight: normal;">`

### Embedded fields

- Will most likely involve tables
  - Can make use of the Rich Text Editor to help create tables
  - Will most likely need to edit the HTML to adjust column widths (and maybe row heights)
  - Recommend adjusting parameters with 2-3 rows
  - Add the rest of the rows after finalizing parameters (to avoid massive corrections)
  - The auto-generated HTML code may not be efficient, which will bloat up the data dictionary
  - Apply the 'majority' style at the highest level, then individual styles to exceptions
- Embedding to a checkbox field
  - _Will not work with enhanced buttons_ &mdash; the field(s) will not appear
  - _e.g._ a checkbox field with an "Other(s)" option cannot have _both_ an embedded field and enhanced buttons activated
    - _Choose one_

### Comparison operators

- Equality `=` and inequality `<>`
  - Quote values
  - If `[var] = 0` is used in branching logic for a field, it will be revealed even if no option is selected
  - If `[var] = '0'` is used instead, it will be hidden until a value of '0' is selected (this is one known advantage of quoting; impact on performance from type coercion is unclear)
- Others (`<`, `<=`, `>`, `>=`)
  - _Do not_ quote numeric values

### Non-standard characters

- Might cause problems (_i.e._ disappear, and replaced with a box, or a question mark, or a hyphen)
  - `&mdash;`: &mdash;
  - `&ge;`: &ge;
  - `&eacute;`: &eacute;

### Calculations

- Summation of variables
  - `[var1] + [var2] + ... + [varn]` will not ignore blanks
  - `sum([var1], [var2], ..., [varn])` will ignore blanks
  - Choose the appropriate one
  - For simple surveys where all fields are required, there is no difference
- Variables that never change or only change at data entry
  - Create fields to store them if needed for calculations later
- Variables that change daily
  - _Do not_ store &mdash; At some point they will be _misinformation_
  - Solve the `saqstats` problem
    - No known solution, yet
    - Statuses 2-5 require checking windows, so cannot be tied to events
- `datediff()`
  - `datediff([date1], [date2], "units", "date format", Return Signed Value)`
  - Calculation is `[date2] - [date1]` in the units specified
  - _Always return signed values_
    - _Especially_ when using `datediff("today", [date2], 'd', true)`, where `[date2]` is in the future
    - May not be necessary if `[date2]` is _always_ greater than `[date1]`
  - Using datetimes or asking for larger units (> days) might give results with fractional components
    - There might be differences in how PHP and JS calculate time intervals
    - So, consider rounding off to a reasonable number of decimal places to give Rule H a break
