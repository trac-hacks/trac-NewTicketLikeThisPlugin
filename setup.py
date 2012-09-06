from setuptools import find_packages, setup

version='0.2'

try:
    long_description = open("README.txt").read()
except:
    long_description = ''

setup(name='trac-NewTicketLikeThisPlugin',
      version=version,
      description="Pluggable framework for 'cloning' Trac tickets according to custom business logic",
      long_description=long_description,
      author='Ethan Jucovy',
      author_email='ejucovy@gmail.com',
      url='http://trac-hacks.org/wiki/NewTicketLikeThisPlugin',
      keywords='trac plugin',
      license="BSD",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests*']),
      include_package_data=True,
      package_data={ 'newticketlikethisplugin': ['templates/*', 'htdocs/*'] },
      zip_safe=False,
      entry_points = """
      [trac.plugins]
      newticketlikethis = newticketlikethis
      """,
      )

