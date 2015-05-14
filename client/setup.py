import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'requests',
    ]

setup(name='AMTTestGameClient',
      version='0.0',
      description='Test client for AMT game',
      author='Ivan Kosmatykh',
      author_email='ivan.kosmatikh@gmail.com',
      packages=find_packages(),
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      start_AMTTestGameClient = gameclient.main:main
      """,
      )
