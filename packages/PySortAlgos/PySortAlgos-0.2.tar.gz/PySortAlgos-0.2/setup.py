from distutils.core import setup
setup(
  name = 'PySortAlgos',
  packages = ['PySortAlgos'],
  version = '0.2',
  license='MIT',
  description = 'A simple package that contains some commonly used sorting functions',
  author = 'Bahir Hakimi',
  author_email = 'bahirhakimy2020@gmail.com',
  url = 'https://github.com/bahirhakimy/PySortAlgos',
  download_url = 'https://github.com/BahirHakimy/PySortAlgos/archive/refs/tags/0.1.tar.gz',
  keywords = ['sorting', 'algorithm', 'quicksort', 'array'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.9',
  ],
)