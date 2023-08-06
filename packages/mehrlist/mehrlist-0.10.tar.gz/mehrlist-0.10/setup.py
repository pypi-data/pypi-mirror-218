from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''Subclass of list with more than 100 useful methods - pure Python'''

# Setting up
setup(
    name="mehrlist",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/mehrlist',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['bisectsearch', 'catmapper', 'flatten_any_dict_iterable_or_whatsoever', 'flatten_everything', 'intersection_grouper', 'isiter', 'levelflatten', 'list2tree', 'nested2nested', 'screwhashesset', 'tolerant_isinstance'],
    keywords=['nested', 'list'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['bisectsearch', 'catmapper', 'flatten_any_dict_iterable_or_whatsoever', 'flatten_everything', 'intersection_grouper', 'isiter', 'levelflatten', 'list2tree', 'nested2nested', 'screwhashesset', 'tolerant_isinstance'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*