from setuptools import setup, find_packages

setup(
    name="asmy",
    version="0.1.0",
    description="Python-based multi-architecture assembler",
    author="Serge Zaitsev",
    license="MIT",
    packages=find_packages(include=["asmy", "asmy.*"]),
    install_requires=[],
    python_requires=">=3.8",
    url="https://github.com/zserge/asmy",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Assemblers",
    ]
)
