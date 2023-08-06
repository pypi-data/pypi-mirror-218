# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codeboxapi']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'codeboxapi',
    'version': '0.0.1',
    'description': 'CodeBox is the simplest cloud infrastructure for your LLM Apps and Services.',
    'long_description': '# CodeBox\n\nCodeBox is the simplest cloud infrastructure for your LLM Apps and Services.\nIt allows you to run python code in an isolated/sandboxed environment.\nAdditionally, it provides simple fileIO (and vector database support coming soon).\n\n## Installation\n\nYou can install CodeBox with pip:\n\n```bash\npip install codebox\n```\n\n## Usage\n\n```python\nimport codebox as cb\n\ncb.set_api_key("your-api-key")\n# or put your api key inside the .env file\n# CODEBOX_API_KEY=your-api-key\n\n# create and startup\ncodebox = CodeBox()\ncodebox.start()\n\n# check if it\'s running\nprint(codebox.status() == "running")\n\n# run some code\nresult = codebox.run("print(\'Hello, World!\')")\n\n# print the result\nprint(result)\n```\n\n## Contributing\n\nFeel free to contribute to this project.\nYou can open an issue or submit a pull request.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n## Contact\n\nYou can contact me at [pleurae-berets.0u@icloud.com](mailto:pleurae-berets.0u@icloud.com)\n',
    'author': 'Shroominic',
    'author_email': 'pleurae-berets.0u@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
