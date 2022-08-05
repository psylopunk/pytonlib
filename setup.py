import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ton",
    version="0.20",
    author="psylopunk",
    author_email="psylopunk@protonmail.com",
    description="Python client for The Open Network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psylopunk/pytonlib",
    packages=setuptools.find_packages(),
    install_requires=[
        'crc16>=0.1.1',
        'poetry>=1.1.13',
        'ujson>=5.2.0',
        'requests>=2.27.1',
        'tvm_valuetypes>=0.0.9',
        'PyNaCl>=1.5.0'
    ],
    package_data={
        'ton': [
            'distlib/linux/*',
            'distlib/darwin/*',
            'distlib/windows/*',
            'distlib/freebsd/*',
        ]
    },
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
