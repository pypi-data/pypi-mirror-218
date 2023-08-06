import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proofy-sdk-python",
    version="0.0.2",
    author="ProofyDevTeam",
    author_email="dev@sbtkyc.io",
    description="Proofy SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://proofy.me",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)