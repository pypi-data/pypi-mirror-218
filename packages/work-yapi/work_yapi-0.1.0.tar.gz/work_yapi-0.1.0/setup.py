#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests']

test_requirements = ['pytest>=3', ]

setup(
    author="zhy",
    author_email='531691961@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="YApi python SDK",
    entry_points={
        'console_scripts': [
            'work_yapi=work_yapi.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='work_yapi',
    name='work_yapi',
    packages=find_packages(include=['work_yapi', 'work_yapi.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/w89306768/work_yapi',
    version='0.1.0',
    zip_safe=False,
)
