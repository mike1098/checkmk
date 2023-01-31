#!/usr/bin/env python3
# Copyright (C) 2020 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import json
from collections import defaultdict
from unittest.mock import call, MagicMock

import pytest
from pytest_mock import MockerFixture

from tests.unit.cmk.gui.conftest import WebTestAppForCMK

from cmk.automations.results import (
    CheckPreviewEntry,
    GetServicesLabelsResult,
    ServiceDiscoveryPreviewResult,
    SetAutochecksResult,
)

mock_discovery_result = ServiceDiscoveryPreviewResult(
    check_table=[
        CheckPreviewEntry(
            "old",
            "cpu.loads",
            "cpu_load",
            None,
            "cpuload_default_levels",
            (5.0, 10.0),
            "CPU load",
            0,
            "15 min load: 1.32 at 8 Cores (0.17 per Core)",
            [
                ("load1", 2.7, 40.0, 80.0, 0, 8),
                ("load5", 1.63, 40.0, 80.0, 0, 8),
                ("load15", 1.32, 40.0, 80.0, 0, 8),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "cpu.threads",
            "threads",
            None,
            "{}",
            {"levels": (2000, 4000)},
            "Number of threads",
            0,
            "Count: 1708 threads, Usage: 1.35%",
            [
                ("threads", 1708, 2000.0, 4000.0, None, None),
                ("thread_usage", 1.3496215054443164, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "new",
            "df",
            "filesystem",
            "/opt/omd/sites/heute/tmp",
            {"include_volume_name": False},
            {
                "include_volume_name": False,
                "inodes_levels": (10.0, 5.0),
                "levels": (80.0, 90.0),
                "levels_low": (50.0, 60.0),
                "magic_normsize": 20,
                "show_inodes": "onlow",
                "show_levels": "onmagic",
                "show_reserved": False,
                "trend_perfdata": True,
                "trend_range": 24,
            },
            "Filesystem /opt/omd/sites/heute/tmp",
            0,
            "0.08% used (6.30 MB of 7.76 GB)",
            [
                ("fs_used", 6.30078125, 6356.853125, 7151.459765625, 0, 7946.06640625),
                ("fs_size", 7946.06640625, None, None, None, None),
                ("fs_used_percent", 0.07929434424363863, None, None, None, None),
                ("inodes_used", 1558, 1830773.7, 1932483.3499999999, 0.0, 2034193.0),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "new",
            "df",
            "filesystem",
            "/opt/omd/sites/old/tmp",
            {"include_volume_name": False},
            {
                "include_volume_name": False,
                "inodes_levels": (10.0, 5.0),
                "levels": (80.0, 90.0),
                "levels_low": (50.0, 60.0),
                "magic_normsize": 20,
                "show_inodes": "onlow",
                "show_levels": "onmagic",
                "show_reserved": False,
                "trend_perfdata": True,
                "trend_range": 24,
            },
            "Filesystem /opt/omd/sites/old/tmp",
            0,
            "0% used (0.00 B of 7.76 GB)",
            [
                ("fs_used", 0.0, 6356.853125, 7151.459765625, 0, 7946.06640625),
                ("fs_size", 7946.06640625, None, None, None, None),
                ("fs_used_percent", 0.0, None, None, None, None),
                ("inodes_used", 1, 1830773.7, 1932483.3499999999, 0.0, 2034193.0),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "new",
            "df",
            "filesystem",
            "/opt/omd/sites/stable/tmp",
            {"include_volume_name": False},
            {
                "include_volume_name": False,
                "inodes_levels": (10.0, 5.0),
                "levels": (80.0, 90.0),
                "levels_low": (50.0, 60.0),
                "magic_normsize": 20,
                "show_inodes": "onlow",
                "show_levels": "onmagic",
                "show_reserved": False,
                "trend_perfdata": True,
                "trend_range": 24,
            },
            "Filesystem /opt/omd/sites/stable/tmp",
            0,
            "0.12% used (9.43 MB of 7.76 GB)",
            [
                ("fs_used", 9.42578125, 6356.853125, 7151.459765625, 0, 7946.06640625),
                ("fs_size", 7946.06640625, None, None, None, None),
                ("fs_used_percent", 0.11862197933037819, None, None, None, None),
                ("inodes_used", 1412, 1830773.7, 1932483.3499999999, 0.0, 2034193.0),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "new",
            "df",
            "filesystem",
            "/",
            {"include_volume_name": False},
            {
                "include_volume_name": False,
                "inodes_levels": (10.0, 5.0),
                "levels": (80.0, 90.0),
                "levels_low": (50.0, 60.0),
                "magic_normsize": 20,
                "show_inodes": "onlow",
                "show_levels": "onmagic",
                "show_reserved": False,
                "trend_perfdata": True,
                "trend_range": 24,
            },
            "Filesystem /",
            0,
            "25.24% used (117.68 of 466.31 GB)",
            [
                ("fs_used", 120506.43359375, 382000.025, 429750.028125, 0, 477500.03125),
                ("fs_size", 477500.03125, None, None, None, None),
                ("fs_used_percent", 25.236947792084568, None, None, None, None),
                ("inodes_used", 1131429, 28009267.2, 29565337.599999998, 0.0, 31121408.0),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "df",
            "filesystem",
            "/boot/efi",
            "{'include_volume_name': False}",
            {
                "include_volume_name": False,
                "inodes_levels": (10.0, 5.0),
                "levels": (80.0, 90.0),
                "levels_low": (50.0, 60.0),
                "magic_normsize": 20,
                "show_inodes": "onlow",
                "show_levels": "onmagic",
                "show_reserved": False,
                "trend_perfdata": True,
                "trend_range": 24,
            },
            "Filesystem /boot/efi",
            0,
            "3.0% used (15.33 of 510.98 MB)",
            [
                ("fs_used", 15.328125, 408.7875, 459.8859375, 0, 510.984375),
                ("fs_size", 510.984375, None, None, None, None),
                ("fs_used_percent", 2.9997247958902853, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "new",
            "df",
            "filesystem",
            "/boot",
            {"include_volume_name": False},
            {
                "include_volume_name": False,
                "inodes_levels": (10.0, 5.0),
                "levels": (80.0, 90.0),
                "levels_low": (50.0, 60.0),
                "magic_normsize": 20,
                "show_inodes": "onlow",
                "show_levels": "onmagic",
                "show_reserved": False,
                "trend_perfdata": True,
                "trend_range": 24,
            },
            "Filesystem /boot",
            0,
            "30.85% used (217.37 of 704.48 MB)",
            [
                ("fs_used", 217.3671875, 563.5875, 634.0359375, 0, 704.484375),
                ("fs_size", 704.484375, None, None, None, None),
                ("fs_used_percent", 30.854791846873823, None, None, None, None),
                ("inodes_used", 305, 42163.200000000004, 44505.6, 0.0, 46848.0),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "kernel.performance",
            "kernel_performance",
            None,
            "{}",
            {},
            "Kernel Performance",
            0,
            "WAITING - Counter based check, cannot be done offline",
            [
                ("process_creations", 0.0, None, None, None, None),
                ("context_switches", 0.0, None, None, None, None),
                ("major_page_faults", 0.0, None, None, None, None),
                ("page_swap_in", 0.0, None, None, None, None),
                ("page_swap_out", 0.0, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "kernel.util",
            "cpu_iowait",
            None,
            "{}",
            {},
            "CPU utilization",
            0,
            "User: 14.7%, System: 12.14%, Wait: 0.1%, Total CPU: 26.95%",
            [
                ("user", 14.70410082412248, None, None, None, None),
                ("system", 12.142805812602681, None, None, None, None),
                ("wait", 0.10180487170606699, None, None, None, None),
                ("util", 26.948711508431227, None, None, 0, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 0",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 0",
            0,
            "25.0 °C",
            [("temp", 25.0, 107.0, 107.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 1",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 1",
            0,
            "20.0 °C",
            [("temp", 20.0, 70.0, 80.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 2",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 2",
            0,
            "54.0 °C",
            [("temp", 54.0, 78.0, 88.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 3",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 3",
            0,
            "35.0 °C",
            [("temp", 35.0, 70.0, 80.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 4",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 4",
            0,
            "41.0 °C",
            [("temp", 41.0, 70.0, 80.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 5",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 5",
            0,
            "55.5 °C",
            [("temp", 55.5, 115.0, 115.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 6",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 6",
            0,
            "64.0 °C",
            [("temp", 64.0, 99.0, 127.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 7",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 7",
            1,
            "74.0 °C (warn/crit at 70.0/80.0 °C)",
            [("temp", 74.0, 70.0, 80.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "lnx_thermal",
            "temperature",
            "Zone 8",
            "{}",
            {"device_levels_handling": "devdefault", "levels": (70.0, 80.0)},
            "Temperature Zone 8",
            0,
            "38.0 °C",
            [("temp", 38.0, 70.0, 80.0, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "new",
            "mem.linux",
            "memory_linux",
            None,
            {},
            {
                "levels_commitlimit": ("perc_free", (20.0, 10.0)),
                "levels_committed": ("perc_used", (100.0, 150.0)),
                "levels_hardwarecorrupted": ("abs_used", (1, 1)),
                "levels_pagetables": ("perc_used", (8.0, 16.0)),
                "levels_shm": ("perc_used", (20.0, 30.0)),
                "levels_total": ("perc_used", (120.0, 150.0)),
                "levels_virtual": ("perc_used", (80.0, 90.0)),
                "levels_vmalloc": ("abs_free", (52428800, 31457280)),
            },
            "Memory",
            2,
            "Total virtual memory: 49.43% - 8.14 GB of 16.48 GB, RAM: 47.68% - 7.40 GB of 15.52 GB, Swap: 77.91% - 763.52 MB of 980.00 MB, Largest Free VMalloc Chunk: 0% free - 0.00 B of 32.00 TB VMalloc Area (warn/crit below 50.00 MB/30.00 MB free)(!!)",
            [
                ("active", 8891592704, None, None, None, None),
                ("active_anon", 7336378368, None, None, None, None),
                ("active_file", 1555214336, None, None, None, None),
                ("anon_huge_pages", 0, None, None, None, None),
                ("anon_pages", 7420919808, None, None, None, None),
                ("bounce", 0, None, None, None, None),
                ("buffers", 272564224, None, None, None, None),
                ("cached", 3219124224, None, None, None, None),
                ("caches", 4009385984, None, None, None, None),
                ("cma_free", 0, None, None, None, None),
                ("cma_total", 0, None, None, None, None),
                ("commit_limit", 9359654912, None, None, None, None),
                ("committed_as", 16258154496, None, None, None, None),
                ("dirty", 14913536, None, None, None, None),
                ("hardware_corrupted", 0, None, None, None, None),
                ("inactive", 2157494272, None, None, None, None),
                ("inactive_anon", 1121906688, None, None, None, None),
                ("inactive_file", 1035587584, None, None, None, None),
                ("kreclaimable", 361406464, None, None, None, None),
                ("kernel_stack", 28037120, None, None, None, None),
                ("mapped", 970366976, None, None, None, None),
                ("mem_available", 7177719808, None, None, None, None),
                ("mem_free", 4710035456, None, None, None, None),
                ("mem_total", 16664109056, None, None, None, None),
                ("mem_used", 7944687616, None, None, None, None),
                ("mem_used_percent", 47.675441809110545, None, None, None, None),
                ("mlocked", 81920, None, None, None, None),
                ("nfs_unstable", 0, None, None, None, None),
                ("page_tables", 84729856, None, None, None, None),
                ("pending", 14913536, None, None, None, None),
                ("percpu", 9633792, None, None, None, None),
                ("sreclaimable", 361406464, None, None, None, None),
                ("sunreclaim", 257396736, None, None, None, None),
                ("shmem", 934322176, None, None, None, None),
                ("shmem_huge_pages", 0, None, None, None, None),
                ("shmem_pmd_mapped", 0, None, None, None, None),
                ("slab", 618803200, None, None, None, None),
                ("swap_cached", 156291072, None, None, None, None),
                ("swap_free", 226992128, None, None, None, None),
                ("swap_total", 1027600384, None, None, None, None),
                ("swap_used", 800608256, None, None, None, None),
                ("total_total", 17691709440, None, None, None, None),
                ("total_used", 8745295872, None, None, None, None),
                ("unevictable", 19808256, None, None, None, None),
                ("writeback", 0, None, None, None, None),
                ("writeback_tmp", 0, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "mkeventd_status",
            None,
            "heute",
            "{}",
            {},
            "OMD heute Event Console",
            0,
            "WAITING - Counter based check, cannot be done offline",
            [
                ("num_open_events", 0, None, None, None, None),
                ("process_virtual_size", 218300416, None, None, None, None),
                ("average_message_rate", 0.0, None, None, None, None),
                ("average_rule_hit_rate", 0.0, None, None, None, None),
                ("average_rule_trie_rate", 0.0, None, None, None, None),
                ("average_drop_rate", 0.0, None, None, None, None),
                ("average_event_rate", 0.0, None, None, None, None),
                ("average_connect_rate", 0.0, None, None, None, None),
                ("average_request_time", 0.00027762370400620984, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "mkeventd_status",
            None,
            "stable",
            "{}",
            {},
            "OMD stable Event Console",
            0,
            "WAITING - Counter based check, cannot be done offline",
            [
                ("num_open_events", 0, None, None, None, None),
                ("process_virtual_size", 205152256, None, None, None, None),
                ("average_message_rate", 0.0, None, None, None, None),
                ("average_rule_hit_rate", 0.0, None, None, None, None),
                ("average_rule_trie_rate", 0.0, None, None, None, None),
                ("average_drop_rate", 0.0, None, None, None, None),
                ("average_event_rate", 0.0, None, None, None, None),
                ("average_connect_rate", 0.0, None, None, None, None),
                ("average_request_time", 0.00039733688471126213, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "mknotifyd",
            None,
            "heute",
            "{}",
            {},
            "OMD heute Notification Spooler",
            0,
            "Version: 2020.06.08, Spooler running",
            [
                ("last_updated", 20, None, None, None, None),
                ("new_files", 0, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "mknotifyd",
            None,
            "stable",
            "{}",
            {},
            "OMD stable Notification Spooler",
            0,
            "Version: 1.6.0-2020.06.05, Spooler running",
            [
                ("last_updated", 12, None, None, None, None),
                ("new_files", 0, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "mounts",
            "fs_mount_options",
            "/",
            "['errors=remount-ro', 'relatime', 'rw']",
            ["errors=remount-ro", "relatime", "rw"],
            "Mount options of /",
            0,
            "Mount options exactly as expected",
            [],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "mounts",
            "fs_mount_options",
            "/boot",
            "['relatime', 'rw']",
            ["relatime", "rw"],
            "Mount options of /boot",
            0,
            "Mount options exactly as expected",
            [],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "mounts",
            "fs_mount_options",
            "/boot/efi",
            "['codepage=437', 'dmask=0077', 'errors=remount-ro', 'fmask=0077', 'iocharset=iso8859-1', 'relatime', 'rw', 'shortname=mixed']",
            [
                "codepage=437",
                "dmask=0077",
                "errors=remount-ro",
                "fmask=0077",
                "iocharset=iso8859-1",
                "relatime",
                "rw",
                "shortname=mixed",
            ],
            "Mount options of /boot/efi",
            0,
            "Mount options exactly as expected",
            [],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "omd_apache",
            None,
            "heute",
            "None",
            None,
            "OMD heute apache",
            0,
            "WAITING - Counter based check, cannot be done offline",
            [
                ("requests_images", 0.0, None, None, None, None),
                ("requests_cmk_other", 0.0, None, None, None, None),
                ("requests_cmk_snapins", 0.0, None, None, None, None),
                ("requests_styles", 0.0, None, None, None, None),
                ("requests_scripts", 0.0, None, None, None, None),
                ("requests_cmk_wato", 0.0, None, None, None, None),
                ("requests_cmk_views", 0.0, None, None, None, None),
                ("requests_cmk_bi", 0.0, None, None, None, None),
                ("requests_cmk_dashboards", 0.0, None, None, None, None),
                ("requests_nagvis_snapin", 0.0, None, None, None, None),
                ("requests_nagvis_ajax", 0.0, None, None, None, None),
                ("requests_nagvis_other", 0.0, None, None, None, None),
                ("requests_other", 0.0, None, None, None, None),
                ("secs_cmk_other", 0.0, None, None, None, None),
                ("secs_cmk_snapins", 0.0, None, None, None, None),
                ("secs_scripts", 0.0, None, None, None, None),
                ("secs_cmk_wato", 0.0, None, None, None, None),
                ("secs_images", 0.0, None, None, None, None),
                ("secs_styles", 0.0, None, None, None, None),
                ("secs_cmk_views", 0.0, None, None, None, None),
                ("secs_cmk_bi", 0.0, None, None, None, None),
                ("secs_cmk_dashboards", 0.0, None, None, None, None),
                ("secs_nagvis_snapin", 0.0, None, None, None, None),
                ("secs_nagvis_ajax", 0.0, None, None, None, None),
                ("secs_nagvis_other", 0.0, None, None, None, None),
                ("secs_other", 0.0, None, None, None, None),
                ("bytes_scripts", 0.0, None, None, None, None),
                ("bytes_styles", 0.0, None, None, None, None),
                ("bytes_cmk_other", 0.0, None, None, None, None),
                ("bytes_cmk_snapins", 0.0, None, None, None, None),
                ("bytes_cmk_wato", 0.0, None, None, None, None),
                ("bytes_images", 0.0, None, None, None, None),
                ("bytes_cmk_views", 0.0, None, None, None, None),
                ("bytes_cmk_bi", 0.0, None, None, None, None),
                ("bytes_cmk_dashboards", 0.0, None, None, None, None),
                ("bytes_nagvis_snapin", 0.0, None, None, None, None),
                ("bytes_nagvis_ajax", 0.0, None, None, None, None),
                ("bytes_nagvis_other", 0.0, None, None, None, None),
                ("bytes_other", 0.0, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "omd_apache",
            None,
            "stable",
            "None",
            None,
            "OMD stable apache",
            0,
            "WAITING - Counter based check, cannot be done offline",
            [
                ("requests_cmk_other", 0.0, None, None, None, None),
                ("requests_cmk_views", 0.0, None, None, None, None),
                ("requests_cmk_wato", 0.0, None, None, None, None),
                ("requests_cmk_bi", 0.0, None, None, None, None),
                ("requests_cmk_snapins", 0.0, None, None, None, None),
                ("requests_cmk_dashboards", 0.0, None, None, None, None),
                ("requests_nagvis_snapin", 0.0, None, None, None, None),
                ("requests_nagvis_ajax", 0.0, None, None, None, None),
                ("requests_nagvis_other", 0.0, None, None, None, None),
                ("requests_images", 0.0, None, None, None, None),
                ("requests_styles", 0.0, None, None, None, None),
                ("requests_scripts", 0.0, None, None, None, None),
                ("requests_other", 0.0, None, None, None, None),
                ("secs_cmk_other", 0.0, None, None, None, None),
                ("secs_cmk_views", 0.0, None, None, None, None),
                ("secs_cmk_wato", 0.0, None, None, None, None),
                ("secs_cmk_bi", 0.0, None, None, None, None),
                ("secs_cmk_snapins", 0.0, None, None, None, None),
                ("secs_cmk_dashboards", 0.0, None, None, None, None),
                ("secs_nagvis_snapin", 0.0, None, None, None, None),
                ("secs_nagvis_ajax", 0.0, None, None, None, None),
                ("secs_nagvis_other", 0.0, None, None, None, None),
                ("secs_images", 0.0, None, None, None, None),
                ("secs_styles", 0.0, None, None, None, None),
                ("secs_scripts", 0.0, None, None, None, None),
                ("secs_other", 0.0, None, None, None, None),
                ("bytes_cmk_other", 0.0, None, None, None, None),
                ("bytes_cmk_views", 0.0, None, None, None, None),
                ("bytes_cmk_wato", 0.0, None, None, None, None),
                ("bytes_cmk_bi", 0.0, None, None, None, None),
                ("bytes_cmk_snapins", 0.0, None, None, None, None),
                ("bytes_cmk_dashboards", 0.0, None, None, None, None),
                ("bytes_nagvis_snapin", 0.0, None, None, None, None),
                ("bytes_nagvis_ajax", 0.0, None, None, None, None),
                ("bytes_nagvis_other", 0.0, None, None, None, None),
                ("bytes_images", 0.0, None, None, None, None),
                ("bytes_styles", 0.0, None, None, None, None),
                ("bytes_scripts", 0.0, None, None, None, None),
                ("bytes_other", 0.0, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "systemd_units.services_summary",
            "systemd_services_summary",
            "Summary",
            "{}",
            {"states": {"active": 0, "failed": 2, "inactive": 0}, "states_default": 2},
            "Systemd Service Summary",
            0,
            "138 services in total, Service 'kubelet' activating for: 0.00 s, 5 disabled services",
            [],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "tcp_conn_stats",
            "tcp_conn_stats",
            None,
            "tcp_conn_stats_default_levels",
            {},
            "TCP Connections",
            0,
            "CLOSE_WAIT: 5, ESTABLISHED: 13, FIN_WAIT2: 1, LISTEN: 21, SYN_SENT: 1, TIME_WAIT: 108",
            [
                ("CLOSED", 0, None, None, None, None),
                ("CLOSE_WAIT", 5, None, None, None, None),
                ("CLOSING", 0, None, None, None, None),
                ("ESTABLISHED", 13, None, None, None, None),
                ("FIN_WAIT1", 0, None, None, None, None),
                ("FIN_WAIT2", 1, None, None, None, None),
                ("LAST_ACK", 0, None, None, None, None),
                ("LISTEN", 21, None, None, None, None),
                ("SYN_RECV", 0, None, None, None, None),
                ("SYN_SENT", 1, None, None, None, None),
                ("TIME_WAIT", 108, None, None, None, None),
            ],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "old",
            "uptime",
            "uptime",
            None,
            "{}",
            {},
            "Uptime",
            0,
            "Up since Tue Jun  2 07:50:48 2020, uptime: 7 days, 7:30:46",
            [("uptime", 631846.94, None, None, None, None)],
            {},
            ["heute"],
        ),
        CheckPreviewEntry(
            "active",
            "cmk_inv",
            None,
            "Check_MK HW/SW Inventory",
            "{}",
            {},
            "Check_MK HW/SW Inventory",
            None,
            "WAITING - Active check, cannot be done offline",
            [],
            {},
            ["heute"],
        ),
    ],
    host_labels={"cmk/check_mk_server": {"plugin_name": "labels", "value": "yes"}},
    output="+ FETCHING DATA\n [agent] Using data from cache file /omd/sites/heute/tmp/check_mk/cache/heute\n [agent] Use cached data\n [piggyback] Execute data source\nNo piggyback files for 'heute'. Skip processing.\nNo piggyback files for '127.0.0.1'. Skip processing.\n+ EXECUTING DISCOVERY PLUGINS (29)\nkernel does not support discovery. Skipping it.\n+ EXECUTING HOST LABEL DISCOVERY\n",
    new_labels={},
    vanished_labels={},
    changed_labels={},
)


@pytest.fixture(name="mock_discovery_preview")
def fixture_mock_discovery_preview(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cmk.gui.watolib.services.discovery_preview", return_value=mock_discovery_result
    )


@pytest.fixture(name="mock_discovery")
def fixture_mock_discovery(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("cmk.gui.watolib.services.discovery", return_value=None)


@pytest.fixture(name="mock_set_autochecks")
def fixture_mock_set_autochecks(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cmk.gui.watolib.services.set_autochecks", return_value=SetAutochecksResult()
    )


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_discovery_fails_on_invalid_content_type(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_discovery_preview: MagicMock,
    mock_set_autochecks: MagicMock,
) -> None:
    resp = aut_user_auth_wsgi_app.post(
        f"{base}/domain-types/service_discovery_run/actions/start/invoke",
        params='{"mode": "foo", "host_name": "example.com"}',
        headers={"Accept": "application/json"},
        status=415,
    )
    assert "Content type not valid" in resp.json["title"]
    mock_discovery_preview.assert_not_called()
    mock_set_autochecks.assert_not_called()


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_discovery_on_invalid_mode(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_discovery_preview: MagicMock,
    mock_set_autochecks: MagicMock,
) -> None:
    resp = aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/service_discovery_run/actions/start/invoke",
        params='{"mode": "foo", "host_name": "example.com"}',
        content_type="application/json",
        headers={"Accept": "application/json"},
        status=400,
    )
    assert resp.json["detail"] == "These fields have problems: mode"
    mock_discovery_preview.assert_not_called()
    mock_set_autochecks.assert_not_called()


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_discovery_refresh_services(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_discovery_preview: MagicMock,
    mock_set_autochecks: MagicMock,
) -> None:
    resp = aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/service_discovery_run/actions/start/invoke",
        params='{"mode": "refresh", "host_name": "example.com"}',
        content_type="application/json",
        headers={"Accept": "application/json"},
        status=302,
    )
    assert (
        resp.location
        == "http://localhost/NO_SITE/check_mk/api/1.0/objects/service_discovery_run/example.com/actions/wait-for-completion/invoke"
    )
    assert mock_discovery_preview.mock_calls == [
        call("NO_SITE", "example.com", prevent_fetching=True, raise_errors=False),
        call("NO_SITE", "example.com", prevent_fetching=False, raise_errors=False),
        call("NO_SITE", "example.com", prevent_fetching=True, raise_errors=False),
    ]
    mock_set_autochecks.assert_not_called()


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_discovery_tabula_rasa(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_set_autochecks: MagicMock,
    mock_discovery_preview: MagicMock,
    mock_discovery: MagicMock,
) -> None:
    aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/service_discovery_run/actions/start/invoke",
        params='{"mode": "tabula_rasa", "host_name": "example.com"}',
        content_type="application/json",
        headers={"Accept": "application/json"},
        status=302,
    )
    mock_set_autochecks.assert_not_called()
    assert mock_discovery.mock_calls == [
        call(
            "NO_SITE",
            "refresh",
            ["example.com"],
            scan=True,
            raise_errors=False,
            non_blocking_http=True,
        )
    ]
    assert mock_discovery_preview.mock_calls == [
        call("NO_SITE", "example.com", prevent_fetching=True, raise_errors=False),
        call("NO_SITE", "example.com", prevent_fetching=True, raise_errors=False),
    ]


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_discovery_disable_and_re_enable_one_service(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_discovery_preview: MagicMock,
    mock_set_autochecks: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch(
        # one would like to mock the call in the library and not the import. WHY????
        "cmk.gui.watolib.services.get_services_labels",
        return_value=GetServicesLabelsResult(labels=defaultdict(lambda: {})),
    )
    aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/service_discovery_run/actions/start/invoke",
        params='{"mode": "refresh", "host_name": "example.com"}',
        content_type="application/json",
        headers={"Accept": "application/json"},
        status=302,
    )
    resp = aut_user_auth_wsgi_app.call_method(
        "get",
        f"{base}/objects/service_discovery/example.com",
        headers={"Accept": "application/json"},
        status=200,
    )
    mock_discovery_preview.reset_mock()

    df_boot_ignore = aut_user_auth_wsgi_app.follow_link(
        resp,
        "cmk/service.move-ignored",
        json_data=resp.json["extensions"]["check_table"]["df-/boot"],
        headers={"Accept": "application/json"},
        status=204,
    )
    assert df_boot_ignore.text == ""
    mock_discovery_preview.assert_called_once()
    mock_discovery_preview.reset_mock()
    mock_set_autochecks.assert_called_once_with(
        "NO_SITE",
        "example.com",
        {
            ("cpu.loads", None): ("CPU load", "cpuload_default_levels", {}, ["heute"]),
            ("cpu.threads", None): ("Number of threads", "{}", {}, ["heute"]),
            ("df", "/boot/efi"): (
                "Filesystem /boot/efi",
                "{'include_volume_name': False}",
                {},
                ["heute"],
            ),
            ("kernel.performance", None): ("Kernel Performance", "{}", {}, ["heute"]),
            ("kernel.util", None): ("CPU utilization", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 0"): ("Temperature Zone 0", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 1"): ("Temperature Zone 1", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 2"): ("Temperature Zone 2", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 3"): ("Temperature Zone 3", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 4"): ("Temperature Zone 4", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 5"): ("Temperature Zone 5", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 6"): ("Temperature Zone 6", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 7"): ("Temperature Zone 7", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 8"): ("Temperature Zone 8", "{}", {}, ["heute"]),
            ("mkeventd_status", "heute"): ("OMD heute Event Console", "{}", {}, ["heute"]),
            ("mkeventd_status", "stable"): ("OMD stable Event Console", "{}", {}, ["heute"]),
            ("mknotifyd", "heute"): ("OMD heute Notification Spooler", "{}", {}, ["heute"]),
            ("mknotifyd", "stable"): ("OMD stable Notification Spooler", "{}", {}, ["heute"]),
            ("mounts", "/"): (
                "Mount options of /",
                "['errors=remount-ro', 'relatime', 'rw']",
                {},
                ["heute"],
            ),
            ("mounts", "/boot"): (
                "Mount options of /boot",
                "['relatime', 'rw']",
                {},
                ["heute"],
            ),
            ("mounts", "/boot/efi"): (
                "Mount options of /boot/efi",
                "['codepage=437', 'dmask=0077', 'errors=remount-ro', 'fmask=0077', 'iocharset=iso8859-1', 'relatime', 'rw', 'shortname=mixed']",
                {},
                ["heute"],
            ),
            ("omd_apache", "heute"): ("OMD heute apache", "None", {}, ["heute"]),
            ("omd_apache", "stable"): ("OMD stable apache", "None", {}, ["heute"]),
            ("systemd_units.services_summary", "Summary"): (
                "Systemd Service Summary",
                "{}",
                {},
                ["heute"],
            ),
            ("tcp_conn_stats", None): (
                "TCP Connections",
                "tcp_conn_stats_default_levels",
                {},
                ["heute"],
            ),
            ("uptime", None): ("Uptime", "{}", {}, ["heute"]),
        },
    )
    mock_set_autochecks.reset_mock()

    df_boot_monitor = aut_user_auth_wsgi_app.follow_link(
        resp,
        "cmk/service.move-monitored",
        json_data=resp.json["extensions"]["check_table"]["df-/boot"],
        headers={"Accept": "application/json"},
        status=204,
    )
    assert df_boot_monitor.text == ""
    mock_discovery_preview.assert_called_once()
    mock_set_autochecks.assert_called_once_with(
        "NO_SITE",
        "example.com",
        {
            ("cpu.loads", None): ("CPU load", "cpuload_default_levels", {}, ["heute"]),
            ("cpu.threads", None): ("Number of threads", "{}", {}, ["heute"]),
            ("df", "/boot/efi"): (
                "Filesystem /boot/efi",
                "{'include_volume_name': False}",
                {},
                ["heute"],
            ),
            ("df", "/boot"): (
                "Filesystem /boot",
                {"include_volume_name": False},
                {},
                ["heute"],
            ),
            ("kernel.performance", None): ("Kernel Performance", "{}", {}, ["heute"]),
            ("kernel.util", None): ("CPU utilization", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 0"): ("Temperature Zone 0", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 1"): ("Temperature Zone 1", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 2"): ("Temperature Zone 2", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 3"): ("Temperature Zone 3", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 4"): ("Temperature Zone 4", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 5"): ("Temperature Zone 5", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 6"): ("Temperature Zone 6", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 7"): ("Temperature Zone 7", "{}", {}, ["heute"]),
            ("lnx_thermal", "Zone 8"): ("Temperature Zone 8", "{}", {}, ["heute"]),
            ("mkeventd_status", "heute"): ("OMD heute Event Console", "{}", {}, ["heute"]),
            ("mkeventd_status", "stable"): (
                "OMD stable Event Console",
                "{}",
                {},
                ["heute"],
            ),
            ("mknotifyd", "heute"): ("OMD heute Notification Spooler", "{}", {}, ["heute"]),
            ("mknotifyd", "stable"): (
                "OMD stable Notification Spooler",
                "{}",
                {},
                ["heute"],
            ),
            ("mounts", "/"): (
                "Mount options of /",
                "['errors=remount-ro', 'relatime', 'rw']",
                {},
                ["heute"],
            ),
            ("mounts", "/boot"): (
                "Mount options of /boot",
                "['relatime', 'rw']",
                {},
                ["heute"],
            ),
            ("mounts", "/boot/efi"): (
                "Mount options of /boot/efi",
                "['codepage=437', 'dmask=0077', 'errors=remount-ro', 'fmask=0077', 'iocharset=iso8859-1', 'relatime', 'rw', 'shortname=mixed']",
                {},
                ["heute"],
            ),
            ("omd_apache", "heute"): ("OMD heute apache", "None", {}, ["heute"]),
            ("omd_apache", "stable"): ("OMD stable apache", "None", {}, ["heute"]),
            ("systemd_units.services_summary", "Summary"): (
                "Systemd Service Summary",
                "{}",
                {},
                ["heute"],
            ),
            ("tcp_conn_stats", None): (
                "TCP Connections",
                "tcp_conn_stats_default_levels",
                {},
                ["heute"],
            ),
            ("uptime", None): ("Uptime", "{}", {}, ["heute"]),
        },
    )


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_discover_single_service(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_discovery_preview: MagicMock,
    mock_set_autochecks: MagicMock,
) -> None:
    resp = aut_user_auth_wsgi_app.call_method(
        "put",
        f"{base}/objects/host/example.com/actions/update_discovery_phase/invoke",
        params='{"check_type": "systemd_units_services_summary", "service_item": "Summary", "target_phase": "monitored"}',
        headers={"Accept": "application/json"},
        content_type="application/json",
        status=204,
    )
    assert resp.text == ""
    mock_discovery_preview.assert_called_once()
    # TODO: This seems to be a bug. Might be caused by the fact that the service is currently not
    # known to the host. I have not verified this. But in case something like this happens, the
    # endpoint should fail with some error instead instead of continuing silently.
    mock_set_autochecks.assert_not_called()


def test_openapi_bulk_discovery_with_default_options(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
) -> None:
    # create some sample hosts
    aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/host_config/actions/bulk-create/invoke",
        params=json.dumps(
            {
                "entries": [
                    {
                        "host_name": "foobar",
                        "folder": "/",
                    },
                    {
                        "host_name": "sample",
                        "folder": "/",
                    },
                ]
            }
        ),
        status=200,
        headers={"Accept": "application/json"},
        content_type="application/json",
    )

    resp = aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/discovery_run/actions/bulk-discovery-start/invoke",
        status=200,
        params=json.dumps(
            {
                "hostnames": ["foobar", "sample"],
            }
        ),
        headers={"Accept": "application/json"},
        content_type="application/json",
    )
    assert resp.json["id"] == "bulk_discovery"
    assert resp.json["title"].endswith("is active") or resp.json["title"].endswith(
        "is finished"
    ), resp.json
    assert "active" in resp.json["extensions"]
    assert "state" in resp.json["extensions"]
    assert "result" in resp.json["extensions"]["logs"]
    assert "progress" in resp.json["extensions"]["logs"]

    status_resp = aut_user_auth_wsgi_app.call_method(
        "get",
        base + f"/objects/discovery_run/{resp.json['id']}",
        status=200,
        headers={"Accept": "application/json"},
    )
    assert status_resp.json["id"] == resp.json["id"]
    assert "active" in status_resp.json["extensions"]

    # TODO: additional tests for bulk discovery modes (CMK-10160)


def test_openapi_bulk_discovery_with_invalid_hostname(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
) -> None:
    aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/discovery_run/actions/bulk-discovery-start/invoke",
        status=400,
        params=json.dumps({"hostnames": ["wrong_hostname"]}),
        headers={"Accept": "application/json"},
        content_type="application/json",
    )


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_refresh_job_status(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_discovery_preview: MagicMock,
) -> None:
    host_name = "example.com"

    aut_user_auth_wsgi_app.call_method(
        "get",
        f"{base}/objects/service_discovery_run/example.com/actions/wait-for-completion/invoke",
        headers={"Accept": "application/json"},
        status=404,
    )

    aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/domain-types/service_discovery_run/actions/start/invoke",
        params='{"mode": "refresh", "host_name": "example.com"}',
        content_type="application/json",
        headers={"Accept": "application/json"},
        status=302,
    )

    aut_user_auth_wsgi_app.call_method(
        "get",
        f"{base}/objects/service_discovery_run/example.com/actions/wait-for-completion/invoke",
        headers={"Accept": "application/json"},
        status=204,
    )

    resp = aut_user_auth_wsgi_app.call_method(
        "get",
        base + f"/objects/service_discovery_run/{host_name}",
        status=200,
        headers={"Accept": "application/json"},
    )
    assert resp.json["id"] == resp.json["id"]
    assert "active" in resp.json["extensions"]
    assert "state" in resp.json["extensions"]
    assert "result" in resp.json["extensions"]["logs"]
    assert "progress" in resp.json["extensions"]["logs"]


@pytest.mark.usefixtures("with_host", "inline_background_jobs")
def test_openapi_deprecated_execute_discovery_endpoint(
    base: str,
    aut_user_auth_wsgi_app: WebTestAppForCMK,
    mock_discovery_preview: MagicMock,
) -> None:
    aut_user_auth_wsgi_app.call_method(
        "post",
        f"{base}/objects/host/example.com/actions/discover_services/invoke",
        params='{"mode": "refresh"}',
        content_type="application/json",
        headers={"Accept": "application/json"},
        status=302,
    )
