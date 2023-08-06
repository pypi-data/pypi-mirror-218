from distutils.core import  setup
import setuptools
packages = ['Mission']# 唯一的包名，自己取名
setup(name='MissionData',
	version='1.0',
	author='lsw',
    packages=packages, 
    package_dir={'requests': 'requests'},)
