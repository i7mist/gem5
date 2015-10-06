import sys
import stats_analyzer as sa

base_dir = "/safari/hyena/tianshi/gem5-stable/characterize"
standards = ["DDR3", "DDR4", "LPDDR3", "LPDDR4", "GDDR5", "WideIO", "WideIO2", "HBM"]
tCK = [(3/0.4)/8, (3/0.4)/9, (3/0.4)/8, 2.5/4, 8.0/14, 5.0*3/4, 2.5*3/4, 2.0]
nRCDR = [13, 18, 20, 29, 21, 5, 10, 7]
nRCDW = [13, 18, 20, 29, 18, 5, 10, 6]
nRP = [13, 18, 20, 27, 21, 5, 10, 7] # or nRPpb
nCL = [13, 18, 16, 32, 21, 3, 9, 7]
nBL = [4, 4, 4, 8, 2, 4, 2, 2]
nDQSCK = [0, 0, 3, 3, 0, 1, 1, 0]
workload = sys.argv[1]
out_f = open(sys.argv[2], "w")
num_of_standards = len(standards)

care_of_stats = ["sim_insts", "l1_access", "l1_read_access", "memory_bandwidth", "write_bandwidth", "read_bandwidth", "cpi", "dcache_miss_rate", "l2cache_miss_rate", "l3cache_miss_rate", "average_memory_latency(ns)", "average_act_cmd", "average_act_time(ns)", "average_read_act_time(ns)", "average_non_auto_pre_cmd", "average_non_auto_pre_cmd(ns)", "average_wait_to_issue_time(ns)", "average_rd_time(ns)","other_time(ns)", "row_hit_rate", "read_row_hit_rate", "write_row_hit_rate", "average_queue_length_per_cycle", "average_requests_per_bank_per_cycle", "bank_num", "average_requests_per_rank_per_cycle", "rank_num", "average_requests_per_channel_per_cycle", "channel_num", "busy_time_per_rank(ns)", "active_time_per_rank(ns)", "refresh_time_per_rank(ns)", "active_and_refresh_time_per_rank(ns)", "refresh_time_per_req(ns)", "channel_active_rates"]

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

  tck = tCK[i]
  tRCDR = tck * nRCDR[i]
  tRCDW = tck * nRCDW[i]
  tRP = tck * nRP[i]
  read_latency = tck * (nCL[i] + nBL[i] + nDQSCK[i])

  total_active_cycs = s.mem_stats["active_cycles"]
  total_cycs = s.mem_stats["dram_cycles"]

  for careofs in care_of_stats:
    if s.sys_stats.has_key(careofs):
      v.append(s.sys_stats[careofs])

    elif s.mem_stats.has_key(careofs):
      v.append(s.mem_stats[careofs])

    elif careofs == "average_memory_latency(ns)":
      mem_latency_sum = sum([l[1] for l in s.mem_stats["latency_sum"][0]])
      if read_reqs > 0:
        v.append(mem_latency_sum * tck / read_reqs)
        s.mem_stats["average_memory_latency(ns)"] = mem_latency_sum * tck / read_reqs
      else:
        v.append(0)

    elif careofs == "average_act_cmd":
      act_cmd_sum = sum([l[1] for l in s.mem_stats["act_cmd_count"][0]])
      s.mem_stats["act_cmd_sum"] = act_cmd_sum
      v.append(act_cmd_sum / total_reqs)

    elif careofs == "average_act_time(ns)":
      if s.mem_stats.has_key("read_act_cmd_count"):
        act_cmd_sum = s.mem_stats["act_cmd_sum"]
        read_act_cmd_sum = sum([l[1] for l in s.mem_stats["read_act_cmd_count"][0]])
        s.mem_stats["average_read_act_time(ns)"] = read_act_cmd_sum * tRCDR / read_reqs
        write_act_cmd_sum = act_cmd_sum - read_act_cmd_sum
        act_cmd_time = read_act_cmd_sum * tRCDR + write_act_cmd_sum * tRCDW
        v.append(act_cmd_time / total_reqs)
      else:
        read_row_miss_sum = sum([l[1] for l in s.mem_stats["read_rowmiss"][0]])
        write_row_miss_sum = sum(l[1] for l in s.mem_stats["write_rowmiss"][0])
        row_miss_sum = read_row_miss_sum + write_row_miss_sum
        act_cmd_sum = s.mem_stats["act_cmd_sum"]
        read_act_cmd_time = read_row_miss_sum/row_miss_sum * act_cmd_sum * tRCDR
        write_act_cmd_time = write_row_miss_sum/row_miss_sum * act_cmd_sum * tRCDW
        estimate_avg_act_cmd_time = (read_act_cmd_time + write_act_cmd_time) / total_reqs
        v.append(estimate_avg_act_cmd_time)
        estimate_avg_read_act_cmd_time = read_act_cmd_time / read_reqs
        s.mem_stats["average_read_act_time(ns)"] = estimate_avg_read_act_cmd_time

    elif careofs == "average_non_auto_pre_cmd":
      non_auto_pre_cmd_sum = sum([l[1] for l in s.mem_stats["pre_cmd_count"][0]])
      v.append(non_auto_pre_cmd_sum / total_reqs)

    elif careofs == "average_non_auto_pre_cmd(ns)":
      non_auto_pre_cmd_sum = sum([l[1] for l in s.mem_stats["pre_cmd_count"][0]])
      v.append(non_auto_pre_cmd_sum * tRP / total_reqs)
      s.mem_stats["average_non_auto_pre_cmd(ns)"] = non_auto_pre_cmd_sum * tRP / total_reqs

    elif careofs == "average_wait_to_issue_time(ns)":
      wait_to_issue_sum = sum([l[1] for l in s.mem_stats["wait_issue_time_sum"][0]])
      v.append(wait_to_issue_sum * tck/ total_reqs)
      s.mem_stats["average_wait_to_issue_time(ns)"] = wait_to_issue_sum * tck / total_reqs

    elif careofs == "average_rd_time(ns)":
      v.append(read_latency)

    elif careofs == "other_time(ns)":
      other_time = s.mem_stats["average_memory_latency(ns)"]
      other_time -= s.mem_stats["average_read_act_time(ns)"]
      other_time -= s.mem_stats["average_non_auto_pre_cmd(ns)"]
      other_time -= s.mem_stats["average_wait_to_issue_time(ns)"]
      other_time -= read_latency
      v.append(other_time)

    elif careofs == "row_hit_rate":
      row_hit_sum = sum([l[1] for l in s.mem_stats["read_rowhit"][0]]) + sum([l[1] for l in s.mem_stats["write_rowhit"][0]])
      v.append(row_hit_sum / total_reqs)

    elif careofs == "read_row_hit_rate":
      read_row_hit_sum = sum([l[1] for l in s.mem_stats["read_rowhit"][0]])
      v.append(read_row_hit_sum / read_reqs)

    elif careofs == "write_row_hit_rate":
      write_row_hit_sum = sum([l[1] for l in s.mem_stats["write_rowhit"][0]])
      if write_reqs > 0:
        v.append(write_row_hit_sum / write_reqs)
      else:
        v.append(0)

    elif careofs == "average_queue_length_per_cycle":
      req_queue_length_sum = sum([l[1] for l in s.mem_stats["req_queue_length_sum"][0]])
      v.append(req_queue_length_sum / total_cycs)

    elif careofs == "average_requests_per_bank_per_cycle":
      r = s.mem_stats["total_serving_reqs"]
      c = s.mem_stats["total_active_cycs"]
      bank = len(r) - 1
      bank_num = len(r[bank])
      s.mem_stats["bank_num"] = bank_num
      avg_reqs_per_cyc_sum = 0
      for i in range(0, bank_num):
        avg_reqs_per_cyc_sum += r[bank][i][1] / c[bank][i][1]
      avg_reqs = avg_reqs_per_cyc_sum / bank_num
      v.append(avg_reqs)

    elif careofs == "average_requests_per_rank_per_cycle":
      r = s.mem_stats["total_serving_reqs"]
      c = s.mem_stats["total_active_cycs"]
      rank = 1
      rank_num = len(r[rank])
      s.mem_stats["rank_num"] = rank_num
      avg_reqs_per_cyc_sum = 0
      for i in range(0, rank_num):
        avg_reqs_per_cyc_sum += r[rank][i][1] / c[rank][i][1]
      avg_reqs = avg_reqs_per_cyc_sum / rank_num
      v.append(avg_reqs)

    elif careofs == "average_requests_per_channel_per_cycle":
      r = s.mem_stats["total_serving_reqs"]
      c = s.mem_stats["total_active_cycs"]
      channel = 0
      channel_num = len(r[channel])
      s.mem_stats["channel_num"] = channel_num
      avg_reqs_per_cyc_sum = 0
      for i in range(0, channel_num):
        avg_reqs_per_cyc_sum += r[channel][i][1] / c[channel][i][1]
      avg_reqs = avg_reqs_per_cyc_sum / channel_num
      v.append(avg_reqs)

    elif careofs == "busy_time_per_rank(ns)":
      if s.mem_stats.has_key("total_busy_cycs"):
        c = s.mem_stats["total_busy_cycs"]
        rank = 1
        rank_num = len(c[rank])
        busy_time_sum = sum([l[1] for l in c[rank]]) *tck
        busy_time_avg = busy_time_sum / rank_num
        v.append(busy_time_avg)
      else:
        v.append("")

    elif careofs == "active_time_per_rank(ns)":
      c = s.mem_stats["total_active_cycs"]
      rank = 1
      rank_num = len(c[rank])
      active_time_sum = sum([l[1] for l in c[rank]]) * tck
      active_time_avg = active_time_sum / rank_num
      v.append(active_time_avg)

    elif careofs == "refresh_time_per_rank(ns)":
      c = s.mem_stats["total_refresh_cycs"]
      rank = 1
      rank_num = len(c[rank])
      refresh_time_sum = sum([l[1] for l in c[rank]]) * tck
      refresh_time_avg = refresh_time_sum / rank_num
      v.append(refresh_time_avg)

    elif careofs == "active_and_refresh_time_per_rank(ns)":
      if s.mem_stats.has_key("total_active_and_refresh_cycs"):
        c = s.mem_stats["total_active_and_refresh_cycs"]
        rank = 1
        rank_num = len(c[rank])
        active_and_refresh_time_sum = sum(l[1] for l in c[rank]) * tck
        active_and_refresh_time_avg = active_and_refresh_time_sum / rank_num
        v.append(active_and_refresh_time_avg)
      else:
        ac = s.mem_stats["total_active_cycs"] 
        rc = s.mem_stats["total_refresh_cycs"]
        bc = s.mem_stats["total_busy_cycs"]
        rank = 1
        rank_num = len(c[rank])
        active_time_sum = sum([l[1] for l in ac[rank]]) * tck
        refresh_time_sum = sum([l[1] for l in rc[rank]]) * tck
        busy_time_sum = sum([l[1] for l in bc[rank]]) * tck
        active_and_refresh_time_sum = active_time_sum + refresh_time_sum - busy_time_sum
        active_and_refresh_time_avg = active_and_refresh_time_sum / rank_num
        v.append(active_and_refresh_time_avg)

    elif careofs == "refresh_time_per_req(ns)":
      c = s.mem_stats["total_refresh_cycs"]
      rank = 1
      refresh_time_sum = sum([l[1] for l in c[rank]]) * tck
      v.append(refresh_time_sum / total_reqs)

    elif careofs == "channel_active_rates":
      c = s.mem_stats["total_active_cycs"]
      channel = 0
      channel_num = len(c[channel])
      rates = [l[1] / total_active_cycs for l in c[channel]]
      v.append(",".join([str(rate) for rate in rates]))
    else:
      v.append("")
  output_string = ",".join([str(res) for res in v])
  out_f.write(dram + "," + output_string + "\n")
