from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Logits AI Python Client Library"
LONG_DESCRIPTION = "Logits AI Python Client Library"

setup(
    name="logitsai",
    version=VERSION,
    author="Anand Henry",
    author_email="<anand@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["openai"],
    keywords=["python", "logits logitsai", "logitsai python", "logitsai python"],
    classifiers=[],
)
