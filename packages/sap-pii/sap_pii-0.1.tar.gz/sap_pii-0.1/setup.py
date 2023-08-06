from setuptools import setup, find_packages
setup(
   name='sap_pii',
   version='0.1',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      my_cli_app=sap_pii.my_cli_app:hello
      ''',
)