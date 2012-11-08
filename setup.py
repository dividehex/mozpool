#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

print setup.func_code
setup(name='mozpool',
      version='0.3.1',
      description='System to manage a pool of cranky mobile devices',
      author=u'Ted Mielczarek, Mark Côté, Dustin Mitchell',
      url='http://hg.mozilla.org/build/mozpool',
      author_email='ted@mielczarek.org',
      packages=find_packages('.'),
      package_data={
          'mozpool' : [ 'html/*.html', 'html/ui/*.html', 'html/ui/css/*.css', 'html/ui/js/*.js', 'html/ui/js/deps/*.js' ],
      },
      install_requires=[
          'sqlalchemy',
          'requests',
          'distribute',
          'templeton >= 0.6.2',
      ],
      entry_points={
          'console_scripts': [
              'relay = mozpool.bmm.scripts:relay_script',
              'mozpool-server = mozpool.web.server:main',
              'mozpool-inventorysync = mozpool.lifeguard.inventorysync:main',
              'mozpool-db = mozpool.db.scripts:db_script',
          ]
      }
)
