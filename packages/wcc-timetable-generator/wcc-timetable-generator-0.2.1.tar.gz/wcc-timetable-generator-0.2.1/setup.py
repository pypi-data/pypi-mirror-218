# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wcc_timetable_generator', 'wcc_timetable_generator.components']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.29.0,<0.30.0']

entry_points = \
{'console_scripts': ['wcc-timetable-generator = '
                     'wcc_timetable_generator.__main__:main']}

setup_kwargs = {
    'name': 'wcc-timetable-generator',
    'version': '0.2.1',
    'description': '',
    'long_description': "# Timetable 📊\n\n## 📰 Description \nA CLI tool that allow you to generate a timetable for your school or university such that : \n - A subject can't be seen on two consecutive days\n - A subject have a minimum of 2 hours per week and a maximum of 6\n - The timetable is divided in slots of 2 hours\n - The subjects are distributed between monday morning and saturady morning\n - Morning classes begin at 8:30 and end at 12:30\n - Afternoon classes begin at 13:30 and end at 17:30\n\n ## 📦 Installation \n\n ### 💻 Local installation\n\n ### 🌐 Installation with PIP\n ```bash\n pip install wcc-timetable-generator\n ```\n\n## 🖱 Usage\n```bash\ngenerate-timetable\n```\n\n## Roadmap\n- [x] Add the algorithm \n- [ ] Add GUI\n- [ ] Write tests\n- [ ] Publish to PyPI",
    'author': 'Tsierenana Bôtramanagna Gracy',
    'author_email': 'gtsierenana@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
