import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="MSLXPluginHelper",
  version="0.0.1",
  author="MojaveHao",
  author_email="353181381@qq.com",
  description="Help you create a plugin for MSLX",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/MojaveHao/MSL-X",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3.7",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
  ],
)