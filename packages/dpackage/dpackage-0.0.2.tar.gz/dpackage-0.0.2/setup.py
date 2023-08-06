from setuptools import find_packages, setup


setup(
    name="dpackage",
    version="0.0.2",
    description="test",
    package_dir={"": "_distutils_hack"},
    packages=find_packages(where="_distutils_hack"),
    long_description='sad',
    long_description_content_type="text/markdown",
    url="https://github.com/ArjanCodes/2023-package",
    author="DDjango",
    author_email="ddjango.786@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)