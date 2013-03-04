import os
from setuptools import setup, find_packages
import multilingual_project_blog as app


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-multilingnual-project-blog",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, cms, blog, project, documentation, research',
    author='Martin Brochhaus',
    author_email='mbrochh@gmail.com',
    url="https://github.com/bigee/django-multilingual-project-blog",
    packages=find_packages(),
    include_package_data=True,
    tests_require=[
        'fabric',
        'factory_boy',
        'django-nose',
        'coverage',
        'django-coverage',
        'mock',
    ],
    test_suite='multilingual_project_blog.tests.runtests.runtests',
)
