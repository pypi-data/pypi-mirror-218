from setuptools import setup, find_packages

setup(
    name='QVSED',
    version='1.0.1',
    author='Arsalan Kazmi',
    description='Qt-Based Volatile Small Editor',
    packages=find_packages(),
    license="GPL-3.0-or-later",
    include_package_data=True,
    install_requires=[
        'PyQt5'
    ],
    entry_points={
        'console_scripts': [
            'qvsed = QVSED.qvsed:main',
        ],
    },
    package_data={'QVSED': ['QVSED.ui']},
)
