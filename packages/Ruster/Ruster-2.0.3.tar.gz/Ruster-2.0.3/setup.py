from setuptools import setup, find_packages

setup(
    name='Ruster',
    version='2.0.3',
    author='Pawan Kumar',
    author_email='control@vvfin.in',
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
        "werkzueg",
        "uuid",
        "rustadmin",
        "cryptography",
        "pyjwt",
        "jinja2",
        "itsdangerous",
        "nexusdb"
    ],
    entry_points={
        'console_scripts': [
            'ruster = ruster.app',
        ],
    },
)
