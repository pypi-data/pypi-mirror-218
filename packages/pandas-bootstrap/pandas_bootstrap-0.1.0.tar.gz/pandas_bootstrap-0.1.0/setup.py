# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bootstrap']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pandas>=1.0.0']

setup_kwargs = {
    'name': 'pandas-bootstrap',
    'version': '0.1.0',
    'description': 'Bootstrapping with Pandas made easy',
    'long_description': "# Pandas Bootstrap\n\nBootrapping with Pandas made easy.\n\n## Installation\n\n```bash\npip install pandas-bootstrap\n```\n\n## Usage\n\nThe module is very easy to use. \n\n1. `import bootstrap`\n2. define statistic function: `def some_func(df: pd.DataFrame | pd.Series):`\n3. get bootstrapped samples: `df.boot.get_samples(bfunc=some_func, B=100)`\n\nBelow is a simple example of bootstrapping the mean of two columns.\n\n```python\nimport pandas as pd\n\nimport bootstrap\n\ndf = pd.DataFrame({\n    'a': [1, 2, 3, 4, 5],\n    'b': [6, 7, 8, 9, 10],\n})\n\ndef mean_of_columns(df):\n    return df.mean(numeric_only=True)\n\nsample_kwargs = dict(random_state=42)\ndf_bootstrap = df.boot.get_samples(bfunc=mean_of_columns, B=5, sample_kwargs=sample_kwargs)\n```\n\nwhich results in:\n\n```text \n          a    b\nsample          \n0       3.0  8.0\n1       2.6  7.6\n2       4.0  9.0\n3       3.2  8.2\n4       3.0  8.0\n```\n\n## Documentation\n\nRead more in the [documentation](https://wd60622.github.io/pandas-bootstrap/)",
    'author': 'Will Dean',
    'author_email': 'wd60622@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
