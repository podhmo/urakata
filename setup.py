import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'cliff',
    'pyramid_sqlalchemy',
    'pyramid_services'
]

setup(name='urakata',
      version='0.0',
      description='shadow scaffold template server',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='urakata',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = urakata:main
      [console_scripts]
      urakata = urakata.scripts.urakata:main
      [urakata.commands]
      initialize = urakata.scripts.initialize:Initialize
      clean = urakata.scripts.clean:Clean
      scan = urakata.scripts.scan:Scan
      emit = urakata.scripts.emit:Emit
      """,
      )
