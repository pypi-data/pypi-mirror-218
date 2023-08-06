from setuptools import setup, find_packages
from readme_renderer.markdown import render

long_description = ""
with open('README.md', encoding='utf-8') as file:
  long_description = file.read()

setup(
  name = "lesaviezvous",
  version = "0.1.1",
  author="Coding Team",
  author_email="codingteam@telegmail.com",
  license='MIT',
  description='Un package Python pour obtenir des informations intéressantes du monde.',
  long_description=render(long_description),
  long_description_content_type="text/markdown",
  url="https://github.com/codingtuto/lesaviezvouspkg/",
  packages=find_packages(exclude=["testing"]),
  install_requires=[
    'requests'
  ],
  python_requires='>=3.7',
  classifiers=[
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.7",
    "Topic :: Utilities"
  ],
)