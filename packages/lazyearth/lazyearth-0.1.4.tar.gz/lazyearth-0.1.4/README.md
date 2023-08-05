<img src="https://lazyearth.org/logo/logo_on_PyPI.svg" width=100%>

# Lazyearth: Python earth science package
[![Package Status](https://img.shields.io/pypi/status/pandas.svg)](https://pypi.org/project/lazyearth/)
[![Downloads](https://static.pepy.tech/badge/lazyearth/month)](https://pepy.tech/project/lazyearth)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it?
Lazyearth is a Python package that offers ease and speed in analyzing geospatial data. Lazyearth was designed to support the functions of the Open Data Cube, which primarily aggregates aerial satellite imagery, but it can also operate on personal computers. The purpose of creating Lazyearth is for it to become a widely used tool in the field of geoscience.
<ul>
<li>Website : <a href="https://lazyearth.org/">https://lazyearth.org/</a></li>
<li>PyPI : <a href="https://pypi.org/project/lazyearth/">https://pypi.org/project/lazyearth/</a></li>
<li>Mailing : <a href="Tun.k@ku.th">Tun.k@ku.th</a></li>
<li>Bug reports : <a href="https://github.com/Tun555/lazyearth/issues">https://github.com/Tun555/lazyearth/issues</a></li>
<li>learn : <a href="https://lazyearth.org/install/learn/">https://lazyearth.org/install/learn</a></li>
</ul>

## Installation
If you want to work on a personal computer, you need to install the GDAL package first
Open command prompt
```python
conda install -c conda-forge gdal
```
However, if you want to work on Open Data Cube or Google Colab, you can get started immediately.
The latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/lazyearth)
```python
# PyPI
pip install lazyearth
```

## Main Features
<ul>
    <li>Opening and Saving : It can open various types of images and save them easily in multiple formats after processing.</li>
    <li>Image plotting : This feature supports the display of a diverse range of images for single or comparative purposes. It can accommodate various formats, such as 1 or 3-dimensional numpy arrays, as well as xarray.</li>
    <li>Band combination : It can easily blend different color bands of satellite images</li>
    <li>Remote Sensing Calculation: There are multiple calculation indices such as NDVI, EVI, BSI etc.</li>
    <li>Water: This features water analysis, including water detection and water quality.</li>
</ul>



