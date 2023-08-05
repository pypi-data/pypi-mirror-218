# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resource_monitor_scanner']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.2,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'py3nvml>=0.2.7,<0.3.0',
 'seaborn>=0.12,<0.13',
 'streamlit>=1.24.0,<2.0.0']

setup_kwargs = {
    'name': 'resource-monitor-scanner',
    'version': '0.1.0',
    'description': '',
    'long_description': '# resource-monitor-scanner\n\n# Requiremetns\n`pip install -r requirements.txt`\n\n# Running\nrunning the script will log the stats to a csv, if time is not passed it will take 300s (5 min) as default recording duration, if called with negative duration it will be \nrecording data until forced to stop (Ctrl+C)\n\n`python main.py <time>`\n\nat any time of the execution it can be stopped and there will still be a valid csv to use\n\n# GPU and OS Support\nThe system theoretically supports both AMD and NVIDIA GPUs, and also multiple GPUs but it has only been tested in a single NVIDIA GPU, in an ArchLinux system.\n\n# Contributions\nAll contributions are wellcome, even testing in different hardware configurations.',
    'author': 'JavierOramas',
    'author_email': 'javiale2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
