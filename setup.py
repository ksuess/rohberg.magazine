from setuptools import setup, find_packages
import os

version = '1.0'

tests_require = [
    'ftw.builder',
    'ftw.testing [splinter]',
    'plone.app.testing',
    ]

setup(name='rohberg.magazine',
      version=version,
      description="Illustration of dexterity types and related",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rohberg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.contenttypes',
          'html2text',
          'plonetheme.onegov',
          'ftw.subsite',
          'ftw.contentpage',
          'ftw.slider',
          'collective.z3cform.widgets',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
