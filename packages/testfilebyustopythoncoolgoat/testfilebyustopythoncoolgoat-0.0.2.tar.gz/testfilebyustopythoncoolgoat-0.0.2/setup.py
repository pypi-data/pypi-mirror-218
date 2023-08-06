from setuptools import setup, find_packages



VERSION = '0.0.2'
DESCRIPTION = "TestFile"
LONG_DESCRIPTION = "OkOkOk"


# Setting up
setup(
    name="testfilebyustopythoncoolgoat",
    version=VERSION,
    author="Ok Kumar",
    author_email="<OkOk@ok.com>",
    license='BSD',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/Kshitij-200/Leetcode_DSA",
    project_urls={
        'Homepage': 'https://example.com',
        'Documentation': 'https://example.com/docs',
        'Source Code': 'https://github.com/your-username/your-repo',},
    packages=find_packages(),
    install_requires=[
    "numpy>=1.22.3",
    "pandas>=2.0.0",
    "scikit-learn>=1.0.0",
    "scipy>=1.10.0",
    "matplotlib>=3.5.0",
    "seaborn>=0.11",
    "python-dateutil>=2.8.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: BSD License"
    ]
)
