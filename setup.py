from setuptools import setup

setup(
    name='pic-sorter',
    version='0.0.1',
    description='Crawl and sort your files',
    author='Vincent Segouin',
    author_email='vincent.segouin@gmail.com',
    packages=['pic-sorter'],  # same as name
    install_requires=['exifread', 'python-magic', 'watchdog', 'pytesseract'],  # external packages as dependencies
)

#  brew install tesseract
#  brew install freetype imagemagick@6
