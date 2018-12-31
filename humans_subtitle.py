import datetime
import re

timecode = lambda delt: "%02d:%02d:%02d,%03d" % (
    delt.seconds//3600, (delt.seconds//60)%60, delt.seconds%60,
    (delt.microseconds+500)//1000)

def doit():
    """Open humans_list.txt, get file names, print out Matroska SRT file"""
    f = open("humans_list.txt")
    vt1 = datetime.timedelta()
    ifile = 0
    dt100ms = datetime.timedelta(0,0,100000)
    appeardelay = dt100ms
    fadeearly = dt100ms
    appeardelay_walk = datetime.timedelta(0,0,33334)
    for line in f:
        if not line.startswith("file '"):
            continue
        ifile += 1
        m = re.search(r'/m([0-9]{8}_[0-9]{6}_[0-9]{3})\.mp4', line)
        if not m:
            print("Bad line %s" % line)
            continue
        g = m.groups()
        if len(g) != 1:
            print("Bad match "+g)
            continue
        ttext = g[0]
        path = line[6:m.start()]
        fcsv = open("%s/c%s.csv" % (path,ttext))
        line1 = next(fcsv)
        assert(line1[19] == ',')
        ttext1 = line1[0:19]
        for line in fcsv:
            if line[19] == ',':
                line2 = line
        ttext2 = line2[0:19]
        assert(ttext2 > ttext)
        assert(ttext1 <= ttext)
        t1 = datetime.datetime.strptime(ttext1+"+0000", '%Y%m%d_%H%M%S_%f%z')
        t2 = datetime.datetime.strptime(ttext2+"+0000", '%Y%m%d_%H%M%S_%f%z')
        vt2 = vt1 + (t2-t1)
        print(ifile)
        print("%s --> %s" % (timecode(vt1+appeardelay),
                             timecode(vt2-fadeearly)))
        print(t1.strftime('%Y-%m-%d %H:%M:%S UTC'))
        print("")
        vt1 = vt2
        appeardelay += appeardelay_walk
    print("")

if __name__ == "__main__":
    doit()
