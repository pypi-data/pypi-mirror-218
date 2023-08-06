from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='PySortAlgos',
    version='0.5',
    author='Bahir Hakimi',
    author_email='bahirhakimy2020@gmail.com',
    description='A simple package that contains some commonly used sorting functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/your-username/PySortAlgos',
    packages=['PySortAlgos'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)