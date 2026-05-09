# SysLab Task Quality Report

Generated: 2026-03-04

## Summary

| Course | Task | Critical |
|--------|------|----------|
| mit_6_1810_2022 | task_1_util | 0 |
| mit_6_1810_2022 | task_2_syscall | 0 |
| mit_6_1810_2022 | task_3_pgtbl | 0 |
| mit_6_1810_2022 | task_4_traps | 0 |
| mit_6_1810_2022 | task_5_cow | 0 |
| mit_6_1810_2022 | task_6_thread | 0 |
| mit_6_1810_2022 | task_7_net | 0 |
| mit_6_1810_2022 | task_8_lock | 0 |
| mit_6_1810_2022 | task_9_fs | 0 |
| mit_6_1810_2022 | task_10_mmap | 0 |
| mit_6_5840_2024 | task_1_mapreduce | 0 |
| mit_6_5840_2024 | task_2_kvsrv | 0 |
| mit_6_5840_2024 | task_2b_kvsrv | 0 |
| mit_6_5840_2024 | task_3a_raft | 0 |
| mit_6_5840_2024 | task_3b_raft | 0 |
| mit_6_5840_2024 | task_3c_raft | 0 |
| mit_6_5840_2024 | task_3d_raft | 0 |
| mit_6_5840_2024 | task_4a_kvraft | 0 |
| mit_6_5840_2024 | task_4b_kvraft | 0 |
| mit_6_5840_2024 | task_5a_shardkv | 0 |
| mit_6_5840_2024 | task_5b_shardkv | 0 |
| mit_6_824_2012 | task_1_lock_server | 0 |
| mit_6_824_2012 | task_2_basic_file_server | 0 |
| mit_6_824_2012 | task_3_mkdir_unlink_locking | 0 |
| mit_6_824_2012 | task_4_caching_locks | 0 |
| mit_6_824_2012 | task_5_caching_extents | 0 |
| mit_6_824_2012 | task_6_paxos | 0 |
| mit_6_824_2012 | task_7_rsm | 0 |
| pku_pintos_2025 | task_1_threads | 0 |
| pku_pintos_2025 | task_2_userprog | 0 |
| pku_pintos_2025 | task_3a_vm | 0 |
| pku_pintos_2025 | task_3b_mmap | 0 |
| sfu_cmpt_201_2025 | task_2_bash_scripting | 0 |
| sfu_cmpt_201_2025 | task_3_c_compilation | 0 |
| sfu_cmpt_201_2025 | task_4_make_cmake | 0 |
| sfu_cmpt_201_2025 | task_5_debugging_tools | 0 |
| sfu_cmpt_201_2025 | task_6_memory_stack | 0 |
| sfu_cmpt_201_2025 | task_7_memory_mapping | 0 |
| sfu_cmpt_201_2025 | task_8_simple_shell | 0 |
| sfu_cmpt_201_2025 | task_9_memory_allocator | 0 |
| sfu_cmpt_201_2025 | task_10_mapreduce | 0 |
| sfu_cmpt_201_2025 | task_11_chat_server | 0 |
| sfu_cmpt_201_2025 | task_12_blockchain | 0 |
| uchicago_chidb_2015 | task_1_btree | 0 |
| uchicago_chidb_2015 | task_2_dbm | 0 |
| uchicago_chidb_2015 | task_3_codegen | 0 |
| uw_madison_cs537_2018 | task_2a_processes_shell | 0 |
| uw_madison_cs537_2018 | task_4a_concurrency_mapreduce | 0 |
| uw_madison_cs537_2018 | task_5_filesystems_checker | 0 |

**Total**: 0 critical findings across 49 tasks.

## Findings by Task

No critical findings were identified. All 49 tasks passed the audit checks:

- **Protected Files**: Every task that lists `protected_files` in `config.json` also documents them in `task.md` (typically in an "Environment Notes" section).
- **Working Directory**: All tasks clearly state or make inferable the working directory via an explicit path in `task.md`.
- **Build/Eval Alignment**: No undocumented build flags or environment requirements that would cause silent evaluation failures were found.
