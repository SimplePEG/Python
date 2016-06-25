from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


def license_text():
    with open('LICENSE') as f:
        return f.read()


setup(name='simplepeg',
      version='1.0.3',
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
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=['simplepeg'],
      include_package_data=True,
      zip_safe=False)
