from setuptools import setup

######################################################################################################
################ You May Remove All the Comments Once You Finish Modifying the Script ################
######################################################################################################

setup(

    name = 'sejmapi', 
    

    version = '0.1.0',
    
  
    py_modules = ["sejm_api"],
    

    package_dir = {'':'src'},
    
   
#     packages = ['ThePackageName1',
#                 'ThePackageName2',
#                 ...
#  ],
    
    
    author = 'Michal Salamon',
    author_email = 'komarjazdek23@gmail.com',
    
    
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type = "text/markdown",
    
    
    url='https://github.com/KomarJazdek/Your-First-Python-Package-on-PyPI',
    
    
 
    
    classifiers  = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Text Processing',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
    ],
    
    

    install_requires = [
        'requests ~= 2.31.0' 
        

    ],
    
    
    
    keywords = ['API', 'Sejm', 'Government'],
    
)
