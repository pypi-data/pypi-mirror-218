from setuptools import setup, find_packages

setup(
    name='trycortex-py',
    version='1.0.0',
    description='A short description of your package',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/kinesysai/cortex-py',
    author='Charles Pun',
    author_email='charlespun6@gmail.com',
)