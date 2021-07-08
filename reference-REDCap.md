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
  - In development:
    - Changing the instrument name in the online designer will immediately create a new name that follows the rules above
  - In production:
    - _Impossible_ &mdash; Changing the instrument name in the online designer will only affect the display
    - The only way is to modify the instrument or project data dictionary and upload
- Unlike variable names, form names can be changed in production, but that would be a terrible idea, so any bad decisions made will most likely persist to the end of the form's lifecycle

Do we need good variable/form names? No. We could give random characters to everything, as long as there are no duplicates. But doing so will make everything else intractable. We will _want_ good names.

## Field labels

- Variable names may have limited ability to express the full nature of variables
- Field labels will allow a more detailed description, and fulfills this function in the data dictionary
- Field labels are also what get displayed in forms and more importantly surveys
  - Field labels might need to incorporate HTML and inline CSS to prettify content
  - Data dictionary may be harder to read with the addition of HTML tags

### HTML elements

- `<div>` and `<p>`
  - Use for styling a block of text, _e.g._ block indentation
  - Interchangable in most cases, but one might be preferred over the other in some situations (might have something to do with REDCap's default styling for each)
  - Use `<div>` for indenting labels within instruments
    - `<p>` has a surprising effect of reducing font size with indentation level &mdash; Surprises are bad
  - Use `<p>` for the survey queue custom message
    - Text in `<div>` will not wrap, and long sentences might trail out of the viewport
- `<span>` and `<font>`
  - Use when applying a style within a line, or limited to one line
  - Do not use for block indentation
  - `<font>` might require less code in some cases
- Others:
  - `<strong>`, `<em>`, `<u>`, `<b>`, `<i>`, `<h1>`, ..., `<h6>`, ...

### Newlines (Line breaks)

- Avoid newlines if possible (use `<br />` instead)
  - Newlines will mess up the data dictionary
    - The number of lines in the data dictionary will not match the number of fields in the instrument (after accounting for the header)
    - Not a major consequence, but best to avoid unnecessary discrepancies
    - Suggestion:
      - Use newlines when first creating a field, because it's easier to read
      - Once finalized, replace all newlines with `<br />`
- HTML tables will have to be done in a single line
  - If not, all the newlines will accumulate into a massive blank space above the table
  - Does not apply when using the Rich Text Editor

### Indentation

- Currently using `<... style="margin: 0 0 0 10%;">...</...>` for one level of indentation for non-descriptive fields
- +10% for each level of indentation
- Descriptive fields will require half the percentage for a similar indentation level

### Unbold

- `<... style="font-weight: normal;">...</...>` or `<... style="font-weight: lighter;">...</...>`

### Embedded fields

- Will likely involve tables in most cases
  - Can make use of the Rich Text Editor to help create tables
  - Adjust column widths (and other attributes) in the HTML source code
  - Suggestion:
    - "Optimize" using 2-3 rows before adding the rest (for larger tables)
  - HTML source code generated by the Rich Text Editor may not be the most efficient
    - Just like VBA code generated by the Macro Recorder
    - This might massively bloat up the data dictionary
    - Determine the "majority" style of the table and apply it
    - Then tend to individual exceptions
- Embedding to a checkbox field
  - _Will not work with enhanced buttons_ &mdash; the field(s) will not appear
  - _i.e._ a checkbox field with an "Other(s)" option cannot have _both_ an embedded field and enhanced buttons activated
    - _Choose one_

### Non-standard characters

- Watch out for these &mdash; They might disappear, or be replaced with a box/hyphen/question mark
- Some listed below:

HTML       | Symbol
:---------:|:-----:
`&mdash;`  | &mdash;
`&ge;`     | &ge;
`&eacute;` | &eacute;

## Operators and functions

### Comparison operators

- Equality `=` and inequality `<>`
  - To standardize practice, quote values compared against
  - There is an advantage in doing so for branching logic
    - If branching logic is `[var] = '0'`, field will not appear until `[var]` has a value of `'0'`
    - If branching logic is `[var] = 0`, field will always be visible until `[var]` has a value not equal to `'0'`
  - What type coercion goes on behind the scenes is a mystery...
- `<`, `>`, `<=`, and `>=`
  - _Do not_ quote numeric values

### Calculations

- Summation of variables
  - `[var_1] + [var_2] + ... + [var_n]` will not ignore blanks
  - `sum([var_1], [var_2], ..., [var_n])` will ignore blanks
  - Choose the appropriate one
    - First one by default
    - If expecting blanks, second one
  - For simple surveys where all fields are required, there is no difference
- `datediff()`
  - Signature: `datediff([date1], [date2], "units", "date format", Return Signed Value)`
  - Calculation is `[date2] - [date1]`, results returned in the unit specified
  - _Always return signed values_
    - _Especially_ when using `datediff("today", [date2], 'd', true)`, where `[date2]` is in the future
    - May not be necessary if `[date2]` is _always_ greater (or lesser) than `[date1]`
  - "today"
    - Avoid using it if possible
    - If using it, avoid storing values that depend on calculations involving it
    - If storing values that depend on it... haiz... [be prepared](https://www.youtube.com/watch?v=zPUe7O3ODHQ&t=138s) that the values will be inaccurate
- Giving Rule H a break
  - Round off all values with decimal places
  - How many decimal places? Someone should know about the [uncertainty of the measurements](https://www.youtube.com/watch?v=GtOGurrUPmQ&t=280s)
