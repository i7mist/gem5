#!/bin/bash
 
GEM5_DIR=/safari/hyena/tianshi/gem5
SPEC_DIR=/safari/hyena/tianshi/benchmark                  # Install location of your SPEC2006 benchmarks
#SPEC_DIR=/safari/africanswallow/yixinluo/hrm/spec2006/benchmark                  # Install location of your SPEC2006 benchmarks
RESULT_DIR=/safari/hyena/tianshi/characterize_result
 
ARGC=$# # Get number of arguments excluding arg0 (the script itself). Check for help message condition.
if [[ "$ARGC" != 6 ]]; then # Bad number of arguments.
    echo "./run_spec2006.sh BIN BENCHMARK OUTPUT_DIR RAMULATOR_CONFIG RESTORE_POINT STANDARD"
    exit
fi
 
# set warmup length
WARMUP_LENGTH=100000000

# Get command line input. We will need to check these.
BIN=$1
BENCHMARK=$2                    # Benchmark name, e.g. bzip2
OUT=$3                   # Directory to place run output. Make sure this exists!
RAMULATOR_CONFIG=$4             # Ramulator configuration file
RESTORE_POINT=$5
STANDARD=$6
RESTORE_POINT_WARM=$((RESTORE_POINT - WARMUP_LENGTH)) # restore point before warm region
echo RESTORE_POINT_WARM $RESTORE_POINT_WARM
OUTPUT_DIR=$RESULT_DIR/$OUT/$BENCHMARK/$STANDARD
mkdir -p $OUTPUT_DIR
# CHECKPOINT_DIR=$GEM5_DIR/$OUT/checkpoints
CHECKPOINT_DIR=/safari/hyena/tianshi/tmp/gem5-stable/characterize/spec_outdir/checkpoints
CMDTRACE_DIR=$RESULT_DIR/$OUT/$BENCHMARK/cmdtrace/$STANDARD
mkdir -p $CMDTRACE_DIR

# set mem-size option in gem5
# if [[ "$STANDARD" == "WideIO" ]]; then
#  MEM_SIZE=1GB
# else
#  MEM_SIZE=4GB
# fi

# in case the process fails due to running out of memory, we set memory size belong to all DRAM to 4GB
MEM_SIZE="4GB"

######################### BENCHMARK CODENAMES ####################
PERLBENCH_CODE=400.perlbench
BZIP2_CODE=401.bzip2
GCC_CODE=403.gcc
BWAVES_CODE=410.bwaves
GAMESS_CODE=416.gamess
MCF_CODE=429.mcf
MILC_CODE=433.milc
ZEUSMP_CODE=434.zeusmp
GROMACS_CODE=435.gromacs
CACTUSADM_CODE=436.cactusADM
LESLIE3D_CODE=437.leslie3d
NAMD_CODE=444.namd
GOBMK_CODE=445.gobmk
DEALII_CODE=447.dealII
SOPLEX_CODE=450.soplex
POVRAY_CODE=453.povray
CALCULIX_CODE=454.calculix
HMMER_CODE=456.hmmer
SJENG_CODE=458.sjeng
GEMSFDTD_CODE=459.GemsFDTD
LIBQUANTUM_CODE=462.libquantum
H264REF_CODE=464.h264ref
TONTO_CODE=465.tonto
LBM_CODE=470.lbm
OMNETPP_CODE=471.omnetpp
ASTAR_CODE=473.astar
WRF_CODE=481.wrf
SPHINX3_CODE=482.sphinx3
XALANCBMK_CODE=483.xalancbmk
SPECRAND_INT_CODE=998.specrand
SPECRAND_FLOAT_CODE=999.specrand
 
#################### BENCHMARK CODE MAPPING ######################
BENCHMARK_CODE="none"
 
if [[ "$BENCHMARK" == "perlbench" ]]; then
    BENCHMARK_CODE=$PERLBENCH_CODE
    BENCHMARK_START=541
fi
if [[ "$BENCHMARK" == "bzip2" ]]; then
    BENCHMARK_CODE=$BZIP2_CODE
    BENCHMARK_START=368
fi
if [[ "$BENCHMARK" == "gcc" ]]; then
    BENCHMARK_CODE=$GCC_CODE
    BENCHMARK_START=64
fi
if [[ "$BENCHMARK" == "bwaves" ]]; then
    BENCHMARK_CODE=$BWAVES_CODE
    BENCHMARK_START=680
fi
if [[ "$BENCHMARK" == "gamess" ]]; then
    BENCHMARK_CODE=$GAMESS_CODE
    BENCHMARK_START=48
fi
if [[ "$BENCHMARK" == "mcf" ]]; then
    BENCHMARK_CODE=$MCF_CODE
    BENCHMARK_START=370
fi
if [[ "$BENCHMARK" == "milc" ]]; then
    BENCHMARK_CODE=$MILC_CODE
    BENCHMARK_START=272
fi
if [[ "$BENCHMARK" == "zeusmp" ]]; then
    BENCHMARK_CODE=$ZEUSMP_CODE
    BENCHMARK_START=405
fi
if [[ "$BENCHMARK" == "gromacs" ]]; then
    BENCHMARK_CODE=$GROMACS_CODE
    BENCHMARK_START=1
fi
if [[ "$BENCHMARK" == "cactusADM" ]]; then
    BENCHMARK_CODE=$CACTUSADM_CODE
    BENCHMARK_START=81
fi
if [[ "$BENCHMARK" == "leslie3d" ]]; then
    BENCHMARK_CODE=$LESLIE3D_CODE
    BENCHMARK_START=176
fi
if [[ "$BENCHMARK" == "namd" ]]; then
    BENCHMARK_CODE=$NAMD_CODE
    BENCHMARK_START=1527
fi
if [[ "$BENCHMARK" == "gobmk" ]]; then
    BENCHMARK_CODE=$GOBMK_CODE
    BENCHMARK_START=133
fi
if [[ "$BENCHMARK" == "dealII" ]]; then # DOES NOT WORK
    BENCHMARK_CODE=$DEALII_CODE
    BENCHMARK_START=1387
fi
if [[ "$BENCHMARK" == "soplex" ]]; then
    BENCHMARK_CODE=$SOPLEX_CODE
    BENCHMARK_START=382
fi
if [[ "$BENCHMARK" == "povray" ]]; then
    BENCHMARK_CODE=$POVRAY_CODE
    BENCHMARK_START=160
fi
if [[ "$BENCHMARK" == "calculix" ]]; then
    BENCHMARK_CODE=$CALCULIX_CODE
    BENCHMARK_START=4433
fi
if [[ "$BENCHMARK" == "hmmer" ]]; then
    BENCHMARK_CODE=$HMMER_CODE
    BENCHMARK_START=942
fi
if [[ "$BENCHMARK" == "sjeng" ]]; then
    BENCHMARK_CODE=$SJENG_CODE
    BENCHMARK_START=477
fi
if [[ "$BENCHMARK" == "GemsFDTD" ]]; then
    BENCHMARK_CODE=$GEMSFDTD_CODE
    BENCHMARK_START=1060
fi
if [[ "$BENCHMARK" == "libquantum" ]]; then
    BENCHMARK_CODE=$LIBQUANTUM_CODE
    BENCHMARK_START=2666
fi
if [[ "$BENCHMARK" == "h264ref" ]]; then
    BENCHMARK_CODE=$H264REF_CODE
    BENCHMARK_START=8
fi
if [[ "$BENCHMARK" == "tonto" ]]; then
    BENCHMARK_CODE=$TONTO_CODE
    BENCHMARK_START=44
fi
if [[ "$BENCHMARK" == "lbm" ]]; then
    BENCHMARK_CODE=$LBM_CODE
    BENCHMARK_START=13
fi
if [[ "$BENCHMARK" == "omnetpp" ]]; then
    BENCHMARK_CODE=$OMNETPP_CODE
    BENCHMARK_START=477
fi
if [[ "$BENCHMARK" == "astar" ]]; then
    BENCHMARK_CODE=$ASTAR_CODE
    BENCHMARK_START=185
fi
if [[ "$BENCHMARK" == "wrf" ]]; then
    BENCHMARK_CODE=$WRF_CODE
    BENCHMARK_START=2694
fi
if [[ "$BENCHMARK" == "sphinx3" ]]; then
    BENCHMARK_CODE=$SPHINX3_CODE
    BENCHMARK_START=3195
fi
if [[ "$BENCHMARK" == "xalancbmk" ]]; then # DOES NOT WORK
    BENCHMARK_CODE=$XALANCBMK_CODE
    BENCHMARK_START=178
fi
if [[ "$BENCHMARK" == "specrand_i" ]]; then
    BENCHMARK_CODE=$SPECRAND_INT_CODE
    BENCHMARK_START=0
fi
if [[ "$BENCHMARK" == "specrand_f" ]]; then
    BENCHMARK_CODE=$SPECRAND_FLOAT_CODE
    BENCHMARK_START=0
fi
 
# Sanity check
if [[ "$BENCHMARK_CODE" == "none" ]]; then
    echo "Input benchmark selection $BENCHMARK did not match any known SPEC CPU2006 benchmarks! Exiting."
    exit 1
fi

# Check OUTPUT_DIR existence
if [[ !(-d "$OUTPUT_DIR") ]]; then
    echo "Output directory $OUTPUT_DIR does not exist! Exiting."
    exit 1
fi
 
RUN_DIR=$SPEC_DIR/benchspec/CPU2006/$BENCHMARK_CODE/run/run_base_ref\_amd64-m64-gcc42-nn.0000     # Run directory for the selected SPEC benchmark
echo $RUN_DIR
cd $RUN_DIR 

# execute Gem5 
$GEM5_DIR/build/X86/$BIN \
    --outdir=$OUTPUT_DIR \
    --remote-gdb-port=0 \
    $GEM5_DIR/configs/example/spec2006_config.py \
    --benchmark=$BENCHMARK \
    --benchmark_stdout=$OUTPUT_DIR/$BENCHMARK.out \
    --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err \
    --at-instruction \
    --warmup-insts=$WARMUP_LENGTH \
    -r $RESTORE_POINT_WARM --checkpoint-dir=$CHECKPOINT_DIR/$BENCHMARK\
    -I 1000000000 \
    --cpu-type=detailed \
    --mem-type=Ramulator \
    --mem-size=$MEM_SIZE \
    --ramulator-config=$GEM5_DIR/ext/ramulator/configs/$RAMULATOR_CONFIG.cfg \
    --ramulator-mem-trace=$CMDTRACE_DIR/$BENCHMARK-$STANDARD- \
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



