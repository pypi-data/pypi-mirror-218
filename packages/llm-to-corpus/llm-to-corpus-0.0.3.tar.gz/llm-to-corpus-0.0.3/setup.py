import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


def read_version(fname="src/llm_to_corpus/version.py"):
    exec(compile(open(fname, encoding="utf-8").read(), fname, "exec"))
    return locals()["__version__"]


setup(
    name="llm-to-corpus",
    version=read_version(),
    description="Large language model to corpus",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jordimas/llm-to-corpus/",
    author="Jordi Mas",
    author_email="jmas@softcatala.org",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["src/llm_to_corpus"],
    include_package_data=True,
    extras_require={
        "dev": ["flake8==6.*", "black==23.*", "nose2"],
    },
    entry_points={
        "console_scripts": [
            "llm-to-corpus=src.llm_to_corpus.cli:main",
        ]
    },
)
