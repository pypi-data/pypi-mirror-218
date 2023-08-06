import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hmtaipy",
    version="1.0.2",
    license='MIT',
    author="TheCuteOwl",
    description="API Wrapper of hmtai NPM package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    packages=setuptools.find_packages(),
    scripts=['bin/hmtaipy.py'],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)