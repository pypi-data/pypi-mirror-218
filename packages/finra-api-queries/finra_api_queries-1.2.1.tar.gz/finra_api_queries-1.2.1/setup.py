# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finra_api_queries']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'finra-api-queries',
    'version': '1.2.1',
    'description': "An API wrapper for FINRA's Query API",
    'long_description': '# finra_api_queries\n\nFINRA is the Financial Industry Regulatory Authority, which oversees US brokerages and exchanges such as the NYSE and NASDAQ.  They ensure that brokers and dealers in US stock/debt markets are acting according to the laws and rules defined by the Securities and Exchange Commission (SEC) as well as by FINRA.  Their API contains information about historical market activity, such as fixed income market activity, statistics such as the size of trades that major institutional investors make, and over-the-counter (OTC) trading activity.  This information allows regulators as well as the public to understand market trading behavior.\n\nThe finra_api_queries package simplifies the querying of the FINRA Query API including more complex API calls. It also features functions that enable the time series data visualization of fixed income data, summarization of key market breadth data, and keyword filtering for stocks.\n\n## Installation\n\n```bash\n$ pip install finra_api_queries\n```\n\n## How to Use\n\n```bash\n$ from finra_api_queries import finra_api_queries\n```\n\n## Usage\n\n1. Obtain an API key and secret on the FINRA API website.\n2. Input the key and secret using the retrieve_api_token() function to generate the time-limited access token necessary to retrieve data from the API.\n3. Use the various functions to easily extract data sets from the FINRA Query API with a variety of parameters, visualize time series data, as well as filter and aggregate data in pandas data frames and Seaborn plots.\n4. Use API to glean time series-related and aggregated insights about fixed income activity and trading block activity.\n\nThis package features the following 7 functions:\n\n* retrieve_api_token\n* show_filterable_columns\n* retrieve_dataset\n* filter_market_participant\n* summarize_trading_breadth\n* visualize_market_sentiment\n* generate_market_participant_summary\n\n#### readthedocs Package Documentation\nhttps://finra-api-queries.readthedocs.io/en/latest/\n\n#### Test PyPi Link\nhttps://test.pypi.org/project/finra-api-queries/\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`finra_api_queries` was created by Cindy Chen. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`finra_api_queries` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Cindy Chen',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chencindyj/finra_api_queries',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
