from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
project_urls = {
  'HomePage': 'https://bitbucket.org/cwrusdle/mds3-kgraph/src/main/',
    'Documentation':'https://bitbucket.org/cwrusdle/mds3-kgraph/src/main/docs/kgraph-doc/doc/mds3-kgraph/index.html'
}


setup(
    name='mds3-kgraph',
    version='0.1.0',
    keywords=['Knowledgegraph','ImageProcessing','Scenegraph'],
    description='mds3-kgraph',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls=project_urls,
    author='Mingjian Lu，Sameera Nalin Venkat,Thomas Ciardi,Yinghui Wu,Roger French',
    author_email='mxl1171@case.edu,sxn440@case.edu,thomas.ciardi@case.edu ,yxw1650@case.edu,rxf131@case.edu',


    # BSD 3-Clause License:
    # - http://choosealicense.com/licenses/bsd-3-clause
    # - http://opensource.org/licenses/BSD-3-Clause
    license='BSD License (BSD-3)',
    packages=find_packages(),
    include_package_data=True,
)
