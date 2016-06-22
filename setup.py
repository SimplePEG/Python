from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='simplepeg',
      version='1.0.1',
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
      license=license,
      packages=['simplepeg'],
      include_package_data=True,
      zip_safe=False)