#!/usr/bin/env gnuplot

set xrange  [5:60]
set yrange [50:65] 
set grid ytics
set grid xtics

# get the name of the experiment folder. E.g. 1s-10m-25f 
titolo=system("echo $(basename $(dirname $PWD))")
set title titolo
set term png
set output titolo.'-PDR.png'

set xlabel 'time(mins)'
set ylabel 'PDR'
  
set key bottom right

FILES = system("ls *.log")
LABEL = system("ls *.log | sed -e 's/.log//'")

plot for [i=1:words(FILES)] word(FILES,i) u 2 t word(LABEL,i)  with linespoints\

#plot '1s-50m-10f-De.csc-1.log' u 2 t 'Default'  with linespoints,\

