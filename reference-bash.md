## Get source directory

```bash
# https://stackoverflow.com/a/246128
WD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" &> /dev/null && pwd)"

WD="$(realpath "${BASH_SOURCE%/*}/")"
```

## Read file line-by-line

```bash
# http://mywiki.wooledge.org/BashFAQ/001
while IFS= read -r subjid <&9; do
    # Do stuff...
done 9< "${INPUT_FILE}"
```
