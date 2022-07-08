## Get source directory

```bash
# https://stackoverflow.com/a/246128
readonly WD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" &> /dev/null && pwd)"

# https://mywiki.wooledge.org/BashFAQ/028
# Works OK with `./script.sh`, but not `bash script.sh`, so prefer the above
readonly WD="$(realpath "${BASH_SOURCE%/*}/")"
```

## Queue

```bash
# https://unix.stackexchange.com/a/436713
readonly N=20
for i in {1..100}; do
    (
        # Do stuff...
    ) &
    
    (( "$(jobs -pr | wc -l)" >= "$N" )) && wait -n
done
wait
```

## `find` to array

```bash
mapfile -d '' arr < <( find \
    "$path" \
    -type d \
    -not \( -path "*glob1*" -prune \) \
    \( -path "*glob2*" -o "*glob3*" \) \
    -iregex "regex1" \
    -printf "%P/\0" )
```

## Output array text

```bash
printf "%s\n" "${arr[@]}"
printf "%s\0" "${arr[@]}"
```

## Array to `rsync`

```bash
rsync --verbose --archive --recursive --files-from=<( printf "%s\0" "${arr[@]}" ) --from0 -- "$src" "$dest"
```

## Print repeated strings

```bash
printf "1%.s " {1..20}
```

## Read file line-by-line

```bash
# http://mywiki.wooledge.org/BashFAQ/001
while IFS= read -r subjid <&9; do
    # Do stuff...
done 9< "${INPUT_FILE}"
```
