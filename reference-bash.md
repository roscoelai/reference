## Get source directory

```bash
# https://stackoverflow.com/a/246128
WD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" &> /dev/null && pwd)"

# https://mywiki.wooledge.org/BashFAQ/028
WD="$(realpath "${BASH_SOURCE%/*}/")"
```

## Semaphore

```bash
# https://unix.stackexchange.com/a/436713
N=20
for i in {1..100}; do
    (
        # Do stuff...
    ) &
    
    (( "$(jobs -pr | wc -l)" >= "$N" )) && wait -n
done
wait
```

## Read file line-by-line

```bash
# http://mywiki.wooledge.org/BashFAQ/001
while IFS= read -r subjid <&9; do
    # Do stuff...
done 9< "${INPUT_FILE}"
```
