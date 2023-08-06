
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='random-otp-generator',
    version='1.0.0',
    description='A Python package for generating OTPs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nayeem Islam',
    author_email='islam.nayeem@outlook.com',
    url='https://github.com/NoManNayeem/Random-OTP-Generator-API-',
    packages=['otp_generator'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
