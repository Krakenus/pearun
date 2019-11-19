from setuptools import setup

setup(
    name='pearun',
    version='0.1',
    packages=['pearun'],
    author='Milan Vlasák',
    author_email='krakenus02@gmail.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'pearun = pearun.__main__:main',
        ],
    }
)
