from setuptools import setup, find_packages

__version__ = 'dev'

setup(
    name='simpleapp',  # replace name of your project here
    version=__version__,
    author='pprolancer@gmail.com',
    description='Simple Flask App',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('/etc/orange/simpleapp',
         ['orange/simpleapp/conf/config.ini']),
    ],
    entry_points={
        'console_scripts': [
            'simpleapp_db = orange.simpleapp.scripts.database:main',
        ],
    },
    dependency_links=[
    ],
    install_requires=[
        'flask-login',
        'flask-principal',
        'flask',
        'uwsgi',
        'simplejson',
    ],
    classifiers=['Development Status :: 1 - Production/Beta',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Topic :: Internet :: WWW/HTTP',
                 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                 'Topic :: Software Development :: Libraries :: Application Frameworks',
                 'Topic :: Software Development :: Libraries :: Python Modules', ],
)
