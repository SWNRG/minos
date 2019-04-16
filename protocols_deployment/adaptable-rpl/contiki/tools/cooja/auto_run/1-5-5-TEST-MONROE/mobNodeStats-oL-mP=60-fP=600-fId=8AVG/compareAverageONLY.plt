#!/usr/bin/gnuplot

set ylabel "Packet Delivery Ratio (PDR) %"
set xlabel "Node Id"
set style fill solid border 0
set boxwidth 01

set key center below
set style histogram gap 0 clustered #rowstacked
set style data histograms

#set xrange [-2.5:5.5]
#set yrange [0:50]

titolo1 = system ("pwd | rev | cut -d '/' -f 2 | rev")
titolo2 = system ("pwd | rev | cut -d '/' -f 1 | rev")

titlo = titolo1[:8].'-'.titolo2[13:]
set title titlo

set term png
set output titlo.'.png' #.'Only-AVERAGE-PDR.png'

set size ratio 1
set grid ytics

FILES = system("ls mobNode*.log")
LABEL = system("ls *.log | sed -e 's/-RX100%-1hr.csc.log//'")

plot for [i=1:words(FILES)] word(FILES,i) u 2:xtic(1) t word(LABEL,i) fillstyle pattern i # with linespoints\

