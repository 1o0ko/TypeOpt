from setuptools import setup


setup(
    name='typeopt',
    version='0.2',
    description='Typed docopt',
    author='Wojciech Stokowiec',
    author_email='wojciech.stokowiec@tooploox.com',
    url='https://github.com/1o0ko/typeopt',
    download_url='https://github.com/1o0ko/typeopt/tarball/0.1',
    packages=['typeopt'],
    keywords=['arguments', 'docopt', 'command-line'],
    install_requires=[
        'docopt',
    ],
    zip_safe=False
)
