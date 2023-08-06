zen_han_converter
===

# Description

This is a tool for converting full-width and half-width characters to each other, implemented only with Python's standard modules.

# Target characters

- Latin alphabet
- Arabic numerals
- ASCII symbols
- Space

# Installaction

```
pip install zen_han_converter
```

# Usage

```
>>> from zen_han_converter import ZenToHan
>>> zen_to_han = ZenToHan()
>>> zen_to_han.convert('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ')
'abcdefghijklmnopqrstuvwxyz'
```
