from setuptools import setup, find_packages
import os
with open("requirements.txt") as f:
	print(100*"7")
	install_requires = f.read().strip().split("\n")
	print(100*"6")
# get version from __version__ variable in slnee/__init__.py
from slnee import __version__ as version

setup(
	name="slnee",
	version=version,
	description="Custom apps developed by Slnee engineers",
	author="Weslati Baha Eddine",
	author_email="baha@slnee.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
os.system("sudo apt-get install libzbar0")
print(100*"5")
