from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='fnlength',
  version='1.0.0',
  author='IgorMan (IgorMan2005)',
  author_email='igorman2005@gmail.com',
  description='Python filename length script',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/IgorMan2005/fnlength',
  packages=['fnlength'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python filename length script filenamelength fnlength',
  project_urls={
    'Documentation': 'https://best-itpro.ru/news/fnlength/',
  },
  python_requires='>=3.6'
)