#!/bin/zsh

# 1B detailed
export OUTPUT_DIR=characterize/spec_outdir/DDR3
export RAMULATOR_CONFIG=DDR3-config
parallel -P6 -a cmds_list

export OUTPUT_DIR=characterize/spec_outdir/DDR4
export RAMULATOR_CONFIG=DDR4-config
parallel -P6 -a cmds_list

export OUTPUT_DIR=characterize/spec_outdir/LPDDR3
export RAMULATOR_CONFIG=LPDDR3-config
parallel -P6 -a cmds_list

export OUTPUT_DIR=characterize/spec_outdir/LPDDR4
export RAMULATOR_CONFIG=LPDDR4-config
parallel -P6 -a cmds_list

export OUTPUT_DIR=characterize/spec_outdir/GDDR5
export RAMULATOR_CONFIG=GDDR5-config
parallel -P6 -a cmds_list

export OUTPUT_DIR=characterize/spec_outdir/WIDEIO
export RAMULATOR_CONFIG=WideIO-config
parallel -P6 -a cmds_list

export OUTPUT_DIR=characterize/spec_outdir/WIDEIO2
export RAMULATOR_CONFIG=WideIO2-config
parallel -P6 -a cmds_list

export OUTPUT_DIR=characterize/spec_outdir/HBM
export RAMULATOR_CONFIG=HBM-config
parallel -P6 -a cmds_list
