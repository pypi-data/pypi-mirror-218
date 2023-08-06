from setuptools import setup, find_packages

setup(
    name='RustAdmin',
    version='1.0.4',
    author='Pawan kumar',
    author_email='control@vvfin.in',
    url='https://github.com/yourusername/rustadmin',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'rust-admin = Admin.main:main',
        ],
    },
)
