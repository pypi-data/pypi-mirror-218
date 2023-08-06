import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="iter_tools",
    version="0.0.2",
    author="Zecyel & Lion-UY",
    author_email="zecyel@163.com",
    description="Tool for iterations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lion-UY/iter-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)