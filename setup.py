import os, inspect
from setuptools import setup, find_packages

cwd = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
assets_dir = os.path.join(cwd, 'icenine', 'ui', 'assets')
print(assets_dir)
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

assets = package_files(assets_dir)
print(assets)
setup(
    name="icenine",
    version="0.0.1.dev1",
    packages=find_packages(),
    install_requires=open('requirements.txt').read().split('\n'),
    author="Mike Shultz",
    author_email="mike@gointo.software",
    description="An Ethereum cold storage wallet",
    license="GPLv3+",
    keywords="ethereum wallet cold storage air gapped",
    url="https://github.com/mikeshultz/icenine",
    entry_points={
        'console_scripts': [
            'icenine = icenine.bin.launch:main',
        ]
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