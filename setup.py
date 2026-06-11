from setuptools import setup, find_packages

setup(
    name="vedic-agi",
    version="1.0.0",
    description="Sovereign AGI built on Vedic algorithms — 1,092x faster attention",
    author="Joydeep Das",
    author_email="joydeep@divineearthly.in",
    packages=find_packages(),
    install_requires=["torch>=2.0.0", "numpy>=1.24.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
