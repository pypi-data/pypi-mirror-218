from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

exec(open('src/pysuggestify/version.py').read())

setup(
    name="pysuggestify",
    version=__version__,
    author="Mateusz Soczewka",
    author_email="msoczewkas@gmail.com",
    description="A user-friendly Python package for building recommendation systems based on PMF algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msoczi/pysuggestify",
    project_urls={
        "Bug Tracker": "https://github.com/msoczi/pysuggestify/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.4",
        "matplotlib>=3.4.3"
    ],
    py_modules=["pysuggestify"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
)
