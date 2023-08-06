import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="citybrain-official",
    version="0.9",
    author="citybrain.org",
    author_email="opensource@citybrain.org",
    description="retrieve data from citybrain.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'pandas'
    ],
    python_requires='>=3',
)