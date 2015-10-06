#!/bin/zsh

M5_PATH=/safari/hyena/tianshi/gem5-stable
WORKLOAD_PATH=/safari/hyena/tianshi/workloads/DynoGraph

MYARGC=$#

if [[ "$MYARGC" != 4 ]]; then
  echo "./rum_dynograph.sh GEM5_BIN WORKLOAD_NAME INPUT_NAME STANDARD"
  exit
fi

GEM5_BIN=$1
WORKLOAD_NAME=$2
INPUT_NAME=$3
STANDARD=$4

INTERVAL_LENGTH=1000000000
WARMUP_LENGTH=100000000

# set mem-size option
#if [[ "$STANDARD" == "WideIO" ]]; then
#  MEM_SIZE="1GB"
#else
#  MEM_SIZE="4GB"
#fi

# in case the process will die of memory deficiency, we set the memory size to all DRAM standards to 4GB
MEM_SIZE="4GB"

OUTPUT_DIR=/safari/hyena/tianshi/gem5-stable/characterize/workloads_outdir/DynoGraph/$WORKLOAD_NAME/$INPUT_NAME/$STANDARD

mkdir -p $OUTPUT_DIR

# TODO finish config file for all DRAM 
RAMULATOR_CONFIG="$STANDARD"-config

# restore checkpoint

$M5_PATH/build/X86/$GEM5_BIN \
    --outdir=$OUTPUT_DIR \
    --remote-gdb-port=0 \
    $M5_PATH/configs/example/se.py \
    --cpu-type=detailed --mem-size=$MEM_SIZE \
    --mem-type=ramulator \
    --ramulator-config=$M5_PATH/ext/ramulator/configs/$RAMULATOR_CONFIG.cfg \
    --caches \
    --l3cache \
    --l1d_size=32kB \
    --l2_size=256kB \
    --l3_size=8MB \
    --l1d_assoc=8 \
    --l2_assoc=8 \
    --l3_assoc=8 \
    --cacheline_size=64 \
    -c $WORKLOAD_PATH/$WORKLOAD_NAME \
    -o "$WORKLOAD_PATH/data/$INPUT_NAME" \
    --output="$OUTPUT_DIR/$WORKLOAD_NAME.$INPUT_NAME.out" \
    --errout="$OUTPUT_DIR/$WORKLOAD_NAME.$INPUT_NAME.err"
