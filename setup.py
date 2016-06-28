#!/usr/bin/env python
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


def readme():
    with open('README.rst') as f:
        return f.read()


def license_text():
    with open('LICENSE') as f:
        return f.read()


class Tox(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args)
        sys.exit(errno)


setup(name='simplepeg',
      version='1.0.4',
      description='Python version of SimplePEG',
      long_description=readme(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Text Processing :: Linguistic',
      ],
      url='https://github.com/SimplePEG/Python',
      author='Oleksii Okhrymenko',
      author_email='ai_boy@live.ru',
      keywords='peg parser grammar',
      license=license_text(),
      tests_require=['pytest', 'tox'],
      cmdclass={'test': Tox},
      packages=['simplepeg'],
      include_package_data=True,
      zip_safe=False)
