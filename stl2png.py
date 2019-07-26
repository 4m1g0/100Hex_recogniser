#!/usr/bin/python

import os
import sys
import time
import hashlib

fin = ""
fout = ""
size = ""

def main():

    m = hashlib.md5()
    m.update(fin)

    ff = "stl_to_png_%s.scad" % m.hexdigest()

    f = open(ff, "w")
    f.write("import(\"%s\");\n" % fin)
    f.write("$vpr = [ 0,0,0 ];") # set orthogonal camera
    f.close()

    cmd = "openscad -o %s.png --camera=0,0,0,0,0,0,610 --imgsize=%s,%s %s" % (fout, size, size, ff)
    os.system(cmd)

    os.remove(ff)

    sys.exit(0)

if __name__ == '__main__':

    f = open("/tmp/stl_to_png_tmp.log", "w")
    f.write("%i %s" % (len(sys.argv), sys.argv))
    f.close()

    if len(sys.argv) != 4:
        print "add args [in file] [out file] [size]"
        sys.exit(0)
    else:
        fin = sys.argv[1]
        fout = sys.argv[2]
        size = sys.argv[3]

main()
