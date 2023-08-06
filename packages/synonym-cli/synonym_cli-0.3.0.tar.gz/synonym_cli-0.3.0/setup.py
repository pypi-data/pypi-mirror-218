# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['synonym_cli']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'beautifulsoup4>=4.12.2,<5.0.0',
 'importlib-metadata>=6.7.0,<7.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=13.4.2,<14.0.0']

entry_points = \
{'console_scripts': ['syn = synonym_cli.__main__:cli']}

setup_kwargs = {
    'name': 'synonym-cli',
    'version': '0.3.0',
    'description': '🌾Get synonyms and antonyms of words from Thesaurus.com and other sources in your terminal, with rich output.',
    'long_description': '<div align="center"><img src="https://user-images.githubusercontent.com/16024979/162848437-8da9d5d4-a234-44d3-94d8-048f92b015a6.png" alt="syn"><a alt="Github" href="https://github.com/agmmnn/syn"><img alt="GitHub release" src="https://img.shields.io/github/v/release/agmmnn/syn"></a> <a href="https://pypi.org/project/synonym-cli/"><img alt="PyPI" src="https://img.shields.io/pypi/v/synonym-cli"></a> <a href="https://pepy.tech/project/synonym-cli"><img alt="PyPI" src="https://pepy.tech/badge/synonym-cli"></a></div>\n\n# 🌾 syn\n\nGet synonyms and antonyms of words from [Thesaurus.com](https://www.thesaurus.com/), [Datamuse API](https://www.datamuse.com/api/) and [AlterVista](https://thesaurus.altervista.org/) in your terminal, with [rich](https://github.com/Textualize/rich) output.\n\n# Install:\n\n```\npip install synonym-cli\n```\n\n## Usage:\n\n```\nsyn <word>\n```\n\n### Explore Mode\n\nReturns more particular results about the given word. Uses [Datamuse API](https://www.datamuse.com/api/).\n\n> for Web UI: https://wordwhisper.vercel.app\n\n`$ syn dominant -d`\n![](https://user-images.githubusercontent.com/16024979/209148078-309ba28e-dc59-459f-9035-b6d3d75b710f.png)\n\n### Other Languages\n\nFor other languages you can use `--lang`, `-l` command. To use this feature, you need to get an api key from [here](https://thesaurus.altervista.org/openapi).\n\n`$ syn -l fr belle`\n![](https://user-images.githubusercontent.com/16024979/209144768-0cde6709-65d9-4142-9eae-bb4bc38e4a13.png)\n\n`$ syn -l ru фраза`\n![](https://user-images.githubusercontent.com/16024979/209144765-abca9b54-5495-4295-98f7-15acdbde7623.png)\n\n> AlterVista\'s Thesaurus API supports the following languages:\n\n> Czech: `cs`, Danish: `da`, English (US): `en`, French: `fr`, German (Germany): `de`, German (Switzerland): `de`, Greek: `el`, Hungarian: `hu`, Italian: `it`, Norwegian: `no`, Polish: `pl`, Portuguese: `pt`, Romanian: `ro`, Russian: `ru`, Slovak: `sk`, Spanish: `es`.\n\n### Set Default Language\n\nYou can set the default language with the `--setlang <lang_code>` argument, so you don\'t have to give the `-l` argument every time.\n\n```\n$ syn --setlang fr\n> default language is: fr\n$ syn belle\n> ...\n```\n\n## Arguments\n\n```\n  -h, --help      show this help message and exit\n  -p, --plain     returns plain text output\n  -l, --lang      <language>\n  --setkey        set apikey for altervista api\n  --setlang       set default language (currently default is \'en\')\n  --show          show settings file\n  -v, --version   show program\'s version number and exit\n```\n\n# Contrubuting\n\nContributions are welcome. If you want to contribute to this list send a pull request or just open a new issue.\n',
    'author': 'agmmnn',
    'author_email': 'agmmnn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/agmmnn/syn',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
