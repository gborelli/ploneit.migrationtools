from setuptools import setup, find_packages
import os

version = '1.0'
requirements = ['setuptools', 'Products.CMFPlone']
try:
    import json
except:
    requirements.append('simplejson')

setup(name='ploneit.migrationtools',
      version=version,
      description="plone.it migration tools",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ploneit'],
      include_package_data=True,
      zip_safe=False,
      install_requires= requirements,
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
