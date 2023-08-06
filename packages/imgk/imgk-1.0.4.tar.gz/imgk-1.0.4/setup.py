from setuptools import setup, find_packages

with open('README.md', 'rb') as f:
    long_description = f.read().decode('utf-8')

setup(
    name='imgk',
    version='1.0.4',
    author='Prakhar Rathore',
    description='Image Processing Utility',
    url='https://github.com/prak132/imgk_cli',
    keywords='image-processing utility command-line',
    long_description_content_type='text/markdown',
    long_description=long_description,
    platforms="macOS",
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'imgk=imgk.cli:main',
        ],
    }
)
