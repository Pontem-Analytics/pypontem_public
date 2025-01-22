# PyPontem Release Documentation

PyPontem is a one-stop python package for flow-assurance workflows

Authors:
- Afsa Umutoniwase
- Kwizera Erneste
- Jayanth Nair

## Description of functionality

- tpl.tplParser
    - Detailed functionality described in [docs](./docs/tplparser.md)
    - Integrated with xlwings for Excel use as described [here](./docs/xlwings_guide.md)


## Release Notes

- 0.1.0
    - First release with tplParser and xlwings integration
- 0.1.1
    - First patch which address the following issues:
        - [Time units not shown in output](https://github.com/Pontem-Analytics/PyPontem/issues/8)
        - [Unit formatting fixed in trend output](https://github.com/Pontem-Analytics/PyPontem/issues/9)
        - [Wrong trend values extracted in cases with multiple PVT files](https://github.com/Pontem-Analytics/PyPontem/issues/10)
        - [Metadata not shown in cases with multiple PVT files](https://github.com/Pontem-Analytics/PyPontem/issues/11)
        - [Not recognizing an annulus branch](https://github.com/Pontem-Analytics/PyPontem/issues/14)
        - [Branch profiles not returning in Excel](https://github.com/Pontem-Analytics/PyPontem/issues/15)
- 0.2
    - Major update which brings the following functionalities (in both Python API and Excel add in)
        - Internal unit conversions
        - Batch parsing
        - Averaging over time units
        - Input matrix specification
    - Fixed the following issues/added enhancements:
        - [Branch profile function not working in xlwings](https://github.com/Pontem-Analytics/PyPontem/issues/15)
        - [Global variables not working in Excel](https://github.com/Pontem-Analytics/PyPontem/issues/17)
        - [search_catalog with wrong variable](https://github.com/Pontem-Analytics/PyPontem/issues/20)
        - [Variables in lowercase and uppercase letters](https://github.com/Pontem-Analytics/PyPontem/issues/21)
        - [Ability to select values (extract_trends)](https://github.com/Pontem-Analytics/PyPontem/issues/23)
        - [Compute the average and the n value](https://github.com/Pontem-Analytics/PyPontem/issues/25)
        - [Branch variable and apostrophe](https://github.com/Pontem-Analytics/PyPontem/issues/18)
        - [Average function calculation for last n hours](https://github.com/Pontem-Analytics/PyPontem/issues/13)
        - [Custom unit selection](https://github.com/Pontem-Analytics/PyPontem/issues/5)
        - [Branch profiles not returning in Excel](https://github.com/Pontem-Analytics/PyPontem/issues/15)

