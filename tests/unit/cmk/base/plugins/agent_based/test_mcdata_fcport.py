#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.base.plugins.agent_based.mcdata_fcport import parse_mcdata_fcport
from cmk.base.plugins.agent_based.utils.interfaces import Interface


def test_parse_mcdata_fcport() -> None:
    assert parse_mcdata_fcport(
        [
            [
                "1",
                "2",
                "4",
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                "0",
            ],
            [
                "2",
                "1",
                "3",
                [0, 0, 1, 146, 209, 24, 114, 84],
                [0, 0, 0, 0, 27, 195, 137, 220],
                [0, 0, 0, 0, 198, 226, 194, 153],
                [0, 0, 0, 0, 1, 249, 185, 120],
                [0, 0, 0, 0, 0, 0, 0, 0],
                "0",
            ],
            [
                "32",
                "1",
                "3",
                [0, 0, 0, 53, 6, 92, 201, 237],
                [0, 0, 0, 0, 222, 78, 147, 38],
                [0, 0, 0, 0, 26, 119, 228, 49],
                [0, 0, 0, 0, 1, 26, 227, 84],
                [0, 0, 0, 0, 0, 0, 0, 0],
                "0",
            ],
        ],
    ) == [
        Interface(
            index="01",
            descr="01",
            alias="01",
            type="6",
            speed=0,
            oper_status="2",
            in_octets=0,
            in_ucast=0,
            in_mcast=0,
            in_bcast=0,
            in_discards=0,
            in_errors=0,
            out_octets=0,
            out_ucast=0,
            out_mcast=0,
            out_bcast=0,
            out_discards=0,
            out_errors=0,
            out_qlen=0,
            oper_status_name="down",
            total_octets=0,
        ),
        Interface(
            index="02",
            descr="02",
            alias="02",
            type="6",
            speed=2000000000,
            oper_status="1",
            in_octets=2064761100,
            in_ucast=36144795,
            in_mcast=0,
            in_bcast=0,
            in_discards=0,
            in_errors=0,
            out_octets=8123033736776,
            out_ucast=3700628163,
            out_mcast=0,
            out_bcast=0,
            out_discards=0,
            out_errors=0,
            out_qlen=0,
            oper_status_name="up",
            total_octets=8125098497876,
        ),
        Interface(
            index="32",
            descr="32",
            alias="32",
            type="6",
            speed=2000000000,
            oper_status="1",
            in_octets=16547413172,
            in_ucast=20495714,
            in_mcast=0,
            in_bcast=0,
            in_discards=0,
            in_errors=0,
            out_octets=1045961420308,
            out_ucast=492267494,
            out_mcast=0,
            out_bcast=0,
            out_discards=0,
            out_errors=0,
            out_qlen=0,
            oper_status_name="up",
            total_octets=1062508833480,
        ),
    ]
