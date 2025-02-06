<img style="float:right;" src="https://cdn.prod.website-files.com/645a93c524f9bd7ace372f1b/646ba830c8f56fa29664d1d7_logo.svg" alt="Pontem Analytics Logo" width="100" />


# Welcome to pypontem

![GitHub release](https://img.shields.io/pypi/v/pypontem)
![License](https://img.shields.io/badge/license-MIT-green)
![Python Version](https://img.shields.io/badge/python-3.12.3-blue)

**pypontem** is a Python-based library designed for postprocessing simulation outputs generated by **OLGA**, a leading transient multiphase flow simulator. It helps **flow assurance engineers** efficiently extract, organize, and analyze simulation data.

## Table of Contents
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [Authors](#authors)
- [Further Resources](#further-resources)
- [Contributing](#contributing)
- [License](#license)
- [Contact & Support](#contact--support)

## Key Features
- **Metadata Extraction** – Retrieve simulation metadata (e.g., version, title, author).
- **Branch Analysis** – Identify branch names and extract elevation profiles.
- **Variable Search** – Search variable catalogs based on name, location, or pipeline section.
- **Trend Data Extraction** – Extract time-series data from **TPL** files.
- **Profile Data Extraction** – Extract spatial profile data from **PPL** files.
- **Unit Conversion** – Seamless and robust handling of unit transformations.

## Installation
pypontem requires **Python 3.12.3**. Follow these steps to install:

```sh
# Create a new Conda environment
conda create -n pypontem_env python=3.12.3 jupyter 

# Activate the environment
conda activate pypontem_env

# Install the package
pip install pypontem
```

## Usage Example
Once installed, you can start using **pypontem** as follows:

```python
from pypontem.tpl.tplparser import tplParser

# Load a sample OLGA simulation file
tpl = tplParser(r'example_tpl.tpl')

# Extract metadata from a tpl file
metadata = tpl.metadata
print(metadata)
```

For a detailed walkthrough, check the **[official documentation](http://www.pypontem.pontemanalytics.com/)**.

## Contributing
We welcome contributions! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Submit a pull request for review.


## Authors
- **Pontem Analytics**

## Further Resources
- 📚 **[Official Documentation](http://www.pypontem.pontemanalytics.com/)** – Learn how to use pypontem effectively.
- 💻 **[GitHub Repository](https://github.com/Pontem-Analytics/pypontem_public)** – Explore the source code, contribute, or report issues.

## License
This project is licensed under the **MIT License**.

## Contact & Support
For support, feature requests, or bug reports, open an issue in the **[GitHub repository](https://github.com/Pontem-Analytics/pypontem_public/issues)** 

