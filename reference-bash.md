## Get source directory

```bash
# https://stackoverflow.com/a/246128

get_wd() {
    echo "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
}
```
