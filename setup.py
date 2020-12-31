from distutils.core import setup
setup(
  name = 'recipeGetter',
  packages = ['recipeGetter'],
  version = '0.0.2',
  license='MIT',
  description = 'A scraper for recipe website',  
  author = 'Xavier Hamel',
  author_email = 'xavier.hamel.protic@gmail.com',
  url = 'https://github.com/xavierhamel/recipeGetter',
  download_url = 'https://github.com/xavierhamel/recipeGetter/archive/v_02.tar.gz',
  keywords = ['recipe', 'scraper', 'getter'],
  install_requires=[      
          'requests',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',    
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.9',
  ],
)
