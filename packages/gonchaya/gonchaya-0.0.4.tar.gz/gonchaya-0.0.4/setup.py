from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='gonchaya',
  version='0.0.4',
  author='Alexander Firsov aka gonchaya aka padla',
  author_email='gonchaya@gifara.ru',
  url='https://github.com/Alexander-Firsov/gonchaya',
  license='BSD-3-Clause',
  description='Data Science tools',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=['gonchaya'],
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Natural Language :: Russian'
  ],
  keywords='example python',
  python_requires='>=3.8'
)
