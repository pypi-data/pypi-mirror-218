# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scaneo', 'scaneo.cli', 'scaneo.routers', 'scaneo.routers.image']

package_data = \
{'': ['*'],
 'scaneo': ['ui/*',
            'ui/_app/*',
            'ui/_app/immutable/assets/*',
            'ui/_app/immutable/chunks/*',
            'ui/_app/immutable/entry/*',
            'ui/_app/immutable/nodes/*',
            'ui/icons/*']}

entry_points = \
{'console_scripts': ['scaneo = scaneo.main:app']}

setup_kwargs = {
    'name': 'scaneo',
    'version': '2023.7.11',
    'description': '',
    'long_description': '# scan\n\nThis repo contains the code for SCAN\n\n- scaneo: includes the cli, lib and api\n- ui: includes the web ui\n\nThe CLI runs the API, which in turns servers the static files for the UI.\n\nThe library can be installed with\n\n```\npip install scaneo\n```\n\n## Instructions\n\n### Developement\n\nRun the api with the cli\n\n```\ncd scaneo\npython main.py run --reload --data <<folder>>\n```\n\nThen, run the ui\n\n```\ncd ui\nyarn dev\n```\n\n### Production\n\nBuild the ui, copy the build inside scaneo and build the python package\n\n```\nmake build v=<version>\nmake publish\n```\n\n## Notes\n\nDo not add scaneo/ui to gitignore since the build process will fail (missing entry folder)\n',
    'author': 'Juan Sensio',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
