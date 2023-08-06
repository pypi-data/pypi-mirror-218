# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sortedness', 'sortedness.evaluation', 'sortedness.wtau']

package_data = \
{'': ['*']}

install_requires = \
['lange>=1.230203.1,<2.0.0', 'pathos>=0.3.0,<0.4.0']

extras_require = \
{':python_version >= "3.8" and python_version < "3.11"': ['scipy>=1.10.1,<2.0.0']}

setup_kwargs = {
    'name': 'sortedness',
    'version': '0.230710.0',
    'description': 'Measures of projection quality',
    'long_description': '![test](https://github.com/sortedness/sortedness/workflows/test/badge.svg)\n[![codecov](https://codecov.io/gh/sortedness/sortedness/branch/main/graph/badge.svg)](https://codecov.io/gh/sortedness/sortedness)\n<a href="https://pypi.org/project/sortedness">\n<img src="https://img.shields.io/github/v/release/sortedness/sortedness?display_name=tag&sort=semver&color=blue" alt="github">\n</a>\n![Python version](https://img.shields.io/badge/python-3.8+-blue.svg)\n[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n<!-- [![arXiv](https://img.shields.io/badge/arXiv-2109.06028-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2109.06028) --->\n[![API documentation](https://img.shields.io/badge/doc-API%20%28auto%29-a0a0a0.svg)](https://sortedness.github.io/sortedness)\n[![DOI](https://zenodo.org/badge/513273889.svg)](https://zenodo.org/badge/latestdoi/513273889)\n[![Downloads](https://static.pepy.tech/badge/sortedness)](https://pepy.tech/project/sortedness)\n\n\n# sortedness\n\n`sortedness` is a measure of quality of data transformation, often dimensionality reduction.\nIt is less sensitive to irrelevant distortions and return values in a more meaningful interval than Kruskal stress formula I.\n<br>This [Python library](https://pypi.org/project/sortedness) / [code](https://github.com/sortedness/sortedness) provides a reference implementation for the functions presented [here (paper unavailable until publication)](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Nonparametric+Dimensionality+Reduction+Quality+Assessment+based+on+Sortedness+of+Unrestricted+Neighborhood&btnG=).\n\n## Overview\nLocal variants return a value for each provided point. The global variant returns a single value for all points.\nAny local variant can be used as a global measure by taking the mean value.\n\nLocal variants: `sortedness(X, X_)`, `pwsortedness(X, X_)`, `rsortedness(X, X_)`.\n\nGlobal variant: `global_sortedness(X, X_)`.\n\n## Python installation\n### from package through pip\n```bash\n# Set up a virtualenv. \npython3 -m venv venv\nsource venv/bin/activate\n\n# Install from PyPI\npip install -U sortedness\n```\n\n### from source\n```bash\ngit clone https://github.com/sortedness/sortedness\ncd sortedness\npoetry install\n```\n\n\n### Examples\n\n**Sortedness**\n<details>\n<p>\n\n```python3\n\nimport numpy as np\nfrom numpy.random import permutation\nfrom sklearn.decomposition import PCA\n\nfrom sortedness import sortedness\n\n# Some synthetic data.\nmean = (1, 2)\ncov = np.eye(2)\nrng = np.random.default_rng(seed=0)\noriginal = rng.multivariate_normal(mean, cov, size=12)\nprojected2 = PCA(n_components=2).fit_transform(original)\nprojected1 = PCA(n_components=1).fit_transform(original)\nnp.random.seed(0)\nprojectedrnd = permutation(original)\n\n# Print `min`, `mean`, and `max` values.\ns = sortedness(original, original)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n1.0 1.0 1.0\n"""\n```\n\n```python3\n\ns = sortedness(original, projected2)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n1.0 1.0 1.0\n"""\n```\n\n```python3\n\ns = sortedness(original, projected1)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n0.432937128932 0.7813889452999166 0.944810120534\n"""\n```\n\n```python3\n\ns = sortedness(original, projectedrnd)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n-0.578096068617 -0.06328160775358334 0.396112816715\n"""\n```\n\n\n</p>\n</details>\n\n**Pairwise sortedness**\n<details>\n<p>\n\n```python3\n\nimport numpy as np\nfrom numpy.random import permutation\nfrom sklearn.decomposition import PCA\n\nfrom sortedness import pwsortedness\n\n# Some synthetic data.\nmean = (1, 2)\ncov = np.eye(2)\nrng = np.random.default_rng(seed=0)\noriginal = rng.multivariate_normal(mean, cov, size=12)\nprojected2 = PCA(n_components=2).fit_transform(original)\nprojected1 = PCA(n_components=1).fit_transform(original)\nnp.random.seed(0)\nprojectedrnd = permutation(original)\n\n# Print `min`, `mean`, and `max` values.\ns = pwsortedness(original, original)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n1.0 1.0 1.0\n"""\n```\n\n```python3\n\ns = pwsortedness(original, projected2)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n1.0 1.0 1.0\n"""\n```\n\n```python3\n\ns = pwsortedness(original, projected1)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n0.730078995423 0.7744573488776667 0.837310352695\n"""\n```\n\n```python3\n\ns = pwsortedness(original, projectedrnd)\nprint(min(s), sum(s) / len(s), max(s))\n"""\n-0.198780473657 -0.0645984203715 0.147224384381\n"""\n```\n\n\n</p>\n</details>\n\n**Sortedness**\n<details>\n<p>\n\n```python3\n\nimport numpy as np\nfrom numpy.random import permutation\nfrom sklearn.decomposition import PCA\n\nfrom sortedness import global_pwsortedness\n\n# Some synthetic data.\nmean = (1, 2)\ncov = np.eye(2)\nrng = np.random.default_rng(seed=0)\noriginal = rng.multivariate_normal(mean, cov, size=12)\nprojected2 = PCA(n_components=2).fit_transform(original)\nprojected1 = PCA(n_components=1).fit_transform(original)\nnp.random.seed(0)\nprojectedrnd = permutation(original)\n\n# Print measurement result and p-value.\ns = global_pwsortedness(original, original)\nprint(list(s))\n"""\n[1.0, 3.6741408919675163e-93]\n"""\n```\n\n```python3\n\ns = global_pwsortedness(original, projected2)\nprint(list(s))\n"""\n[1.0, 3.6741408919675163e-93]\n"""\n```\n\n```python3\n\ns = global_pwsortedness(original, projected1)\nprint(list(s))\n"""\n[0.7715617715617715, 5.240847664048334e-20]\n"""\n```\n\n```python3\n\ns = global_pwsortedness(original, projectedrnd)\nprint(list(s))\n"""\n[-0.06107226107226107, 0.46847188611226276]\n"""\n```\n\n\n</p>\n</details>\n\n\n** Copyright (c) 2023. Davi Pereira dos Santos and Tacito Neves**\n\n\n\n\n\n## Grants\n',
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
