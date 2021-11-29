% title
% author(s) (separated by semicolons)
% date

Pandoc Example Markdown
===

Reference [link](http://pages.tzengyuxio.me/pandoc/)

You can compile this document with the following command:

```
pandoc -o my.pdf my.markdown
```

Here is a list of useful options:

```
--number-sections
-V fontfamily=times
-V fontsize=11pt
-V geometry=margin=1in
-V classoption=twocolumn
```

Reference: `man pandoc`

Second Tier Title
---

Sections with `.unnumbered` flag will not be numbered even if the flag
`--number-sections` was specified.

### Level 3 title without number {.unnumbered}

### Title level higher than 3 is useless in Latex Mode

> This is a example of quotation block.
> Quotations..

Part Two {#labelpart2}
===

## Code

Example of Code block

``` {.c}
int
main(void) {
    printf("Hello!\n");
    return 0;
}
```

Python Code
``` {.python}
import sys
if __name__=='__main__':
    print(sys.argv[0], ':', 'hello!')
```

Lua Code
```lua
require 'json'
print('hello lua!')
```

## List

* item1

* item2

    + Nested list item

* Numbered list is also available

    1. item A

    2. item B

---

Split line.

## Table

First example

  Right     Left     Center     Default
-------     ------ ----------   -------
     12     12        12            12
    123     123       123          123
      1     1          1             1

Text alignment

-------     ------ ----------   -------
     12     12        12             12
    123     123       123           123
      1     1          1              1
-------     ------ ----------   -------

Grid table


+---------------+---------------+--------------------+
| Fruit         | Price         | Advantages         |
+===============+===============+====================+
| Bananas       | $1.34         | - built-in wrapper |
|               |               | - bright color     |
+---------------+---------------+--------------------+
| Oranges       | $2.10         | - cures scurvy     |
|               |               | - tasty            |
+---------------+---------------+--------------------+

## Math

$e^{iw} = \cos(w) + i\sin(w)$

$$ e=mc^2 $$

## Links

[example link to github](https://github.com)

[Document inner link](#labelpart2)

## Picture

```markdown
![your caption](path/to/your/picture.png)
```

## Footnote

Pandoc's markdown supports footnotes.^[This is inline footnote.]
