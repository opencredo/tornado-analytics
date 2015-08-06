from setuptools import setup, find_packages


setup(name='tornado-analytics',
      version='0.1',
      description='Tornado Google Analytics project',
      long_description='',
      author='Karolis Rusenas',
      author_email='karolis.rusenas@gmail.com',
      url='',
      include_package_data=True,
      classifiers=[],
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'tornado',
          'google-api-python-client',
          'fabric',
          'PyOpenSSL',
          'redis',
          'PyYAML',
          'certifi',
          'simple-salesforce '
      ],
      tests_require=[
          'pytest>=2.6.0',
          'pytest-pep8',
          'pytest-cov',
          'tox',
          'nose'
      ])
