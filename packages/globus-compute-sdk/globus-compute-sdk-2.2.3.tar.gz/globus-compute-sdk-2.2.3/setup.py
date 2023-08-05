import os
import re
from pathlib import Path

from setuptools import find_namespace_packages, setup

REQUIRES = [
    # request sending and authorization tools
    "requests>=2.20.0",
    "globus-sdk>=3.20.1,<4",
    "globus-compute-common==0.2.0",
    # 'websockets' is used for the client-side websocket listener
    "websockets==10.3",
    # dill is an extension of `pickle` to a wider array of native python types
    # pin to the latest version, as 'dill' is not at 1.0 and does not have a clear
    # versioning and compatibility policy
    "dill==0.3.5.1",
    # typing_extensions, so we can use Protocol and other typing features on python3.7
    'typing_extensions>=4.0;python_version<"3.8"',
    # packaging, allowing version parsing
    # set a version floor but no ceiling as the library offers a stable API under CalVer
    "packaging>=21.1",
    "pika>=1.2",
    "tblib==1.7.0",
    "texttable>=1.6.7",
]
DOCS_REQUIRES = [
    "sphinx<5",
    "furo==2021.09.08",
]

TEST_REQUIRES = [
    "flake8==3.8.0",
    "pytest>=7.2",
    "pytest-mock",
    "pyfakefs",
    "coverage",
    # easy mocking of the `requests` library
    "responses",
]
DEV_REQUIRES = TEST_REQUIRES + [
    "pre-commit",
]


def parse_version():
    # single source of truth for package version
    version_string = ""
    version_pattern = re.compile(r'__version__ = "([^"]*)"')
    with open(os.path.join("globus_compute_sdk", "version.py")) as f:
        for line in f:
            match = version_pattern.match(line)
            if match:
                version_string = match.group(1)
                break
    if not version_string:
        raise RuntimeError("Failed to parse version information")
    return version_string


directory = Path(__file__).parent
long_description = (directory / "PyPI.md").read_text()


setup(
    name="globus-compute-sdk",
    version=parse_version(),
    packages=find_namespace_packages(
        include=["globus_compute_sdk", "globus_compute_sdk.*"]
    ),
    description="Globus Compute: High Performance Function Serving for Science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
        "test": TEST_REQUIRES,
        "docs": DOCS_REQUIRES,
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    keywords=["Globus Compute", "FaaS", "Function Serving"],
    author="Globus Compute Team",
    author_email="support@globus.org",
    license="Apache License, Version 2.0",
    url="https://github.com/funcx-faas/funcx",
    project_urls={
        "Changelog": "https://globus-compute.readthedocs.io/en/latest/changelog.html",  # noqa: E501
        "Upgrade to Globus Compute": "https://globus-compute.readthedocs.io/en/latest/funcx_upgrade.html",  # noqa: E501
    },
)
