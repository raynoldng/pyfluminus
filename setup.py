import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfluminus", 
    version="0.0.1",
    author="Raynold Ng",
    author_email="raynold.ng24@gmail.com",
    description="Python port of fluminus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raynoldng/pyfluminus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
