from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pojediga",
    version="3.0.3",
    author="🇷🇸",
    author_email="ja_sam_lekar_za_sve@pojediga.rs",
    description="A simple pojediga package to feel good every day, every night",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["pojediga"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
