from setuptools import setup, find_packages

setup(
    name="docugyan-shared-models",
    version="0.1.0",
    description="Shared Django models for the DocuGyan ecosystem",
    packages=find_packages(include=['docu_model', 'docu_model.*']),
    include_package_data=True,
    install_requires=[
        "Django>=4.0",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)