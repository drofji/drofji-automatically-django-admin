from setuptools import setup, find_packages

setup(
    name="drofji_automatically_django_admin",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",

    install_requires=[
        "Django>=5.2",
        "django-admin-rangefilter~=0.13.3",
        "django-admin-interface~=0.28.9",
        "django-colorfield~=0.11.0",
        "django-cors-headers~=4.4.0",
        "django-crontab~=0.7.1",
        "django-datepick~=0.1.2",
    ],

    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)