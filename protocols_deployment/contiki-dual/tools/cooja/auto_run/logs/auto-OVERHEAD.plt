#!/usr/bin/env gnuplot

#set xrange  [9:60]
#set yrange [0.8:1] 
set grid ytics
set grid xtics

# get the name of the experiment folder. E.g. 1s-10m-25f 
titolo=system("echo $(basename $(dirname $PWD))")
set title titolo
set term png
set output titolo.'-OH.png'

set xlabel 'time(mins)'
set ylabel 'overhead'
  
set key bottom left

FILES = system("ls *.log")
LABEL = system("ls *.log | sed -e 's/.log//'")

plot for [i=1:words(FILES)] word(FILES,i) u 3 t word(LABEL,i)  with linespoints\

