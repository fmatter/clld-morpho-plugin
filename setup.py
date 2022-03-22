from setuptools import setup, find_packages

with open("requirements.txt") as req_file:
    requirements = req_file.read()

setup(
    name="clld-morpho-plugin",
    version="0.0.1",
    description="clld-morpho-plugin",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Florian Matter",
    author_email="florianmatter@gmail.com",
    url="https://github.com/fmatter/clld-morpho-plugin",
    keywords="web pyramid pylons",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    extras_require={
        "dev": ["flake8", "wheel", "twine"],
        "test": [
            "pytest>=4.6",
        ],
    },
    license="Apache 2.0",
)
