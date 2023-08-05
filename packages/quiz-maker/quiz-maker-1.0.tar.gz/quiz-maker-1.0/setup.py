from setuptools import setup, find_packages


setup(
  name='quiz-maker',
  version='1.0',
  license='MIT',
  author="Bruno Zhong",
  author_email='email@example.com', # Har har har!
  packages=find_packages('src'),
  package_dir={'': 'src'},
  url='https://github.com/Brunozhon/quiz-maker',
  keywords='quiz maker',
  install_requires=[
    'pysimplegui'
  ]
)
