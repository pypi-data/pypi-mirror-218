from setuptools import setup

setup(
    name="tenuki",
    version="0.2.0",
    description="A set of development tools for go/baduk/wéiqí projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konrad Hałas",
    author_email="halas.konrad@gmail.com",
    url="https://github.com/konradhalas/tenuki",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    packages=["tenuki"],
    package_data={"tenuki": ["py.typed"]},
    extras_require={
        "dev": ["pytest>=7.4", "black", "mypy"]
    },
)
