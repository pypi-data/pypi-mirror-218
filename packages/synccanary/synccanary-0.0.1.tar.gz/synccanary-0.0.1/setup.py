import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="synccanary",
    version="0.0.1",
    author="Sanjeev Yadav",
    author_email="sanjeevyadavcr7@gmail.com",
    description=("A package to publish latest canaries version in frontend"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SanjeevYadavcr7/CanarySync",
    project_urls={
        "Bug Tracker": "https://github.com/SanjeevYadavcr7/CanarySync/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "synccanary = synccanary.cli:main",
        ]
    }
)