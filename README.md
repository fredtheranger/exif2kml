exif2kml
========

Extracts GPS data from JPGs and generates KML

=> Prerequisites

- Install Python27 (PIL doesn't have an official build for Python3+)
- Install Python Imaging Library (PIL) from http://www.pythonware.com/products/pil/
- Install SimpleKml from https://pypi.python.org/pypi/simplekml
- Install Git (optional if you want to clone the latest exif2kml files from github)
- Install Google Earth (optional if you want to view you KML file)

=> Usage

- Run 'python exif2xml.py -h' for full usage/help
- Example:
	python exif2kml.py -d ../photos/
	--or--
	python exif2kml.py ../photos/Photo1.jpg