import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="programlib",
    version="2.0.0",
    description="Programs as Objects",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vadim0x60/programlib",
    author="Vadim Liventsev",
    author_email="hello@vadim.me",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Compilers",
        "Programming Language :: Python :: 3",
    ],
    packages=["programlib"],
    include_package_data=True,
)