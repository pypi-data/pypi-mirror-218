from setuptools import setup, find_packages

setup(
    name='imgk',
    version='1.0.0',
    author='Prakhar Rathore',
    description='Image Processing Utility',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
)
