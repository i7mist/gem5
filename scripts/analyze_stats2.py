import sys
import stats_analyzer as sa

base_dir = "/safari/hyena/tianshi"
standards = ["DDR3", "DDR4", "LPDDR3", "LPDDR4", "GDDR5", "WideIO", "WideIO2", "HBM"]
tCK = [(3/0.4)/8, (3/0.4)/9, (3/0.4)/8, 2.5/4, 8.0/14, 5.0*3/4, 2.5*3/4, 2.0]
nRCDR = [13, 18, 20, 29, 21, 5, 10, 7]
nRCDW = [13, 18, 20, 29, 18, 5, 10, 6]
nRP = [13, 18, 20, 27, 21, 5, 10, 7] # or nRPpb for PRE latency
nCL = [13, 18, 16, 32, 21, 3, 9, 7]
nBL = [4, 4, 4, 8, 2, 4, 2, 2]
nDQSCK = [0, 0, 3, 3, 0, 1, 1, 0]
workload = sys.argv[1]
out_f = open(sys.argv[2], "w")
num_of_standards = len(standards)

care_of_stats = [
# high level metrics
                 "sim_insts", "ipc", "energy", "",
# memory intensity
                 "MPKI", "",
# memory bandwidth
                 "memory_bandwidth", "write_bandwidth", "read_bandwidth", "maximum_bandwidth", "bandwidth_utilization", "",
# memory timing parameters
                 "frequency", "tCK(ns)", "tRP(ns)", "tRCDR(ns)", "tRCDW(ns)", "tCL(ns)", "tBL(ns)", "nBL", "", 
# memory latency
                 "average_read_memory_latency(ns)", "average_read_act_cmd", "average_read_act_time(ns)", "average_read_non_auto_pre_cmd", "average_read_non_auto_pre_time(ns)", "average_read_wait_to_issue_time(ns)", "read_latency(ns)", "average_read_wait_after_issue_time(ns)", "",
# memory access pattern
                 "row_hit_rate", "read_row_hit_rate", "write_row_hit_rate", "row_miss_rate", "read_row_miss_rate", "write_row_miss_rate", "row_conflict_rate", "read_row_conflict_rate", "write_row_conflict_rate", "",
# MLP is defined as the average number of outstanding memory requests when there is at least one outstanding request to memory.
# BLP is quantified by the actually serviced in parallel in different DRAM banks.
                 "MLP", "BLP"]

out_f.write("," + ",".join(care_of_stats) + "\n")

value = []

for i in range(0, num_of_standards):
  dram = standards[i]
  s = sa.Stats(base_dir + "/" + workload + "/" + dram + "/" + "stats.txt")
  v = []

# if we haven't got the stats for this DRAM, just let it go...
  if len(s.sys_stats) == 0 or len(s.mem_stats) == 0:
    continue

#   print s.mem_stats

  total_reqs = s.mem_stats["total_incoming_reqs"]
  read_reqs = s.mem_stats["read_reqs"]
  write_reqs = s.mem_stats["write_reqs"]

  tck = s.mem_stats["tCK(ns)"]
  s.mem_stats["tRCDR(ns)"] = tRCDR = tck * s.mem_stats["nRCDR"]
  s.mem_stats["tRCDW(ns)"] = tRCDW = tck * s.mem_stats["nRCDW"]
  s.mem_stats["tRP(ns)"] = tRP = tck * s.mem_stats["nRP"]
  s.mem_stats["tCL(ns)"] = tCL = tck * s.mem_stats["nCL"]
  s.mem_stats["tBL(ns)"] = tBL = tck * s.mem_stats["nBL"]
#   read_latency = s.mem_stats["read_latency(ns)"]
  read_latency = (nCL[i] + nBL[i] + nDQSCK[i]) * tck

  total_active_cycs = s.mem_stats["active_cycles"]
  total_queue_cycs = s.mem_stats["queue_cycles"]
  total_cycs = s.mem_stats["dram_cycles"]

  for careofs in care_of_stats:
    if s.sys_stats.has_key(careofs):
      v.append(s.sys_stats[careofs])

    elif s.mem_stats.has_key(careofs):
      v.append(s.mem_stats[careofs])

    elif careofs == "MPKI": # 
      v.append(s.mem_stats["read_reqs"] / s.sys_stats["sim_insts"] * 1000)
    
    elif careofs == "bandwidth_utilization":
      v.append(s.sys_stats["memory_bandwidth"] / s.mem_stats["maximum_bandwidth"])

    elif careofs == "average_read_memory_latency(ns)":
      mem_read_latency_sum = sum([l[1] for l in s.mem_stats["latency_sum"][0]])
      v.append(mem_read_latency_sum * tck / read_reqs)
      s.mem_stats["average_read_memory_latency(ns)"] = mem_read_latency_sum * tck / read_reqs

    elif careofs == "average_read_act_cmd":
      read_act_cmd_sum = sum([l[1] for l in s.mem_stats["read_act_cmd_count"][0]])
      read_act_time = read_act_cmd_sum * tRCDR
      v.append(read_act_cmd_sum / read_reqs)

      s.mem_stats["average_read_act_time(ns)"] = read_act_time / read_reqs

    elif careofs == "average_read_non_auto_pre_cmd":
      read_non_auto_pre_cmd_sum = sum([l[1] for l in s.mem_stats["read_pre_cmd_count"][0]])
      read_non_auto_pre_cmd_time = read_non_auto_pre_cmd_sum * tRP
      v.append(read_non_auto_pre_cmd_sum / read_reqs)

      s.mem_stats["average_read_non_auto_pre_time(ns)"] = read_non_auto_pre_cmd_time / read_reqs


    elif careofs == "average_read_wait_to_issue_time(ns)":
      read_wait_to_issue_cycs_sum = sum([l[1] for l in s.mem_stats["read_wait_issue_cycs_sum"][0]])
      s.mem_stats["average_read_wait_to_issue_time(ns)"] = read_wait_to_issue_cycs_sum * tck / read_reqs
      v.append(s.mem_stats["average_read_wait_to_issue_time(ns)"])

    elif careofs == "average_read_wait_after_issue_time(ns)":
      read_wait_after_issue_time = s.mem_stats["average_read_memory_latency(ns)"] \
         - s.mem_stats["average_read_act_time(ns)"] \
         - s.mem_stats["average_read_non_auto_pre_time(ns)"] \
         - s.mem_stats["average_read_wait_to_issue_time(ns)"] \
         - read_latency

      print read_wait_after_issue_time / read_reqs
      s.mem_stats["average_read_wait_after_issue_time(ns)"] = read_wait_after_issue_time / read_reqs
      v.append(s.mem_stats["average_read_wait_after_issue_time(ns)"])

    elif careofs == "row_hit_rate":
      row_hit_sum = sum([l[1] for l in s.mem_stats["read_rowhit"][0]]) + sum([l[1] for l in s.mem_stats["write_rowhit"][0]])
      v.append(row_hit_sum / total_reqs)

    elif careofs == "read_row_hit_rate":
      read_row_hit_sum = sum([l[1] for l in s.mem_stats["read_rowhit"][0]])
      if read_reqs > 0:
        v.append(read_row_hit_sum / read_reqs)
      else:
        v.append("read_reqs == 0")

    elif careofs == "write_row_hit_rate":
      write_row_hit_sum = sum([l[1] for l in s.mem_stats["write_rowhit"][0]])
      if write_reqs > 0:
        v.append(write_row_hit_sum / write_reqs)
      else:
        v.append("write_reqs == 0")

    elif careofs == "row_miss_rate":
      row_miss_sum = sum([l[1] for l in s.mem_stats["read_rowmiss"][0]]) + sum([l[1] for l in s.mem_stats["write_rowmiss"][0]])
      v.append(row_miss_sum / total_reqs)

    elif careofs == "read_row_miss_rate":
      read_row_miss_sum = sum([l[1] for l in s.mem_stats["read_rowmiss"][0]])
      if read_reqs > 0:
        v.append(read_row_miss_sum / read_reqs)
      else:
        v.append("read_reqs == 0")

    elif careofs == "write_row_miss_rate":
      write_row_miss_sum = sum([l[1] for l in s.mem_stats["write_rowmiss"][0]])
      if write_reqs > 0:
        v.append(write_row_miss_sum / write_reqs)
      else:
        v.append(0)

    elif careofs == "row_conflict_rate":
      row_conflict_sum = sum([l[1] for l in s.mem_stats["read_rowconflict"][0]]) + sum([l[1] for l in s.mem_stats["write_rowconflict"][0]])
      v.append(row_conflict_sum / total_reqs)

    elif careofs == "read_row_conflict_rate":
      read_row_conflict_sum = sum([l[1] for l in s.mem_stats["read_rowconflict"][0]])
      v.append(read_row_conflict_sum / read_reqs)

    elif careofs == "write_row_conflict_rate":
      write_row_conflict_sum = sum([l[1] for l in s.mem_stats["write_rowconflict"][0]])
      if write_reqs > 0:
        v.append(write_row_conflict_sum / write_reqs)
      else:
        v.append(0)

    elif careofs == "MLP":
      req_queue_length_sum = sum([l[1] for l in s.mem_stats["req_queue_length_sum"][0]])
      v.append(req_queue_length_sum / total_queue_cycs)

    elif careofs == "BLP":
      r = s.mem_stats["total_serving_reqs"]
      channel = 0
      total_serving_reqs = sum([l[1] for l in r[channel]])
      v.append(total_serving_reqs / total_active_cycs)

    else:
      v.append("")
  output_string = ",".join([str(res) for res in v])
  out_f.write(dram + "," + output_string + "\n")
