#!/bin/zsh

MYARGC=$#

EXTRACT_PATH=/safari/hyena/tianshi/extract_stats.sh

if [[ "$MYARGC" != 2 ]]; then
  echo "./extract_gem5_stats.sh INDEX STATS_DIR"
  exit
fi

INDEX=$1
STATS_DIR=$(pwd)/$2

specname=(perlbench
bzip2
gcc
bwaves
gamess
mcf
milc
zeusmp
gromacs
cactusADM
leslie3d
namd
gobmk
dealII
soplex
povray
calculix
hmmer
sjeng
GemsFDTD
libquantum
h264ref
tonto
lbm
omnetpp
astar
wrf
sphinx3
xalancbmk
)

for item in "${specname[@]}"; do
  $EXTRACT_PATH " " $INDEX "$STATS_DIR/$item""/stats.txt"
done
