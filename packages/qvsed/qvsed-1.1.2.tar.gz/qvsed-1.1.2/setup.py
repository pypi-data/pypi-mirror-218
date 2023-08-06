from setuptools import setup, find_packages

setup(
    name='qvsed',
    version='1.1.2',
    author='Arsalan Kazmi',
    description='Qt-Based Volatile Small Editor',
    long_description='QVSED is a volatile text editor, meaning that there are no restrictions against unsaved work or bad files. QVSED is a PyQt5 rewrite of my older project, ASMED (Another SMol EDitor), which was written using Windows Forms, and was quite obviously only for Windows. QVSED seeks to replace ASMED by being cross-platform, and it will bring over the benefits of such a lightweight editor without the overhead of .NET. QVSED is licensed under the GNU General Public License version 3 or later.',
    packages=find_packages(),
    license="GPL-3.0-or-later",
    url='https://github.com/That1M8Head/QVSED/',
    include_package_data=True,
    install_requires=[
        'PyQt5'
    ],
    entry_points={
        'gui_scripts': [
            'qvsed = qvsed.qvsed:main',
        ],
    },
    package_data={'qvsed': ['qvsed.ui']},
)
