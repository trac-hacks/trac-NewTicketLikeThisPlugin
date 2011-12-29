from setuptools import find_packages, setup

version='0.0'

setup(name='NewTicketLikeThisPlugin',
      version=version,
      description="",
      author='Ethan Jucovy',
      author_email='ejucovy@gmail.com',
      url='',
      keywords='trac plugin',
      license="",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests*']),
      include_package_data=True,
      package_data={ 'newticketlikethisplugin': ['templates/*', 'htdocs/*'] },
      zip_safe=False,
      entry_points = """
      [trac.plugins]
      newticketlikethis = newticketlikethis
      """,
      )

