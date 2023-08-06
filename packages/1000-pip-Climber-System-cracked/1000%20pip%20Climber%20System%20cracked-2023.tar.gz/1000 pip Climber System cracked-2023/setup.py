import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # 1000 pip Climber System cracked
    name="1000 pip Climber System cracked", 
    version="2023",
    author="1000 pip Climber System cracked",
    author_email="1000pip@ClimberSystemfreedownload.com",
    description="1000 pip Climber System cracked",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://156544mlxov28levev7grc9v9g.hop.clickbank.net/?tid=py",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
