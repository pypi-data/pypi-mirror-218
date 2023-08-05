import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name = "freq_mob",
  version = "0.11",
  author = "WenSui Liu",
  author_email = "liuwensui@gmail.com",
  description = "Monotonic Optimal Binning for Frequency Models",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/statcompute/freq_mob",
  packages = setuptools.find_packages(),
  install_requires = ['numpy', 'scipy', 'sklearn', 'lightgbm', 'tabulate'], 
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
