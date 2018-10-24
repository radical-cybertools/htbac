mol load pdb /net/dirac/mnt/store7/dave/janssen/store/pde2/4d08/com/drug/j1/j1/build/complex.pdb
set a [atomselect top all]

set outfile [open tmp_cbv w]
set minmax [measure minmax $a]
set boxsize [vecsub [lindex $minmax 1] [lindex $minmax 0]]
set centre [measure center $a]

puts $outfile $boxsize
puts $outfile $centre

close $outfile

$a set beta 0
$a set occupancy 0
set b [atomselect top "(resid 1 to 344) and noh"]
$b set beta 4
set z [atomselect top "(not (resid 1 to 344) and not water and not type IM) and noh"]
$z set beta 4


$a writepdb /net/dirac/mnt/store7/dave/janssen/store/pde2/4d08/com/drug/j1/j1/constraint/f4.pdb

quit
