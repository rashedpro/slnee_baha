from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

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
