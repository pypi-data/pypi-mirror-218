import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    author="Rispar",
    author_email="tecnologia@rispar.com.br",
    url="https://github.com/risparfinance/anbima_calendar",
    name="anbima_calendar",
    version="0.0.2",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={"anbima_calendar": ["LICENSE"]},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Ambima Calendar - Helper functions to handle banking holidays in Brazil",
    license="Apache License 2.0",
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
)
