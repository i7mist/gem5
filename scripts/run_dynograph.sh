#!/bin/zsh

GEM5_DIR=/safari/hyena/tianshi/gem5
WORKLOAD_PATH=/safari/hyena/tianshi/workloads/DynoGraph

MYARGC=$#

if [[ "$MYARGC" != 6 ]]; then
  echo "./rum_dynograph.sh GEM5_BIN WORKLOAD_NAME INPUT_NAME OUTPUT_DIR RAMULATOR_CONFIG STANDARD"
  exit
fi

GEM5_BIN=$1
WORKLOAD_NAME=$2
INPUT_NAME=$3
OUT=$4
RAMULATOR_CONFIG=$5
STANDARD=$6

# set mem-size option
#if [[ "$STANDARD" == "WideIO" ]]; then
#  MEM_SIZE="1GB"
#else
#  MEM_SIZE="4GB"
#fi

# in case the process will die of memory deficiency, we set the memory size to all DRAM standards to 4GB
MEM_SIZE="4GB"

RESULT_DIR=/safari/hyena/tianshi/characterize_result
OUTPUT_DIR=$RESULT_DIR/$OUT/$WORKLOAD_NAME/$INPUT_NAME/$STANDARD
echo $OUTPUT_DIR

mkdir -p $OUTPUT_DIR

cd $WORKLOAD_PATH

$GEM5_DIR/build/X86/$GEM5_BIN \
    --outdir=$OUTPUT_DIR \
    --remote-gdb-port=0 \
    $GEM5_DIR/configs/example/se.py \
    --cpu-type=detailed --mem-size=$MEM_SIZE \
    --mem-type=Ramulator \
    --ramulator-config=$GEM5_DIR/ext/ramulator/configs/$RAMULATOR_CONFIG.cfg \
    -c $WORKLOAD_PATH/$WORKLOAD_NAME \
    -o "$WORKLOAD_PATH/data/$INPUT_NAME" \
    --output="$OUTPUT_DIR/$WORKLOAD_NAME.$INPUT_NAME.out" \
    --errout="$OUTPUT_DIR/$WORKLOAD_NAME.$INPUT_NAME.err" \
    --caches \
    --l3cache \
    --l1d_size=32kB \
    --l2_size=256kB \
    --l3_size=8MB \
    --l1i_assoc=8 \
    --l1d_assoc=8 \
    --l2_assoc=4 \
    --l3_assoc=16 \
    --l1d_latency=4 \
    --l2_latency=12 \
    --l3_latency=36 \
    --cacheline_size=64 \
    --cpu-clock=4GHz \
    --rob_size=224 \
    --loadq_entries=72 \
    --storeq_entries=56 \

