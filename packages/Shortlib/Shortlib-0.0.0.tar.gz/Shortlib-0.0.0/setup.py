#  PyShot - ShortCut Library for Python
#  Copyright (C) 2023-present Pr0fess0r-99 <https://github.com/Pr0fess0r-99>

import re
import setuptools

# read requirements.txt file
with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

# find repository version
with open("shortlib/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

# read readme.md
with open("README.md", encoding="utf-8") as f:
    readme = f.read()
  
setuptools.setup(
    name="Shortlib",
    version=version,
    author="Pr0fess0r-99",
    long_description=readme,
    license='GNU General Public License v3.0',
    description='python short cut',                           
    package_data={
      "shortlib": ["py.typed"],
    },
    url="https://github.com/PR0FESS0R-99/ShortLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    python_requires=">=3.6",
    install_requires=requires,
    py_modules=["shortlib"],
)
