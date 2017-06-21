from setuptools import setup, find_packages
setup(
    name="icmparser",
    version="0.1",
    packages=find_packages(),
    install_requires=[
      'haversine',
      'Pillow'
    ],
    package_data={
      'icmparser.fonts': ['*.png']
    }
)
