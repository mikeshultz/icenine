import os, inspect
from importlib import __import__
from setuptools import setup, find_packages

cwd = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
assets_dir = os.path.join(cwd, 'icenine', 'ui', 'assets')

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

assets = package_files(assets_dir)

setup(
    name="icenine",
    version="0.1.0a2",
    packages=find_packages(exclude=["tests.*", "tests", "scripts", "docs"]),
    install_requires=open('requirements.txt').read().split('\n'),
    author="Mike Shultz",
    author_email="mike@gointo.software",
    description="A graphical Ethereum cold storage wallet",
    license="GPLv3+",
    keywords="ethereum wallet cold storage air gapped",
    url="https://github.com/mikeshultz/icenine",
    download_url="https://github.com/mikeshultz/icenine/archive/v0.1.0a2.tar.gz",
    entry_points={
        'console_scripts': [
            'icenine = icenine.ui.app:launch',
        ]
    },
    package_data={
        '': ['*.txt'] + assets,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: MacOS X",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires='~=3.4',
)