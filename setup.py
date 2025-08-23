from setuptools import setup, find_packages

setup(
    name="nextgen_realty",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "stripe",
        "alembic",
        "pydantic-settings",
        "python-dotenv"
    ],
)