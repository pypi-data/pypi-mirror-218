# colortools
Python package for common color conversions and operations

[![PyPI - Version](https://img.shields.io/pypi/v/colortools-lentolen.svg)](https://pypi.org/project/colortools-lentolen)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colortools-lentolen.svg)](https://pypi.org/project/colortools-lentolen)

-----

**Table of Contents**

- [Description](#description)
- [Features](#features)
- [Quickstart](#quickstart)
- [Documentation](#documentation)
- [License](#license)

## Description
Python package for conversions between common color representations like RGB and HEX and color comparisons using CIE formulas.

## Features
### Conversion between common color representations
- RGB
- HEX
- CMYK
- HSL
- HSV
- LAB
- XYZ
- Color Name
### Color difference calculation (Delta E)
> measure of the perceptual difference between two colors
- Delta E (ΔE) CIE76 Formula
- Delta E (ΔE) CIE94 Formula
- Delta E (ΔE) CIEDE2000 Formula

## Quickstart
### Installation 
To install from PyPI with pip:

```console
$ python -m pip install colortools-lentolen
```

### Example usage: 
Using colortools in a Python script to calculate the CIEDE200 difference between two hex colors.
```python
from colortools import color_utils
color1 = color_utils.hex_to_rgb("#ddf4ee")
color2 = color_utils.hex_to_rgb("#88bfb1")
deltaE = color_utils.ciede2000_rgb(color1, color2)
```

## Documentation
all color models are represented as tuples except hex codes: e.g: (255,255,255)
### color conversion:
syntax example: 
```python
colortools.color_utils.hex_to_rgb(hex)
```
supported color models: rgb, hex, cmyk, hsl, hsv, lab, xyz, colorname
> There are multiple color naming standards availabe: html (standard), html-ger, meodai, x11, [color-meanings.com](https://color-meanings.com).

This is how you can for example use the [meodai](https://github.com/meodai/color-names) GitHub color name collection:
```python
colortools.color_utils.hex_to_colorname("#ffffff", "meodai")
```

### color difference: 
CIE functions to calculate the Delta E difference between to colors (perceptual difference).

- ciede2000(lab1, lab2)
- ciede2000_rgb(rgb1, rgb2)
- cie76(lab1, lab2)
- cie76_rgb(rgb1, rgb2)
- cie94(lab1, lab2)
- cie94_rgb(rgb1, rgb2)

returns Delta E as float

## License

`colortools` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
