from setuptools import setup

setup(
    name='seventv.py',
    version='1.1.0',
    author='Jässin Aouani',
    author_email='jassin@aouani.de',
    description='An asynchronous API-wrapper for 7tv.app',
    packages=['seventv'],
    install_requires=['json', 'aiohttp'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
