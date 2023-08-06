from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='quotegen',
  version='0.0.1',
  description='Basic random quote generator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kirthikesh Parthasarathy',
  author_email='x21195391@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='randomquotegen', 
  packages=find_packages(),
  install_requires=[''] 
)