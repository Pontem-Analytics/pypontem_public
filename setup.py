from setuptools import find_packages, find_namespace_packages, setup
import io
import os


# Package Metadata
NAME = "pypontem"
DESCRIPTION = "The one-stop python toolkit for Flow Assurance workflows"
URL = "https://github.com/Pontem-Analytics/pypontem_public/tree/main"

REQUIRES_PYTHON = "==3.12.3"
VERSION = "1.0.8"
REQUIRED = ["pandas==2.2.0", "pint==0.23", "PyYAML==6.0.2"]
# EXTRAS = {""}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    # author=AUTHOR,
    # author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        where="src", exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    # packages=["pypontem", "pypontem/tpl", "pypontem/utils"],
    # package_dir={"pypontem": "src/pypontem"},
    package_dir={"": "src"},
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    # extras_require=EXTRAS,
    include_package_data=True,
    package_data={'': ['utils/*.yaml'],},

    # license='MIT',
    # classifiers=[
    #     # Trove classifiers
    #     # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: Implementation :: CPython',
    #     'Programming Language :: Python :: Implementation :: PyPy'
    # ],
    # $ setup.py publish support.
    # cmdclass={
    #     "upload": UploadCommand,
    # },
)
