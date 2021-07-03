# REDCap Cheatsheet

> WIP

Random points:

- Avoid (not ban) `<p>`, use `<div>` instead for blocks or `<span>`/`<font>` for sentences
  - `<p>` has been observed to have inconsistent font sizes in certain cases
  - There will be situations where using `<p>` is appropriate
- When using embedded field tables, apply 'majority' style to entire table
  - Reduces amount of code to maintain for individual rows/cells
  - Neater
  - If you don't understand this point, ignore until you have to maintain a moderately-sized table with embedded fields
- Use `<strong>` and `<em>`
  - Not too sure if there are any advantages over `<b>` and `<i>`...
- For testing equal (=) or not equal (<>), surround value with quotes (')
  - `[var] = 0` field will be revealed if no option is selected, but `[var] = '0'` will not if '0' is not selected
- For testing other inequalities (<, <=, >, >=), _do not_ surround value with quotes
- Using `<... style="margin: 0 0 0 10%;">` for indentations for now...
  - _It there a better way?_
- Avoid inserting line breaks &mdash; Use `<br />` instead
  - If not, lines in data dictionary will not correspond with number of fields
- Keep an eye on special characters, _e.g._:
  - `&mdash;`: &mdash;
  - `&ge;`: &ge;
- ...
