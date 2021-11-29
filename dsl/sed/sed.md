SED
===

# deleting trailing new line character
Sed will not work, use `tr -d '\n'`

# the use of regex

```
echo ' convolve_5x5_1_sse@Base 0~20170511-gae1a805' | sed -e 's/^ \(.*\)sse\(.*\)/ (optional)\1sse\2/g'

sed -e 's/.*keyword.*/__&__/g'
```
