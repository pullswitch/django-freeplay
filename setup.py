from setuptools import setup, find_packages


setup(
    name = "django-freeplay",
    version = "0.1.0",
    author = "Dave Lowe",
    author_email = "dave@hellopullswitch.com",
    description = "Easily make regions of content on your site editable without custom models",
    long_description = open("README.rst").read(),
    license = "MIT",
    url = "http://github.com/pullswitch/django-freeplay",
    packages = find_packages(),
    install_requires = [
        "django-model-utils==1.1.0",
        "django-relatedadminwidget==0.0.2",
        "django-imagekit==2.0.1"
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
