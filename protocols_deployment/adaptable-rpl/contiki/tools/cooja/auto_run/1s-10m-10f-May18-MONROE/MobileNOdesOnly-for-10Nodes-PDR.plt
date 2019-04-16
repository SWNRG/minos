#!/usr/bin/env gnuplot

set grid ytics
set grid xtics

A = "#32CD32"
B = "#A52A2A"

# get the name of the experiment folder. E.g. 1s-10m-25f 
# new var, only the name of the containing folder
titolo1 = system ("pwd | rev | cut -d '/' -f 2 | rev")
titolo2 = system ("pwd | rev | cut -d '/' -f 1 | rev")

titlo = titolo1[:11].'-'.titolo2[13:]
set title titlo

set term png
set output titlo.'-PDR.png'

set xlabel 'Mobile Nodes'
set ylabel 'PDR'

set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"
set style histogram gap 1  clustered

set ylabel "PDR"

#set xtic offset 1

set style fill solid border 0
set boxwidth 0.0
set key center below
#set xrange [-.5:4.5]
#set yrange [0:130]

set style data histogram 

FILES = system("ls *.log")
LABEL = system("ls *.log | sed -e 's/-1hr.csc.log//'")

plot word(FILES,1) u 2:xtic(1) t "Adaptable Scenario" fc rgb A fillstyle pattern 1 ,\
     word(FILES,2) u 2 t "Default Scenario" fc rgb B fillstyle pattern 2

