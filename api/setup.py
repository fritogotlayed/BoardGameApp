#!/user/bin/env python

import setuptools

setuptools.setup(
    name='board-game-api',
    author='Frito',
    description='',
    url='https://github.com/fritogotlayed/BoardGameApi',
    version='0.0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_dir={'board_game_api': 'board_game_api'},
    entry_points={
        'console_scripts': [
            'board-game-api = board_game_api.app:main'
        ]
    }
)
