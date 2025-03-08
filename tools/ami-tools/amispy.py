#!/usr/bin/env python3

import socket
import argparse
import sys

def parse_message(lines):
    message = []
    for line in lines:
        key, _, value = line.partition(":")
        message.append((key.strip(), value.strip()))
    return message


def format_message(message):
    return "\n".join("%s: %s" % (key, value) for key, value in message) + "\n\n"


def accumulate_lines(reader):
    line = reader.readline()
    lines = []

    while line.strip() != "":
        lines.append(line)
        line = reader.readline()

    return lines


def connect(conn, username, password):
    message = [
        ('Action', 'login'),
        ('Username', username),
        ('Secret', password),
    ]

    data = format_message(message).encode('utf-8')  # Encode the string to bytes

    conn.send(data)


def pretty_print(message):
    for line in message:
        print("%s: %s" % line)
    print()


def filtered(message, accepted, excluded):
    if not message or len(message[0]) < 2:
        return True  # or handle the error as needed

    event_type = message[0][1]

    if len(accepted) > 0:
        return event_type not in accepted

    if len(excluded) > 0:
        return event_type in excluded

    return False

def main():

    parser = argparse.ArgumentParser('read events from AMI')
    parser.add_argument('-u', '--username', default='', help='username for AMI login')
    parser.add_argument('-p', '--password', default='', help='password for AMI login')
    parser.add_argument('-e', '--exclude', default='', help='comma-separated list of events to exclude (Case-sensitive)')
    parser.add_argument('-a', '--accept', default='', help='comma-separated list of events to accept (Case-sensitive)')
    parser.add_argument('-H', '--host', default='localhost', help='AMI host')
    parser.add_argument('-P', '--port', type=int, default=5038, help='AMI port')

    args = parser.parse_args()

    excluded = args.exclude.split(',') if args.exclude else []
    accepted = args.accept.split(',') if args.accept else []

    if len(excluded) > 0 and len(accepted) > 0:
        print("ERROR: cannot use exclude and accept list at the same time")
        sys.exit(1)

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((args.host, args.port))
    reader = conn.makefile()

    #skip asterisk header
    reader.readline()

    print("connecting...")
    connect(conn, args.username, args.password)

    while True:
        lines = accumulate_lines(reader)
        if lines:
            message = parse_message(lines)
            if not filtered(message, accepted, excluded):
                pretty_print(message)
        else:
            break

if __name__ == "__main__":
    main()
