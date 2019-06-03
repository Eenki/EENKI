from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="DECS",
    version="1.0",
    license='MIT',
    description="A fast Data Encryption Channel System",
    author='Eenki',
    author_email='eenki95@gmail.com',
    packages=['decs', 'decss.crypto'],
    package_data={
        'decs': ['README.rst', 'LICENSE']
    },
    install_requires=[],
    entry_points="""
    [console_scripts]
    decsserver = decs.server:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Channel Servers',
    ],
    long_description=long_description,
)
