#!/bin/bash
for stl in stls/*.stl; do
    imgName=images/$(basename $stl)
    ./stl2png.py $stl $imgName 620
    convert $imgName.png -threshold 90% -negate $imgName.png
    convert $imgName.png -flop $imgName-mirror.png
    #read -n1 -r -p "Press any key to continue..." key
done
