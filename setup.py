# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Package distribution configuration."""
from setuptools import setup

long_description = open("README.rst", "r", encoding="utf-8").read()

setup(
    name="gol-bot",
    version="0.0.2",
    description="Game of Life push-ups counter.",
    long_description=long_description,
    url="https://github.com/lulivi/gol-bot",
    author="Luis Liñán Villafranca",
    author_email="luislivilla@gmail.com",
    license="MIT",
    keywords="telegram bot python gol",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["gol", "gbot"],
    package_data={"bot_help": ["gbot/data/help.txt"]},
    include_package_data=True,
    install_requires=[
        "python-telegram-bot",
        "python-decouple",
    ],
    entry_points={
        "console_scripts": [
            "gol-bot=gbot.__main__:main",
        ]
    },
    project_urls={
        "Source Code": "https://github.com/lulivi/gol-bot",
        "Bug Tracker": "https://github.com/lulivi/gol-bot/issues",
    },
    python_requires=">=3.6",
)
