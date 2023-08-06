import setuptools

with open('README.md', "r") as f:
    long_description = f.read()

setuptools.setup(
    name="MusicBGX",
    version="1.0.7",
    author="Amin Rngbr",
    author_email="rngbramin@gmail.com",
    description="A light and simple library for playing offline and online music in the background (:",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aminrngbr1122",
    keywords="music",
    packages=['MusicBGX'],
    # entry_points={
    #     'console_scripts': [
    #         'proton = ProtonX:protonCmp',
    #     ],
    # },
    install_requires=[
        "pygame"
    ],
    python_requires=">=3.4",
)
