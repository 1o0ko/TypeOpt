from setuptools import setup


setup(name='typeopt',
      version='0.1',
      description='Typed docopt',
      url='https://github.com/nowthisnews/typeopt',
      author='Wojciech Stokowiec',
      author_email='wojciech.stokowiec@tooploox.com',
      packages=['typeopt'],
      install_requires=[
          'docopt',
      ],
      zip_safe=False)
