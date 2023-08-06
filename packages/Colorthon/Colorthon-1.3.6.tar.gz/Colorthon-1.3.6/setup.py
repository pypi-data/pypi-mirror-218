from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Colorthon",
    version="1.3.6",
    author="Pymmdrza",
    author_email="Pymmdrza@gmail.com",
    description="easy color terminal and pretty text with colorthon.",
    keywords=['color','print', 'text', 'colorText'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/colorthon/colorthon",
    project_urls={
        "Documentation": "https://colorthon.github.io/colorthon/",
        "Personal Website": "https://mmdrza.com"
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
