#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2019             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from __future__ import division
import argparse
import sys
import requests
import urllib3  # type: ignore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_arguments(argv)

    sys.stdout.write('<<<check_mk>>>\n')
    for host in args.hosts:
        url_base = "%s://%s:%d" % (args.proto, host, args.port)

        # Sections to query
        # Cluster health: https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-health.html
        # Node stats: https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html
        # Indices Stats: https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-stats.html
        sections = {
            'cluster_health': '/_cluster/health',
            'nodes': '/_nodes/_all/stats',
            'stats': '/*-*/_stats/store,docs',
        }

        try:
            for section in args.modules:
                url = url_base + sections[section]

                auth = (args.user, args.password) if args.user and args.password else None
                try:
                    response = requests.get(url, auth=auth)
                except requests.exceptions.RequestException as e:
                    sys.stderr.write("Error: %s\n" % e)
                    if args.debug:
                        raise
                else:
                    sys.stdout.write("<<<elasticsearch_%s>>>\n" % section)

                json_response = response.json()
                if section == 'cluster_health':
                    handle_cluster_health(json_response)
                elif section == 'nodes':
                    handle_nodes(json_response)
                elif section == 'stats':
                    handle_stats(json_response)
            sys.exit(0)
        except Exception:
            if args.debug:
                raise


def parse_arguments(argv):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-u", "--user", default=None, help="Username for elasticsearch login")
    parser.add_argument("-s", "--password", default=None, help="Password for easticsearch login")
    parser.add_argument(
        "-P",
        "--proto",
        default="https",
        help="Use 'http' or 'https' for connection to elasticsearch (default=https)")
    parser.add_argument("-p",
                        "--port",
                        default=9200,
                        type=int,
                        help="Use alternative port (default: 9200)")
    parser.add_argument(
        "-m",
        "--modules",
        type=lambda x: x.split(' '),
        default="cluster_health nodes stats",
        help=
        "Space-separated list of modules to query. Possible values: cluster_health, nodes, stats (default: all)"
    )
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug mode: let Python exceptions come through")

    parser.add_argument(
        "hosts",
        metavar="HOSTNAME",
        nargs="+",
        help=
        "You can define one or more elasticsearch instances to query. First instance where data is queried wins."
    )

    return parser.parse_args(argv)


def handle_cluster_health(response):
    for item, value in response.iteritems():
        sys.stdout.write("%s %s\n" % (item, value))


def handle_nodes(response):
    nodes_data = response.get("nodes")
    if nodes_data is not None:
        for node in nodes_data:
            node = nodes_data[node]
            proc = node["process"]
            cpu = proc["cpu"]
            mem = proc["mem"]

            sys.stdout.write("%s open_file_descriptors %s\n" %
                             (node["name"], proc["open_file_descriptors"]))
            sys.stdout.write("%s max_file_descriptors %s\n" %
                             (node["name"], proc["max_file_descriptors"]))
            sys.stdout.write("%s cpu_percent %s\n" % (node["name"], cpu["percent"]))
            sys.stdout.write("%s cpu_total_in_millis %s\n" % (node["name"], cpu["total_in_millis"]))
            sys.stdout.write("%s mem_total_virtual_in_bytes %s\n" %
                             (node["name"], mem["total_virtual_in_bytes"]))


def handle_stats(response):
    shards = response.get("_shards")
    if shards is not None:
        sys.stdout.write("<<<elasticsearch_shards>>>\n")

        sys.stdout.write("%s %s %s\n" %
                         (shards.get("total"), shards.get("successful"), shards.get("failed")))

    docs = response.get("_all", {}).get("total")
    if docs is not None:
        sys.stdout.write("<<<elasticsearch_cluster>>>\n")
        count = docs.get("docs", {}).get("count")
        size = docs.get("store", {}).get("size_in_bytes")

        sys.stdout.write("%s %s\n" % (count, size))

    indices_data = response.get("indices")
    if indices_data is not None:
        indices = set()

        sys.stdout.write("<<<elasticsearch_indices>>>\n")
        for index in indices_data:
            indices.add(index.split("-")[0])
        for indice in list(indices):
            all_counts = []
            all_sizes = []
            for index in indices_data:
                if index.split("-")[0] == indice:
                    all_counts.append(
                        indices_data.get(index, {}).get("primaries", {}).get("docs",
                                                                             {}).get("count"))
                    all_sizes.append(
                        indices_data.get(index, {}).get("total", {}).get("store",
                                                                         {}).get("size_in_bytes"))
            sys.stdout.write("%s %s %s\n" %
                             (indice, sum(all_counts) / len(all_counts),
                              sum(all_sizes) / len(all_sizes)))  # fixed: true-division
