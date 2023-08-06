from setuptools import setup, find_packages

setup(
    name='MoReSQUE',
    version='1.0',
    author='Cornelius Steinbrink',
    author_email='mosaik@offis.de',
    description='Uncertainty quantification module for mosaik',
    long_description=(open('README.rst', encoding='utf-8').read()),
    packages=find_packages(),
    include_package_data=True,
    url='',
    install_requires=[
        'mosaik-api>=2.0',
        'numpy',
        'scipy',
        'pyDOE',
        'arrow',
        'statsmodels',
    ],
    entry_points={
        'console_scripts': [
            'propagator = moresque.propagator_sim:main',
        ],
    },
    classifiers={
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
    },
)
