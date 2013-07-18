'''
Simple program to extract exif GPS data (if exists) from JPG(s) and 
generate a KML file that can be loaded into Google Earth.

@date: July 2013
@author: mikec

Helpful links:
    http://www.endlesslycurious.com/2011/05/11/extracting-image-exif-data-with-python/  
    http://eran.sandler.co.il/2011/05/20/extract-gps-latitude-and-longitude-data-from-exif-using-python-imaging-library-pil/  
'''
import argparse, os, re
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from simplekml import Kml

### FUNCTIONS ###
def extract_gpsinfo_from_image(image):
    '''
    Helper function to extract the exif GPSInfo from a file
    '''
    exif = {}
    if hasattr( image, '_getexif' ):
        exifinfo = image._getexif()
        if exifinfo != None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                if decoded == 'GPSInfo':
                    gps = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps[sub_decoded] = value[t]
                        
                    exif[decoded] = gps                  
    return exif

def convert_to_degrees(value):
    '''
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format.
    From: http://eran.sandler.co.il/2011/05/20/extract-gps-latitude-and-longitude-data-from-exif-using-python-imaging-library-pil/
    '''
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)
 
    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)
 
    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)
 
    return d + (m / 60.0) + (s / 3600.0)

def get_lat_long(exif):
    '''
    Extract latitude and longitutde from exif data
    '''
    
    if 'GPSLatitude' in exif:
        latitude = convert_to_degrees(exif['GPSLatitude'])
        if 'GPSLatitudeRef' in exif and exif['GPSLatitudeRef'] != 'N':
            latitude = - latitude
    
    if 'GPSLongitude' in exif:
        longitude = convert_to_degrees(exif['GPSLongitude'])
        if 'GPSLongitude' in exif and exif['GPSLongitude'] != 'E':
            longitude = - longitude
       
    return latitude, longitude

### SETUP ###
parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to directory or file you want to use")
parser.add_argument("-d", "--directory", help="treat path as a directory, not a file", action="store_true")
parser.add_argument("-o", "--output", help="name of output file", default="output.kml")
parser.add_argument("-n", "--name", help="value of name element in KML output", default="exif2xml")
args = parser.parse_args()

# Check if path is valid directory or file
if not os.path.exists(args.path):
    print "Invalid path. Quitting."
    exit(1)

# Handle single JPG file or directory of JPG files
if args.directory:
    files = [os.path.join(args.path, f) for f in os.listdir(args.path) if re.match(r'[A-Za-z0-9-_]+.*\.(jpg|JPG)$', f)]
else:   
    files = [ args.path ]
    
### EXTRACT GPS DATA AND BUILD KML ###
kml = Kml(name=args.name)

cnt = 0
for fname in files:
    image = Image.open(fname)
    exif = extract_gpsinfo_from_image(image)
    latitude, longitude = get_lat_long(exif['GPSInfo'])
    
    print 'Adding %s at %s, %s...' % ( os.path.basename(fname), longitude, latitude )
    descr = '%s, %s' % ( longitude, latitude )
    kml.newpoint(name=os.path.basename(fname),
                description=descr,
                coords=[(longitude, latitude)])
    cnt = cnt + 1
    
kml.save(args.output)
#print kml.kml()
print '\nSuccessfully parsed %s files and generated %s' % ( cnt, args.output )