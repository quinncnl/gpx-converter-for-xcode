import gpxpy
import gpxpy.gpx
from gpxpy import geo


def main():
    path = 'gpxes/eindhoven.gpx'

    gpx_file = open(path, 'r')
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

    f = open("output.gpx", "w")
    f.write(gpx)
    f.close()
                                                         
main()
