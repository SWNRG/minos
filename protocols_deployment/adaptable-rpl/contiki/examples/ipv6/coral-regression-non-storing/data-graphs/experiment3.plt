#!/usr/bin/env gnuplot

set xrange  [0:60]
set yrange [10000:22000] 
set grid ytics
set grid xtics

set title "experiment3-Point2Point"

set term png
set output "experiment3-Point2Point".'.png'

set xlabel 'Time (min)'
set ylabel 'RTT (ms)'

set arrow from 20, graph 0 to 20, graph 1 nohead lc rgb "red" 
set label "          Change\n  Objective Function"  at  21,21000 textcol rgb "red"
set arrow from 40, graph 0 to 40, graph 1 nohead lc rgb "red" 

plot "experiment3.log" u 2 t "Node 5" with linespoints\

