#!/bin/bash
export GEM5_DIR=/safari/hyena/tianshi/gem5-stable
export M5_PATH=/safari/hyena/tianshi/gem5-stable/fs_bin

#$1 gem5 binary
#$2 output dir

MYARGC=$#
if [[ "$MYARGC" != 2 ]]; then
  echo "./run_full_sys.sh gem5_binary output_dir"
  exit
fi

mkdir -p $2

#atomic m5_checkpoint
CPU_TYPE=atomic

BIN=/safari/hyena/tianshi/gem5-stable/build/X86/$1

#for initial run, to get checkpoint after boot 
# $1 -d $2  configs/example/fs.py --cpu-type=$CPU_TYPE --num-cpus=1  --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux_x86_16GB  # -r 1 --restore-with-cpu=detailed

#$1 -d $2  configs/example/fs.py --cpu-type=$CPU_TYPE --script=./configs/boot/memcached.rcS --num-cpus=2  --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux_x86_16GB  --mem-type=ramulator --mem-size=3GB --ramulator-config=$GEM5_DIR/ext/ramulator/configs/gem5-config.cfg --caches --l2cache --l1d_size=32kB --l2_size=256kB --l1d_assoc=8 --l2_assoc=8 --cacheline_size=64

#$BIN -d $2 --remote-gdb-port=0 configs/example/fs.py --cpu-type=$CPU_TYPE --num-cpus=8  --kernel=$M5_PATH/binaries/vmlinux-2.6.32 --disk-image=$M5_PATH/disks/linux_x86_16GB_java --caches

#$BIN -d $2 --remote-gdb-port=0  configs/example/fs.py --cpu-type=$CPU_TYPE --num-cpus=2 --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux_x86_16GB_java --dual

$BIN -d $2 --remote-gdb-port=0 configs/example/fs.py --cpu-type=$CPU_TYPE --num-cpus=2 --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.22.9 --disk-image=$M5_PATH/disks/linux_x86_16GB --dual --etherdump=etherdump.txt

# $BIN -d $2  configs/example/fs.py --cpu-type=$CPU_TYPE --num-cpus=1 --kernel=$M5_PATH/binaries/vmlinux --disk-image=$M5_PATH/disks/test.img

#$1 -d $2  configs/example/fs.py --num-cpus=1  --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux_x86_16GB  --mem-type=ramulator --mem-size=3GB --ramulator-config=$GEM5_DIR/ext/ramulator/configs/gem5-config.cfg --caches --l2cache --l1d_size=32kB --l2_size=256kB --l1d_assoc=8 --l2_assoc=8 --cacheline_size=64 -r 1 --restore-with-cpu=detailed

#$1 -d $2  configs/example/fs.py --cpu-type=$CPU_TYPE --num-cpus=1  --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux_x86_16GB  --caches --l2cache --l1d_size=32kB --l2_size=256kB --l1d_assoc=8 --l2_assoc=8 --cacheline_size=64 # -r 2 --restore-with-cpu=detailed

#$1 -d $2  configs/example/fs.py --cpu-type=timing --num-cpus=2 --mem-type=HMC_2500_x32 --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux_x86_16GB_2 -r 1 --restore-with-cpu=atomic

#NVMain conf
#$1 -d $2  configs/example/fs.py --cpu-type=$CPU_TYPE $PIM --num-cpus=2 --mem-type=NVMainMemory --nvmain-config=nvmain_hmc.config --nvmain-StatsFile=$2/nvstats.st --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux-x86.img --restore-with-cpu=timing -r 1 --ruby #--caches #--l2cache --l1d_size=64kB --l1i_size=64kB --l1d_assoc=4 --cacheline_size=64 --restore-with-cpu=atomic -r 1

#Ramulator conf --mem-size=8GB 
#$1 -d $2  configs/example/fs.py --cpu-type=$CPU_TYPE --num-cpus=2 --mem-type=Ramulator --ramulator-config=gem5-ramulator.cfg --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux_x86_16GB_2 --restore-with-cpu=$CPU_TYPE -r 1 --ruby #--caches #--l2cache --l1d_size=64kB --l1i_size=64kB --l1d_assoc=4 --cacheline_size=64 --restore-with-cpu=atomic -r 1

#./build/X86/gem5.opt configs/example/fs.py --num-cpus=4 --kernel=/home/amirali/gem5Ramulator/fullSystem_images/binaries/x86_64-vmlinux-2.6.22.9.smp --disk-image=/home/amirali/gem5Ramulator/fullSystem_images/disks/linux-x86-new.img 

#./build/X86/gem5.opt --debug-flags=RubyPim,PIM,RubyMemory configs/example/fs.py --num-cpus=4 --kernel=/home/amirali/gem5Ramulator/fullSystem_images/binaries/x86_64-vmlinux-2.6.22.9.smp --disk-image=/home/amirali/gem5Ramulator/fullSystem_images/disks/linux-x86-new.img --restore-with-cpu=timing --ruby -r 1


#run -d ./pim_out/ configs/example/fs.py --cpu-type=detailed --pim-cpu-type=detailed --mem-type=Ramulator --ramulator-config=gem5-ramulator.cfg --num-cpus=2 --kernel=$M5_PATH/binaries/x86_64-vmlinux-2.6.32-smp --disk-image=$M5_PATH/disks/linux-x86.img --restore-with-cpu=timing -r 1 --ruby

