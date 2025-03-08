# Copyright 2023 Accent Communications

import argparse
import sys

from visualplan.analyzer import DialplanExecutionAnalyzer
from visualplan.dialplan import DialplanParser
from visualplan.html import HTMLVisualizer
from visualplan.log import LogParser


def main():
    parsed_args = _parse_args(sys.argv[1:])

    log_parser = LogParser()
    dialplan_parser = DialplanParser()
    dialplan_analyzer = DialplanExecutionAnalyzer()

    log_parse_result = log_parser.parse_file(parsed_args.log_file)
    analyses = []
    for diaplan_file in parsed_args.dialplan_files:
        dialplan_parse_result = dialplan_parser.parse_file(diaplan_file)
        analyses.append(dialplan_analyzer.analyze(dialplan_parse_result, log_parse_result))

    visualizer = HTMLVisualizer('visualplan.html')
    visualizer.write(analyses)


def _parse_args(args):
    parser = _new_argument_parser()
    return parser.parse_args(args)


def _new_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('log_file', help='asterisk log file')
    parser.add_argument('dialplan_files', nargs='+', help='dialplan files')
    return parser


if __name__ == '__main__':
    main()
