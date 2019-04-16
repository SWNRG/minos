#!/usr/bin/env gnuplot

set xrange  [6:]
#set yrange [0.8:1] 
set grid ytics
set grid xtics

#DON'T FORGET TO SET Id=?

# get the name of the experiment folder. E.g. 1s-10m-25f 
titolo1 = system ("pwd | rev | cut -d '/' -f 2 | rev")
titolo2 = system ("pwd | rev | cut -d '/' -f 1 | rev")

titlo = titolo1.'-'.titolo2[6:]
set title titlo

set term png
set output titlo.'-OH.png'

set xlabel 'Time (min)'
set ylabel 'OverHead (OH)'
  
set key bottom left

FILES = system("ls *.log")
LABEL = system("ls *.log | sed -e 's/-1hr.csc.log//'")

plot for [i=1:words(FILES)] word(FILES,i) u 3 t word(LABEL,i)  with linespoints\

