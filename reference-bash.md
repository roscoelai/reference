## Get source directory

https://stackoverflow.com/a/246128
```bash
readonly WD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" &> /dev/null && pwd)"
```

https://mywiki.wooledge.org/BashFAQ/028
```bash
# Requires `realpath`, works OK with `./script.sh` but not `bash script.sh`, so the one above might be better
readonly WD="$(realpath "${BASH_SOURCE%/*}/")"
```

## Display git branch name on `PS1` manually

https://coderwall.com/p/fasnya/add-git-branch-name-to-bash-prompt
```bash
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

# E.g. usage:
PS1='${debian_chroot:+($debian_chroot)}\[\033[92m\]\u@\h\[\033[0m\]:\[\033[93m\]\w\[\033[96m\]$(parse_git_branch)\[\033[0m\] \$ '
```

## Queue

https://unix.stackexchange.com/a/436713
```bash
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

## Adding SSH key to `ssh-agent`

https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/<private key file>
```

## Read file line-by-line

http://mywiki.wooledge.org/BashFAQ/001
```bash
while IFS= read -r subjid <&9; do
    # Do stuff...
done 9< "${INPUT_FILE}"
```
