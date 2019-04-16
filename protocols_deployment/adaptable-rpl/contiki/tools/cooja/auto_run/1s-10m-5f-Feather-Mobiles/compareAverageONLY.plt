set title "Network with 1 fixed sink 5 mobile and 5 static\nMobile Nodes Only"

set ylabel "Packet Delivery Ratio (PDR) %"
set style fill solid border 0
set boxwidth 0.4
set key off #center below
set style histogram gap 0 clustered #rowstacked
set style data histograms

set xrange [0.8:1.7]
set yrange [0:40]

titolo1 = system ("pwd | rev | cut -d '/' -f 2 | rev")
titolo2 = system ("pwd | rev | cut -d '/' -f 1 | rev")

titlo = titolo1[:8].'-'.titolo2[13:]
#set title titlo

set term png
set output titlo.'Only-AVERAGE-PDR.png'

set size ratio 1
set grid ytics
set xtics ("Adaptive Scenario" 1, "Default Scenario" 1.5)

plot "average-Adaptive-Defaute-Compares" u 2 lt rgb "#406090" fillstyle pattern 1 ,\
"" u 3 ti "Default Scenario" lt rgb "#40FF00" fillstyle pattern 4 
# plot "average-Adaptive-Defaute-Compares" u ($0-.05):2:xtic(1) ti "Default Scenario" lt rgb "#406090" fillstyle pattern 1 # ,\
#"" u ($0+0.25):2 ti "Adaptive Scenario" lt rgb "#40FF00" fillstyle pattern 4 

