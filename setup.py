from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="advanced_tc",
    version="0.0.1",
    author="Prova",
    author_email="prova@prova.it",
    description="Calendar view per i timesheets details",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        # "frappe>=15.0.0"
    ],
    include_package_data=True,
    zip_safe=False
)