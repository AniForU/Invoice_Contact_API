from setuptools import setup, find_packages

setup(

    name="Invoice-contact-api",
    description="API to update invoice and contact details",
    version="1.0.0",
    author="Anirudh Sharma",
    author_email="animaxsharma20@gmail.com",
    package=find_packages(where="src"),
    package_dir={"","src"},
    install_requires=[
        "fastapi == 0.63.0",
        "Flask == 1.1.2",
        "Flask_PyMongo == 2.3.0",
        "pymongo == 3.11.3",
        "pydantic == 1.8.1",
        "mockupdb== 1.8.1",
    ]

)