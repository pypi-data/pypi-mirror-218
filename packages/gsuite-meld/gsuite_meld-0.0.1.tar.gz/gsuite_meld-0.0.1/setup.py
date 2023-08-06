from setuptools import find_packages, setup

# pip install wheel, twine
# pip install .

# python setup.py bdist_wheel sdist
# twine check dist/*
# twine twine upload -r testpypi dist/*
# twine upload dist/*

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="gsuite_meld",
    version="0.0.1",
    description="'gsuite-meld' is a Python package unifying various GSuite services. It enables easy interaction with Google Sheets, Docs, Drive, and more. Designed for extensibility, it accommodates future GSuite additions, making multi-service workflows simple.",
    package_dir={"": "."},
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loudpumpkins/gsuite-meld",
    author="Alexei Panov",
    author_email="alexei_panov@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "google-api-python-client>=2.92.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=1.0.0",
        "typing_extensions>=4.7.1",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.6",
)