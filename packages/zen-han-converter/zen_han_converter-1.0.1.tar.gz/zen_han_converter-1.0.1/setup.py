from setuptools import setup, find_packages


setup(
    name="zen_han_converter",
    version="1.0.1",
    author="n4cl",
    author_email="devn4cl@gmail.com",
    description="Converts full-width and half-width characters.",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/n4cl/zen_han_converter.git",
    license='MIT',
    packages=find_packages(),
    package_dir={"zen_han_converter": "zen_han_converter"},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ]
)
