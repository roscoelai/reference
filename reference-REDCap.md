# REDCap Cheatsheet

> WIP

Random points:

- Avoid (not ban) `<p>`, use `<div>` instead for blocks or `<span>`/`<font>` for sentences
  - `<p>` has been observed to have inconsistent font sizes in certain cases
- When using embedded field tables, apply 'majority' style to entire table
  - Reduces amount of code to maintain for individual rows/cells
  - Neater
- Use `<strong>` and `<em>`
- For testing equal (=) or not equal (<>), surround value with quotes (')
  - `[var] = 0` field will be revealed if no option is selected, but `[var] = '0'` will not if '0' is not selected
- For testing other inequalities (<, <=, >, >=), _do not_ surround value with quotes
- Using `<... style="margin: 0 0 0 10%;">` for indentations for now...
- ...
