from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='velilogger',
    py_modules=['velilogger'],
    version='1.0.0',
    description='Veli Logger',
    author='Konstantine',
    author_email='kdvalishvili@veli.store',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
