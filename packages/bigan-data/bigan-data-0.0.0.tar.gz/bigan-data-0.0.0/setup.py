from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="bigan-data",
    version="0.0.0",
    author="heian0224",
    author_email="heian0224@gmail.com",
    description="Bigan Trading Data Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/FutureFantasy/BiGan/_git/bigan-data",
    project_urls={
        "Bug Tracker": "https://dev.azure.com/FutureFantasy/BiGan/_git/bigan-data/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
