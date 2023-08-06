from setuptools import setup, find_packages

setup(
    name='eef-data',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy==1.22.0',
        'pandas==1.5.0',
        'prompt_toolkit==3.0.30',
        'rich==12.4.4',
        'toolz==0.11.2'
    ],
    entry_points={
        'console_scripts': [
            'eef-data=eefdata.app:main',
        ],
    },
)
