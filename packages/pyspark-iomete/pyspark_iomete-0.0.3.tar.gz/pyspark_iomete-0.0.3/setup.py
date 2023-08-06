import os
from distutils.core import setup

package_name = "pyspark_iomete"
package_version = "0.0.3"

description = """IOMETE's PySpark library that contains useful utilities for working with PySpark"""

# pull long description from README
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name=package_name,
    packages=[package_name],
    version=package_version,
    license='Apache License 2.0',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='IOMETE',
    author_email='vusal@iomete.com',
    url='https://github.com/iomete/pyspark-iomete',
    keywords=['iomete', 'pyspark', 'utils'],
    extras_require={
        'dev': ['pyspark']
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
