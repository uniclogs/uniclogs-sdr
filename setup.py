import setuptools
import uniclogs_sdr

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    dependencies = file.read().split('\n')[:-1]

setuptools.setup(
    name=uniclogs_sdr.APP_NAME,
    version=uniclogs_sdr.APP_VERSION,
    author=uniclogs_sdr.APP_AUTHOR,
    license=uniclogs_sdr.APP_LICENSE,
    description=uniclogs_sdr.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=uniclogs_sdr.APP_URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: User Interfaces",
    ],
    install_requires='',
    python_requires='>=3.8.5',
    entry_points={
        "console_scripts": [
            '{} = uniclogs_sdr.__main__:main'.format(uniclogs_sdr.APP_NAME),
        ]
    }
)
