import sys

raw_cycles = {}
raw_data = {}

tCK = [(3/0.4)/8, (3/0.4)/9, (3/0.4)/8, 2.5/4, 8.0/14, 5.0*3/4, 2.5*3/4, 2.0]
raw_cycles["tRC"] = [49, 57, 64, 95, 70, 16, 33, 24]
raw_cycles["tRP"] = [13, 18, 20, 27, 21, 5, 10, 7] # or nRPpb
raw_cycles["tRCDR"] = [13, 18, 20, 29, 21, 5, 10, 7]
raw_cycles["tRCDW"] = [13, 18, 20, 29, 18, 5, 10, 6]
raw_cycles["tCL"] = [13, 18, 16, 32, 21, 3, 9, 7]
raw_cycles["tBL"] = [4, 4, 4, 8, 2, 4, 2, 2]
raw_cycles["tDQSCK"] = [0, 0, 3, 3, 0, 1, 1, 0]
raw_cycles["tRFC"] = [171, 192, 139, 288, 280, 56, 96, 130] # or nRFCab
# GDDR5 RFC using DDR3 values
raw_cycles["tREFI"] = [8320, 9360, 4160, 6247, 6825, 520, 2080, 1950]
# HBM nREFI1B?
raw_data["row_buffer_size(Byte)"] = [1<<11, 1<<11, 1<<12, 1<<11, 1<<11, 1<<11, 1<<12, 1<<11]
# for WideIO2, the implementation doubles the channel width so maybe we need to double the row buffer size also?

out_f = open(sys.argv[1], "w")

standards = ["DDR3", "DDR4", "LPDDR3", "LPDDR4", "GDDR5", "WideIO", "WideIO2", "HBM"]

care_of_specs = ["tRC", "tRP", "tRCDR", "tRCDW", "tCL", "tBL", "tDQSCK", "read_latency", "tRFC", "tREFI", "row_buffer_size(Byte)"]

out_f.write("," + ",".join(care_of_specs) + "\n")

for i in range(len(standards)):
  dram = standards[i]
  results = []
  results.append(dram)
  tck = tCK[i]
  for spec in care_of_specs:
    if raw_cycles.has_key(spec):
      if len(raw_cycles[spec]) > i:
        results.append(raw_cycles[spec][i] * tck)
      else:
        results.append("")
    elif raw_data.has_key(spec):
      if len(raw_data[spec]) > i:
        results.append(raw_data[spec][i])
      else:
        results.append("")
    elif spec == "read_latency":
      if dram == "LPDDR3" or dram == "LPDDR4" or dram == "WideIO" or dram == "WideIO2":
        results.append((raw_cycles["tCL"][i] + raw_cycles["tBL"][i] + raw_cycles["tDQSCK"][i]) * tck)
      else:
        results.append(raw_cycles["tCL"][i] * tck + raw_cycles["tBL"][i] * tck)
    else:
      results.append("")
  out_f.write(",".join([str(res) for res in results]) + "\n")
