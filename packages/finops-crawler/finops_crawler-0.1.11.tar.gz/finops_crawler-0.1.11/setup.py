# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['finops_crawler',
 'finops_crawler.aws',
 'finops_crawler.azure',
 'finops_crawler.openai']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.26.156', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'finops-crawler',
    'version': '0.1.11',
    'description': "It's a package for importing cost and usage data from various cloud platforms and SaaS tools",
    'long_description': '# finops-crawler\n\nThis project is active. Development is ongoing, and contributions are welcome (see below).\n\n## Basic Usage\n\nThis package is designed to fetch cost/usage data from various platforms (Azure, AWS, OpenAI, and more to follow).\n\n**The main principle is to have as simple an approach as possible along with the absolute minimum set of permissions required**. Thus, the quickstart part of each guide is presented as CLI commands.\n\nThe result, for now, is a Python variable as returned by the API or SDK.\n\n### Platform-specific documentation\n\nEach platform is different and has a separate guide on how to set up an entity with minimum permissions to read the cost data. Specific code snippets to get started are included.\n\n- [Azure](https://github.com/finops-fitness-club/finops-crawler/tree/main/src/finops_crawler/azure)\n- [AWS](https://github.com/finops-fitness-club/finops-crawler/tree/main/src/finops_crawler/aws)\n- [OpenAI](https://github.com/finops-fitness-club/finops-crawler/tree/main/src/finops_crawler/openai)\n\n\n### Overview of the flow\n\n1. Set up a user (technical user/service principal) for querying the data\n2. Set up permissions for that user\n3. Set environment variables to be used by the package\n4. Use the package\n\n### Resulting data\n\nEach platform has its own format. Also, the same date range might produce different results depending on the platform. Some might include the last day, some may not.\n\nThere is an open data specification being developed by FinOps Foundation ([FOCUS](https://focus.finops.org/)). At this point, it\'s still very new and not adopted by the industry. We will keep a close eye on it and support it as soon as feasible.\n\n*Note*: querying long time periods might trigger paginated results. AWS and Azure handle it correctly. OpenAI does not have paginated results as it\'s an undocumented API and it also has not existed yet for a very long time.\n\n### Plans\n\nIncrease breath by expanding to various other tools and platforms (Databricks, GCP, etc.)\n\nIncrease depth by implementing `save_to_postgres` or similar functionality to actually store it.\n\n### Contributing\n\nGot ideas for improvements? We\'d love your input!\n\n1. Fork and clone this repository.\n2. Optionally, choose an issue labeled as "help wanted" or "good first issue".\n3. Submit a pull request with your changes and a clear description.\n\nRemember, all contributions from bug fixes to documentation updates are greatly appreciated!\n\nEnjoy :)\n\nEmail: finops.fitness.club@gmail.com\n',
    'author': 'Lauri Koobas',
    'author_email': 'laurikoobas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
