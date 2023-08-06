from setuptools import setup

setup(
    name='queueing_systems',
    version='0.1.0',
    author='Paulius Tervydis',
    author_email='Paulius.Tervydis@ktu.lt',
    description='Python package for queueing system parameter estimation using queueing theory',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pauterv/queueing_systems',
    packages=['queueing_systems'],
    install_requires=[
        # List any dependencies your package requires
        'numpy',
        'pandas',
        'matploblib'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
