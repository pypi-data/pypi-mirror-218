# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfairdatatools', 'pyfairdatatools.tests']

package_data = \
{'': ['*'],
 'pyfairdatatools': ['assets/*',
                     'schemas/*',
                     'templates/*',
                     'templates/high-level-dataset-structure/*',
                     'templates/high-level-dataset-structure/activity_monitor/*',
                     'templates/high-level-dataset-structure/best_corrected_visual_acuity/*']}

install_requires = \
['art>=5.9,<6.0',
 'click',
 'dicttoxml>=1.7.16,<2.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'minilog',
 'pymdown-extensions>=10.0.1,<11.0.0',
 'types-requests>=2.30.0.0,<3.0.0.0',
 'urllib3<2.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['pyfairdatatools = pyfairdatatools.cli:main']}

setup_kwargs = {
    'name': 'pyfairdatatools',
    'version': '0.1.1',
    'description': 'Tools for AI-READI',
    'long_description': '<div align="center">\n\n<img src="https://freesvg.org/img/1653682897science-svgrepo-com.png" alt="logo" width="200" height="auto" />\n\n<br />\n\n<h1>pyfairdatatools</h1>\n\n<p>\nPython package for the FAIR tools of fairhub.io\n</p>\n\n<br />\n\n<p>\n  <a href="https://github.com/AI-READI/pyfairdatatools/graphs/contributors">\n    <img src="https://img.shields.io/github/contributors/AI-READI/pyfairdatatools.svg?style=flat-square" alt="contributors" />\n  </a>\n  <a href="https://github.com/AI-READI/pyfairdatatools/stargazers">\n    <img src="https://img.shields.io/github/stars/AI-READI/pyfairdatatools.svg?style=flat-square" alt="stars" />\n  </a>\n  <a href="https://github.com/AI-READI/pyfairdatatools/issues/">\n    <img src="https://img.shields.io/github/issues/AI-READI/pyfairdatatools.svg?style=flat-square" alt="open issues" />\n  </a>\n  <a href="https://github.com/AI-READI/pyfairdatatools/blob/main/LICENSE">\n    <img src="https://img.shields.io/github/license/AI-READI/pyfairdatatools.svg?style=flat-square" alt="license" />\n  </a>\n  <a href="https://fairdataihub.org/fairshare">\n    <img src="https://raw.githubusercontent.com/fairdataihub/FAIRshare/main/badge.svg" alt="Curated with FAIRshare" />\n  </a>\n</p>\n<p>\n  <a href="https://github.com/AI-READI/pyfairdatatools/actions">\n    <img src="https://img.shields.io/github/actions/workflow/status/AI-READI/pyfairdatatools/main.yml?branch=main&label=linux" alt="Unix Build Status" />\n  </a>\n  <a href="https://ci.appveyor.com/project/AI-READI/pyfairdatatools">\n    <img src="https://img.shields.io/appveyor/ci/AI-READI/pyfairdatatools.svg?label=windows" alt="Windows Build Status" />\n  </a>\n  <a href="https://codecov.io/gh/AI-READI/pyfairdatatools">\n    <img src="https://img.shields.io/codecov/c/gh/AI-READI/pyfairdatatools" alt="Coverage Status" />\n  </a>\n  <a href="https://scrutinizer-ci.com/g/AI-READI/pyfairdatatools">\n    <img src="https://img.shields.io/scrutinizer/g/AI-READI/pyfairdatatools.svg" alt="Scrutinizer Code Quality" />\n  </a>\n  <a href="https://pypi.org/project/pyfairdatatools">\n    <img src="https://img.shields.io/pypi/l/pyfairdatatools.svg" alt="PyPI License" />\n  </a>\n  <a href="https://pypi.org/project/pyfairdatatools">\n    <img src="https://img.shields.io/pypi/v/pyfairdatatools.svg" alt="PyPI Version" />\n  </a>\n  <a href="https://pypistats.org/packages/pyfairdatatools">\n    <img src="https://img.shields.io/pypi/dm/pyfairdatatools.svg?color=orange" alt="PyPI Downloads" />\n  </a>\n</p>\n\n<h4>\n    <a href="https://ai-readi.github.io/pyfairdatatools/">Documentation</a>\n  <span> · </span>\n    <a href="https://ai-readi.github.io/pyfairdatatools/about/changelog/">Changelog</a>\n  <span> · </span>\n    <a href="https://github.com/AI-READI/pyfairdatatools/issues/">Report Bug</a>\n  <span> · </span>\n    <a href="#">Request Feature</a>\n  </h4>\n</div>\n\n<br />\n\n---\n\n## Description\n\npyfairdatatools is a Python package that includes functions of fairhub.io for making data FAIR. This consists of a collection of helpful functions for extracting, transforming raw data, generating relevant metadata files and validating the data and metadata files against the FAIR guidelines adopted by the AI-READI project. Beside supporting fairhub.io, our aim is that the package can be used by anyone wanting to make their data FAIR according to the AI-READI FAIR guidelines.\n\n## Getting started\n\n### Prerequisites/Dependencies\n\nYou will need the following installed on your system:\n\n- Python 3.8+\n- [Pip](https://pip.pypa.io/en/stable/)\n- [Poetry](https://poetry.eustace.io/)\n\n### Installing\n\nInstall it directly into an activated virtual environment:\n\n```bash\npip install pyfairdatatools\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```bash\npoetry add pyfairdatatools\n```\n\n### Usage\n\nAfter installation, the package can be imported:\n\n```bash\n$ python\n>>> import pyfairdatatools\n>>> pyfairdatatools.__version__\n```\n\n### Inputs and Outputs\n\nThe input of most functions will be a json format schema (see "Standards followed" sections) that contain data and metadata related information. The outputs of most functions will be standards metadata files, structured data, etc.\n\n## Standards followed\n\nThis software is being developed following the [Software Development Best Practices of the AI-READI Project](https://github.com/AI-READI/software-development-best-practices), which include following the [FAIR-BioRS guidelines](https://github.com/FAIR-BioRS/Guidelines). Amongs other, we are following closely the [PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/).\n\nThe input structure of the function is currently being developed but anticipated to follow existing schemas such as schema.org and bioschemas.org.\n\n## Contributing\n\n<a href="https://github.com/AI-READI/pyfairdatatools/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=AI-READI/pyfairdatatools" />\n</a>\n\nContributions are always welcome!\n\nIf you are interested in reporting/fixing issues and contributing directly to the code base, please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information on what we\'re looking for and how to get started.\n\n## Issues and Feedback\n\nTo report any issues with the software, suggest improvements, or request a new feature, please open a new issue via the [Issues](https://github.com/AI-READI/pyfairdatatools/issues) tab. Provide adequate information (operating system, steps leading to error, screenshots) so we can help you efficiently.\n\n### Setup\n\nIf you would like to update the package, please follow the instructions below.\n\n1. Create a local virtual environment and activate it:\n\n   ```bash\n   python -m venv .venv\n   source .venv/bin/activate\n   ```\n\n   If you are using Anaconda, you can create a virtual environment with:\n\n   ```bash\n   conda create -n pyfairdatatools-env python\n   conda activate pyfairdatatools-env\n   ```\n\n2. Install the dependencies for this package. We use [Poetry](https://poetry.eustace.io/) to manage the dependencies:\n\n   ```bash\n   pip install poetry==1.3.2\n   poetry install\n   ```\n\n   You can also use version 1.2.0 of Poetry, but you will need to run `poetry lock` after installing the dependencies.\n\n3. Add your modifications and run the tests:\n\n   ```bash\n   poetry run pytest\n   ```\n\n   If you need to add new python packages, you can use Poetry to add them:\n\n   ```bash\n    poetry add <package-name>\n   ```\n\n4. Format the code:\n\n   ```bash\n   poe format\n   ```\n\n5. Check the code quality:\n\n   ```bash\n   poetry run flake8 pyfairdatatools tests\n   ```\n\n6. Run the tests and check the code coverage:\n\n   ```bash\n   poe test\n   poe test --cov=pyfairdatatools\n   ```\n\n7. Build the package:\n\n   Update the version number in `pyproject.toml` and `pyfairdatatools/__init__.py` and then run:\n\n   ```text\n   poetry build\n   ```\n\n8. Publish the package:\n\n   ```bash\n   poetry publish\n   ```\n\n   Set your API token for PyPI in your environment variables:\n\n   ```bash\n   poetry config pypi-token.pypi your-api-token\n   ```\n\n## License\n\nThis work is licensed under\n[MIT](https://opensource.org/licenses/mit). See [LICENSE](https://github.com/AI-READI/pyfairdatatools/blob/main/LICENSE) for more information.\n\n<a href="https://aireadi.org" >\n  <img src="https://www.channelfutures.com/files/2017/04/3_0.png" height="30" />\n</a>\n\n## How to cite\n\nIf you are using this package or reusing the source code from this repository for any purpose, please cite:\n\n```text\n    Coming soon...\n```\n\n## Acknowledgements\n\nThis project is funded by the NIH under award number 1OT2OD032644. The content is solely the responsibility of the authors and does not necessarily represent the official views of the NIH.\n\nAdd any other acknowledgements here.\n\n<br />\n\n---\n\n<br />\n\n<div align="center">\n\n<a href="https://aireadi.org">\n  <img src="https://github.com/AI-READI/AI-READI-logo/raw/main/logo/png/option2.png" height="200" />\n</a>\n\n</div>\n',
    'author': 'FAIR Data Innovations Hub',
    'author_email': 'contact@fairdataihub.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pyfairdatatools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
