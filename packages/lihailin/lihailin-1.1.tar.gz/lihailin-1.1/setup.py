from setuptools import setup, find_packages
 
  
 
setup(
 
 name = "lihailin",
 
 version = "1.1",
 
 description = "eds sdk",
 
 long_description = "eds sdk for python",
 
 license = "MIT Licence",
 
  
 
 url = "http://test.com",
 
 author = "lihailin",
 
 author_email = "test@gmail.com",
 
  
 
 packages = find_packages(),
 
 include_package_data = True,
 
 platforms = "any",
 
 install_requires = ["selenium>=4.10.0"],
 
  
 
 scripts = [],
 
 entry_points = {
 
  'console_scripts': [
 
   'test = test.help:main'
 
  ]
 
 }
 
)