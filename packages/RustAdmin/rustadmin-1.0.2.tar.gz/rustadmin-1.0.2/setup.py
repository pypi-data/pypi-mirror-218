from setuptools import setup, find_packages

setup(
    name='rustadmin',
    version='1.0.2',
    author='Pawan kumar',
    author_email='control@vvfin.in',
    description='Rustadmin is tool design to handle Ruster server',
    packages=find_packages(),
    py_modules=['rustadmin'],
    install_requires=[
        "Rustadmin"
    ],
    entry_points={
        'console_scripts': [
            'ruster = RustAdmin.create:main',
        ],
    },
)
