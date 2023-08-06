from setuptools import setup

# Read contents of README.md file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
      name='onedriveintegrate',
      version='1.2',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='Package for OneDrive File Management',
      author='William Guo',
      license='MIT',
      packages=['onedriveintegrate'],
      zip_safe=False
)