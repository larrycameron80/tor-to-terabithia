#!/usr/bin/env python3

from collections import namedtuple
import csv
import socket
import random

WordList = namedtuple("WordList", ['conjunctions', 'others'])

def load_wordlist(filename):
    wordlist = WordList([], []) # A totally empty list.
    with open(filename) as wordlist_file:
        for line in wordlist_file:
            # Check that the line is valid; if not, skip it.
            split_line = line.strip('\n').split(',')
            if len(split_line) != 2:
                continue
            else:
                # Line was valid; get the part of speech and put it in the right bin
                if split_line[1] == 'c':
                    if split_line[0] in wordlist.conjunctions:
                        pass
                    else:
                        wordlist.conjunctions.append(split_line[0])
                else:
                    if split_line[0] in wordlist.others:
                        pass
                    else:
                        wordlist.others.append(split_line[0])
    return wordlist

# A short explaination of the format.
# Conjunctions delimit portions of the bridge line
# This may not fool a human but it will probably fool high-throughput NLP systems
#   for a few more years.
# <offset> <address type> <conjunction> <octet_1> <conjunction> <octet_2> <conjunction> <octet_3> ... etc

def encode_ip(addr, wordlist):
    addr_is_ipv6 = False
    return_string = ""
    try:
        socket.inet_aton(addr)
    except socket.error:
        # Not a valid IPv4 address
        try:
            socket.inet_pton(socket.AF_INET6, addr)
            # This line won't get reached if the conversion failed
            addr_is_ipv6 = True
        except socket.error:
            # Not a valid IP address at all!
            raise ValueError("Tried to encode an invalid IP address.")

    # Now we know what to encode; let's do it!
    if addr_is_ipv6:
        raise NotImplementedError("IPv6 isn't done yet.")
    else:
        octets = addr.split('.')
        offset = random.randint(0, len(wordlist.others) - 255)
        print("Offset: {}".format(offset))
        # We subtract from the length of the list because we need headroom to encode in
        return_string += wordlist.others[offset] + " "
        return_string += wordlist.others[offset + 1] + " " # 1 means IPv4
        return_string += random.choice(wordlist.conjunctions) + " "
        for octet in octets:
            return_string += wordlist.others[int(octet) + offset] + " "
            return_string += random.choice(wordlist.conjunctions) + " "

        return return_string

def decode_ip(encoded_ip, wordlist):
    decoded_ip = ""
    words = encoded_ip.split(" ")

    # Get the offset so we can decode the rest
    offset = wordlist.others.index(words[0])
    print("Offset: {}".format(offset))
    
    # Get the IP address type
    addr_is_ipv6 = False
    if words[1] == wordlist.others[offset + 1]:
        print("Format appears to be IPv4.")
        addr_is_ipv6 = False
    elif words[1] == wordlist.others[offset + 2]:
        print("Format appears to be IPv6.")
        addr_is_ipv6 = True
    else:
        raise ValueError("Malformed input - no such address type ({})."\
                .format(wordlist.others.index(words[1]) - offset))
    if addr_is_ipv6:
        raise NotImplementedError("IPv6 isn't done yet.")
    else:
        looking_for_conjunction = True
        for word in words[2:]:
            # Don't do anything on blank words.
            if word == '':
                continue
            if looking_for_conjunction:
                # We want to find a conjunction here
                if not (word in wordlist.conjunctions):
                    raise ValueError("Malformed input.")
                else:
                    looking_for_conjunction = False
            else:
                # This word is part of the IP address.
                decoded_ip += str(wordlist.others.index(word) - offset) + '.'
                looking_for_conjunction = True

        return decoded_ip[:-1]
