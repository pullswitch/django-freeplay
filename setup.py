from setuptools import setup, find_packages


setup(
    name = "django-freeplay",
    version = "0.1.91",
    author = "Dave Lowe",
    author_email = "dave@hellopullswitch.com",
    description = "Easily add CMS functionality to your Django site",
    long_description = open("README.rst").read(),
    license = "MIT",
    url = "http://github.com/pullswitch/django-freeplay",
    packages = ["freeplay"],
    package_data = {"freeplay": ["templates/admin/freeplay/*", "templatetags/*.py"]},
    install_requires = [
        "django-model-utils==1.1.0",
        "django-relatedadminwidget==0.0.2",
        "django-imagekit>=3.0.4"
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
