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
    'version': '1.1.2',
    'description': '',
    'long_description': "# Timetable 📊\n\n## 📰 Description \nA CLI tool that allow you to generate a timetable for your school or university such that : \n - A subject can't be seen on two consecutive days\n - A subject have a minimum of 2 hours per week and a maximum of 6\n - The timetable is divided in slots of 2 hours\n - The subjects are distributed between monday morning and saturady morning\n - Morning classes begin at 8:30 and end at 12:30\n - Afternoon classes begin at 13:30 and end at 17:30\n\n ## 📦 Installation \n\n ### 💻 Local installation\n\nTo install this project locally, you first have to clone this repo and install [poetry](https://python-poetry.org/) with pip : `pip install poetry`.\nThen, go to the root directory and run the following commands : \n```bash\npoetry install # install all the necessary dependencies\npoetry build\npoetry run python -m wcc_timetable_generator \n```\n\n ### 🌐 Installation with PIP\n ```bash\n pip install wcc-timetable-generator\n ```\n\n## 🖱 Usage\nIf you installed it with pip, this is how to run the project : \n```bash\nwcc-timetable-generator\n```\n\n## Roadmap\n- [x] Add the algorithm \n- [x] Add GUI-like UI\n- [x] Publish to PyPI\n- [ ] Fix display and algo so that there are are 1 hour classes\n- [ ] Add an animated GIF as demo to `README.md`\n- [ ] Write tests\n- [ ] Add quit button\n- [ ] Print error messages\n",
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
