from setuptools import setup, find_packages

setup(
    name='url_to_file_downloader',
    version='1.0.0',
    description='A package to download audio, video, documents, or files from a given URL',
    author='Nayeem Islam',
    author_email='islam.nayeem@outlook.com',
    packages=find_packages(),
    install_requires=['requests'],
)
