from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="planbee",
    description="production / job shop / resource scheduler for Python",
    author="Jacob Østergaard Nielsen",
    author_email="jaoe@oestergaard-as.dk",
    url="https://github.com/Yacobolo/PlanBee",
    license="MIT",
    license_file="LICENSE",
    platforms="unix, linux, osx, cygwin, win32",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    zip_safe=False,
    extras_require={
        "testing": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
)
