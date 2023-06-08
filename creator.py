#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dateien in 7z-Archiv einfügen, evtl. mit Passwortschutz und auf jeden fall in 100mb-Teile zerteilt,
die dann in b-Strings eingelagert werden um direkt auf die Festplatte geschrieben und wieder entpackt werden zu können.
"""

import gzip #TODO: l2db3 fertig machen, hier reinkopieren

def compress(data:bytes) -> bytes:
    """GZip-compresses `data`."""
    return gzip.compress(data)

def decompress(data:bytes) -> bytes:
    """GZip-decompresses `data`."""
    return gzip.decompress(data)

