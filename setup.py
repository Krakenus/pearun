from setuptools import setup


def get_long_description():
    with open('README.md') as readme:
        return readme.read()


setup(
    name='pearun',
    version='1.0.0',
    packages=['pearun'],
    author='Milan Vlasák',
    author_email='krakenus02@gmail.com',
    description='A simple utility to run user defined commands',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/Krakenus/pearun',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'pearun = pearun.__main__:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
