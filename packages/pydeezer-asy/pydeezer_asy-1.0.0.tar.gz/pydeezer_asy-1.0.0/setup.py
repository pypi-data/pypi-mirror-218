import setuptools



setuptools.setup(
    name='pydeezer_asy',
    version='1.0.0',
    description='Asynchronous version of the `py-deezer` module',
    author='dehspfn',
    packages=setuptools.find_packages(),
    install_requires=[
        "aiohttp",
        "cryptography",
        "mutagen",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
