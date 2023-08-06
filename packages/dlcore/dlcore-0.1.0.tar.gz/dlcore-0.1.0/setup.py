from setuptools import find_packages, setup

with open("/app/deepsinai/dlcore/Readme.md", "r") as f:
    long_description = f.read()

setup(
    name="dlcore",
    version="0.1.0",
    description="Deep Learning core in pytroch",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Milos Bijanic",
    author_email="bijanicmilos996@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    extras_require={},
    python_requires=">=3.10",
)