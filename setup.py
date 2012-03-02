from setuptools import setup, find_packages

version = '1.0'

setup(name='collective.firehose',
      version=version,
      description="Example Add-on",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'redis',
          'pyzmq',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      [console_scripts]
      firehose-record = collective.firehose.recorder:record_stats
      """,
      )
