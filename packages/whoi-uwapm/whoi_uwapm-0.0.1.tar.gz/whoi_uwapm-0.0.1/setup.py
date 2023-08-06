from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='whoi_uwapm',
    version='0.0.1',
    description='WHOI Acomms Group uwapm',
    long_description=readme,
    author='Eric Gallimore',
    author_email='egallimore@whoi.edu',
    url='https://git.whoi.edu/acomms/whoi_uwapm',
    license='BSD (3-clause)',
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'bokeh'
    ]
)
