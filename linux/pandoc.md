pandoc
===

## convert your markdown file to pdf directly

```
pandoc a.md -V fontfamily=times -V geometry=margin=1in -o a.pdf
```

## Include Chinese character in generated PDF document

```
pandoc -D latex > template.tex

add this at line 2:
+\usepackage{CJKutf8}

add this after \begin{document}:
+\begin{CJK}{UTF8}{gkai}

add this before \end{document}:
+\end{CJK}
```
