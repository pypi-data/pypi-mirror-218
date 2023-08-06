from setuptools import setup, find_packages

setup(
    name='RustAdmin',
    version='1.0.8',
    author='Pawan Kumar',
    author_email='control@vvfin.in',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'rust-admin = admin.main:main',
        ],
    },
)
