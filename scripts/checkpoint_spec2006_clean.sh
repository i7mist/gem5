#!/bin/bash
 
GEM5_DIR=/safari/hyena/tianshi/gem5-stable                          # I set this variable to (pwd) based on the assumption that you are in gem5 working directory. /home/$(YOUR_USER_NAME)/hrm/gem5-stable
#SPEC_DIR=/safari/hyena/amirali/spec2006/benchmark                  # Install location of your SPEC2006 benchmarks
SPEC_DIR=/safari/hyena/tianshi/benchmark                  # Install location of your SPEC2006 benchmarks
#SPEC_DIR=/safari/africanswallow/yixinluo/hrm/spec2006/benchmark                  # Install location of your SPEC2006 benchmarks
 
ARGC=$# # Get number of arguments excluding arg0 (the script itself). Check for help message condition.
if [[ "$ARGC" != 4 ]]; then # Bad number of arguments.
    echo "./run_spec2006.sh BENCHMARK OUTPUT_DIR RAMULATOR_CONFIG BEGIN"
    exit
fi
 
# Get command line input. We will need to check these.
BENCHMARK=$1                    # Benchmark name, e.g. bzip2
OUTPUT_DIR=$2                   # Directory to place run output. Make sure this exists!
RAMULATOR_CONFIG=$3             # Ramulator configuration file
BEGIN=$4                        # simpoint start point
BEGIN_WARM=$((BEGIN - 100000000))
echo BEGIN_WARM $BEGIN_WARM
mkdir -p $OUTPUT_DIR/$BENCHMARK
OUTPUT_DIR=$(pwd)/$OUTPUT_DIR/$BENCHMARK

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
$GEM5_DIR/build/X86/gem5_clean.opt \
    --outdir=$OUTPUT_DIR \
    $GEM5_DIR/configs/example/spec2006_config.py \
    --benchmark=$BENCHMARK \
    --benchmark_stdout=$OUTPUT_DIR/$BENCHMARK.out \
    --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err \
    --at-instruction \
    --take-checkpoints=$BEGIN_WARM --checkpoint-dir=$OUTPUT_DIR\
    --cpu-type=atomic \
    --mem-size=4GB \
    --fastmem

