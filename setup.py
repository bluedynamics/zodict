# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from setuptools import setup, find_packages
import sys, os

version = '1.9.4dev'
shortdesc = 'zope.interface compliant ordered dictionary and zope.location ' + \
            'aware node.'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()
tests_require = [
    'zope.location',
    'interlude',
    'guppy',
]

setup(name='zodict',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: Python Software Foundation License',
            'Framework :: Zope3',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development',
      ],
      keywords='odict zodict tree node leaf datamodel container',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'https://svn.plone.org/svn/archetypes/AGX/zodict',
      license='Python Software Foundation License',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=[],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'node',
      ],
      tests_require=tests_require,
      test_suite="zodict.tests.test_suite",
      extras_require = dict(
          test=tests_require,
      ),
      )
