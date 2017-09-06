#!/usr/bin/env python3

import sys, os
import gpxpy
import gpxpy.gpx
from gpxpy import geo


def convert(file):
    path = file

    gpx_file = open(path, 'r')

    print(gpx_file)
    
    gpx = gpxpy.parse(gpx_file)

    points = []
    
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))

    ret = []

    for it in range(0, len(points) - 1):
        v = (points[it][0], points[it][1], points[it+1][0], points[it+1][1])
        distance = geo.haversine_distance(v[0], v[1], v[2], v[3])
        div = distance / 2
        count = int(div)

        if count == 0:
            ret.append((v[0], v[1]))

        else:
            
            a = (v[2] - v[0]) / count
            b = (v[3] - v[1]) / count

            for i in range(0, count):
                new = (v[0] + i * a, v[1] + i * b)
                ret.append(new)

            ret.append((v[2], v[3]))

    gpx = """<?xml version="1.0"?>
<gpx version="1.1" creator="Xcode">
"""

    for it in range(0, len(ret)):
        gpx += '<wpt lat="'+str(ret[it][0])+'" lon="'+str(ret[it][1])+'"></wpt>\n'

    gpx += """
</gpx>"""

    f = open(path + ".converted.gpx", "w")
    f.write(gpx)
    f.close()

def main():

    if len(sys.argv) == 1:
        print("This program requires at least one parameter")
        sys.exit(1)

    for path in sys.argv:

        if path == sys.argv[0]:
            continue
        
        if os.path.isdir(path):
            # Iterate the root directory recursively using os.walk and for each video file present get the subtitle
            for dir_path, _, file_names in os.walk(path):
                for filename in file_names:
                    file_path = os.path.join(dir_path, filename)
                    convert(file_path)
        else:
            convert(path)

            
if __name__ == '__main__':
    main()
