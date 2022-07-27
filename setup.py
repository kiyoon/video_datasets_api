"""setup script for video_datasets_api package."""

from setuptools import setup, find_packages

setup(
    name = "video_datasets_api",
    version="0.1",
    author = "Kiyoon Kim",
    author_email='kiyoon.kim@ed.ac.uk',
    description = "Video datasets' annotation parser and etc.",
    url = "https://github.com/kiyoon/video_datasets_api",
    packages=find_packages(),
    #packages=['video_datasets_api'],
    #package_dir={'video_datasets_api': 'src'},
    python_requires='>=3.5',
    install_requires=['numpy>=1.16.0',
        'beautifulsoup4',
        'pandas',
        'gulpio2 @ git+https://github.com/kiyoon/GulpIO2',
        'natsort',
        ],
    include_package_data = True,    # required for non-code files in the package to be installed together.
)
