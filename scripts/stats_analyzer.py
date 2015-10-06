import sys
import os.path

### This python script is used for extract structural data from gem5 stats.txt

### Here I list all the statistics I concerns, to be developed ...
# memory_bandwidth
# IPC
# CPI
# cache miss rate
# incoming requests
# row buffer hit/miss
# memory latency sum (average memory latency)
# ACT count
# non auto PRE count
# time wait to issue
# memory controller queue length
# refresh cycle
# active cycle
# busy cycle
# simultaneouly serving requests

stat_map = dict()
multilevel_stats = []

### We ignore most gem5 statistics, except for:
# sim_insts
# system.cpu.dcache.overall_accesses::switch_cpus.data
# system.mem_ctrls.bw_total::total
# system.mem_ctrls.bw_write::total
# system.mem_ctrls.bw_read::total
# system.switch_cpus.cpi
# system.switch_cpus.cpi_total
# system.cpu.dcache.overall_miss_rate::total
# system.cpu.l2cache.overall_miss_rate::total
# system.l3.overall_miss_rate::total
# 
stat_map["sim_insts"] = "sim_insts"
stat_map["system.cpu.dcache.overall_accesses::total"] = "l1_access"
stat_map["system.mem_ctrls.bw_total::total"] = "memory_bandwidth"
stat_map["system.mem_ctrls.bw_write::total"] = "write_bandwidth"
stat_map["system.mem_ctrls.bw_read::total"] = "read_bandwidth"
stat_map["system.switch_cpus.ipc"] = "ipc"
stat_map["system.switch_cpus.cpi"] = "cpi"
stat_map["system.switch_cpus.ipc_total"] = "ipc_total" 
stat_map["system.switch_cpus.cpi_total"] = "cpi_total"
stat_map["system.cpu.ipc"] = "ipc"
stat_map["system.cpu.cpi"] = "cpi"
stat_map["system.cpu.cpi_total"] = "cpi_total"
stat_map["system.cpu.dcache.overall_miss_rate::total"] = "dcache_miss_rate"
stat_map["system.cpu.l2cache.overall_miss_rate::total"] = "l2cache_miss_rate"
stat_map["system.l3.overall_miss_rate::total"] = "l3cache_miss_rate"
stat_map["system.cpu.dcache.ReadReq_miss_rate::total"] = "dcache_read_miss_rate"
stat_map["system.cpu.l2cache.ReadReq_miss_rate::total"] = "l2cache_read_miss_rate"
stat_map["system.l3.ReadReq_miss_rate::total"] = "l3cache_read_miss_rate"
stat_map["system.cpu.dcache.WriteReq_miss_rate::total"] = "dcache_write_miss_rate"
stat_map["system.cpu.l2cache.WriteReq_miss_rate::total"] = "l2cache_write_miss_rate"
stat_map["system.l3.WriteReq_miss_rate::total"] = "l3cache_write_miss_rate"

### We extract the following ramulator statistics
# ramulator.incoming_requests
# ramulator.read_requests
# ramulator.write_requests
# ramulator.dram_cycles
# ramulator.memory_access_cycles
# ramulator.ramulator_active_cycles
# ramulator.ramulator_refresh_cycles
# ramulator.ramulator_busy_cycles

# ramulator.incoming_requests_per_channel::[0, 1, 2, 3,...]
# ramulator.read_row_hit_channel_[0, 1, 2, 3,...]
# ramulator.read_row_miss_channel_[0, 1, 2, 3,...]
# ramulator.write_row_hit_channel_[0, 1, 2, 3,...]
# ramulator.write_row_miss_channel_[0, 1, 2, 3,...]
# ramulator.read_latency_sum_[0, 1, 2, 3,...]
# ramulator.req_queue_length_sum_[0, 1, 2, 3,...]
# ramulator.act_cmd_count_[0, 1, 2, 3,...]
# ramulator.non_auto_precharge_count[0, 1, 2, 3,...]
# ramulator.wait_issue_time_sum[0, 1, 2, 3,...]
# ramulator.read_wait_issue_time_sum[0, 1, 2, 3,...]
# ramulator.write_wait_issue_time_sum[0, 1, 2, 3,...]

# ramulator.total_serving_requests_3_0_7
# ramulator.total_refresh_cycles_3_0_7
# ramulator.total_busy_cycles_3_0_7

stat_map["ramulator.incoming_requests"] = "total_incoming_reqs"
stat_map["ramulator.read_requests"] = "read_reqs"
stat_map["ramulator.write_requests"] = "write_reqs"
stat_map["ramulator.dram_cycles"] = "dram_cycles"
stat_map["ramulator.memory_access_cycles"] = "queue_cycles"
stat_map["ramulator.ramulator_active_cycles"] = "active_cycles"
stat_map["ramulator.ramulator_refresh_cycles"] = "refresh_cycles"
stat_map["ramulator.ramulator_busy_cycles"] = "busy_cycles"
stat_map["ramulator.maximum_bandwidth"] = "maximum_bandwidth"
stat_map["ramulator.tCK"] = "tCK(ns)"
stat_map["ramulator.nRCDR"] = "nRCDR"
stat_map["ramulator.nRCDW"] = "nRCDW"
stat_map["ramulator.nRP"] = "nRP"
stat_map["ramulator.nBL"] = "nBL"
stat_map["ramulator.nCL"] = "nCL"
stat_map["ramulator.read_latency"] = "read_latency(ns)"
stat_map["ramulator.frequency"] = "frequency"

stat_map["ramulator.incoming_requests_per_channel::"] = "incoming_reqs"
stat_map["ramulator.read_row_hit_channel_"] = "read_rowhit"
stat_map["ramulator.read_row_miss_channel_"] = "read_rowmiss"
stat_map["ramulator.read_row_conflict_channel_"] = "read_rowconflict"
stat_map["ramulator.write_row_hit_channel_"] = "write_rowhit"
stat_map["ramulator.write_row_miss_channel_"] = "write_rowmiss"
stat_map["ramulator.write_row_conflict_channel_"] = "write_rowconflict"
stat_map["ramulator.read_latency_sum_"] = "latency_sum"
stat_map["ramulator.req_queue_length_sum_"] = "req_queue_length_sum"
stat_map["ramulator.read_req_queue_length_sum_"] = "read_req_queue_length_sum"
stat_map["ramulator.write_req_queue_length_sum_"] = "write_req_queue_length_sum"
stat_map["ramulator.act_cmd_count_"] = "act_cmd_count"
stat_map["ramulator.read_act_cmd_count_"] = "read_act_cmd_count"
stat_map["ramulator.non_auto_precharge_count"] = "pre_cmd_count"
stat_map["ramulator.read_non_auto_precharge_count"] = "read_pre_cmd_count"
stat_map["ramulator.wait_issue_time_sum"] = "wait_issue_cycs_sum"
stat_map["ramulator.read_wait_issue_time_sum"] = "read_wait_issue_cycs_sum"
stat_map["ramulator.write_wait_issue_time_sum"] = "write_wait_issue_cycs_sum"
stat_map["ramulator.total_serving_requests_"] = "total_serving_reqs"
stat_map["ramulator.total_active_cycles_"] = "total_active_cycs"
stat_map["ramulator.total_refresh_cycles_"] = "total_refresh_cycs"
stat_map["ramulator.total_busy_cycles_"] = "total_busy_cycs"
stat_map["ramulator.total_active_and_refresh_cycles_"] = "total_active_and_refresh_cycs"

multilevel_stats.append("ramulator.incoming_requests_per_channel::")
multilevel_stats.append("ramulator.read_row_hit_channel_")
multilevel_stats.append("ramulator.read_row_miss_channel_")
multilevel_stats.append("ramulator.read_row_conflict_channel_")
multilevel_stats.append("ramulator.write_row_hit_channel_")
multilevel_stats.append("ramulator.write_row_miss_channel_")
multilevel_stats.append("ramulator.write_row_conflict_channel_")
multilevel_stats.append("ramulator.read_latency_sum_")
multilevel_stats.append("ramulator.req_queue_length_sum_")
multilevel_stats.append("ramulator.read_req_queue_length_sum_")
multilevel_stats.append("ramulator.write_req_queue_length_sum_")
multilevel_stats.append("ramulator.act_cmd_count_")
multilevel_stats.append("ramulator.read_act_cmd_count_")
multilevel_stats.append("ramulator.non_auto_precharge_count")
multilevel_stats.append("ramulator.read_non_auto_precharge_count")
multilevel_stats.append("ramulator.wait_issue_time_sum")
multilevel_stats.append("ramulator.read_wait_issue_time_sum")
multilevel_stats.append("ramulator.write_wait_issue_time_sum")

multilevel_stats.append("ramulator.total_serving_requests_")
multilevel_stats.append("ramulator.total_active_cycles_")
multilevel_stats.append("ramulator.total_refresh_cycles_")
multilevel_stats.append("ramulator.total_busy_cycles_")
multilevel_stats.append("ramulator.total_active_and_refresh_cycles_")

# Wow, I think that would be all we have for now!

class Stats(object):

  def is_multilevel_stats(self, full_name):
    for partial_name in multilevel_stats:
      if partial_name in full_name:
        return partial_name
    return ""

  def __init__(self, fname):
    self.stats = dict()
    self.mem_stats = dict()
    self.sys_stats = dict()
    if os.path.isfile(fname):
      f = open(fname, "r")
    else:
      return
    for s in f:
      s = s.split(" ")
      s = filter(None, s)[:2]
      # not statistics
      if len(s) < 2 or "-" in s[0]:
        continue
      if s[0] == "#":
        continue
      value = float(s[1])
      if stat_map.has_key(s[0]):
        stat_name = stat_map[s[0]]
        if s[0].split(".")[0] == "ramulator":
          self.mem_stats[stat_name] = value
        else:
          self.sys_stats[stat_name] = value
      else:
        partial_name = self.is_multilevel_stats(s[0])
        if not partial_name:
          continue
        indices = s[0][len(partial_name):].split("_")
#         print indices
        stat_name = stat_map[partial_name]
        value = float(s[1])
        if s[0].split(".")[0] == "ramulator":
          if self.mem_stats.has_key(stat_name) and self.mem_stats[stat_name].has_key(len(indices) - 1):
            self.mem_stats[stat_name][len(indices) - 1].append((indices, value))
          elif not self.mem_stats.has_key(stat_name):
            self.mem_stats[stat_name] = {len(indices) - 1 : [(indices, value)]}
          else:
            self.mem_stats[stat_name][len(indices) - 1] = [(indices, value)]
        else:
          assert(False and "Wow only ramulator has multilevel stats!")
