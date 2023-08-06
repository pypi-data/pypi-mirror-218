
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="daletou222",
    version="0.0.2",
    author="soundless",
    author_email="soundless2023@gmail.com",
    description="example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="",
    #project_urls={},
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
