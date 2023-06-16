#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, u_n_packer
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

version = 'v0.1'
copyright_name = 'Lampe2020'
print(f'PyPacker {version} - © {copyright_name}')

unpacker_skel = """%{u_n_packer}

orig_file = {'name': os.path.realpath(__file__), 'compiled': %{do_recompile}}
do_repack = %{do_repack}
unpacker_gui = %{unpacker_gui}

extr_path = extract(data=%{data}, run=%{cmd}, keep=do_repack)

if do_repack:
    # The strange 'replace __ for %' stuff below is there to prevent the packer from messing up this template.
    unpacker_skel = %{unpacker_skel}.replace('__{unpacker_skel}'.replace('__', '%'), unpacker_skel)
    unpacker_skel = unpacker_skel.replace('__{do_recompile}'.replace('__', '%'), orig_file['compiled'])
    unpacker_skel = unpacker_skel.replace('__{do_repack}-.replace('__', '%'), do_repack)
    unpacker_skel = unpacker_skel.replace('__{unpacker_gui}'.replace('__', '%'), unpacker_gui)
    unpacker_skel = unpacker_skel.replace('__{cmd}'.replace('__', '%'), repr(%{cmd})) # repr to also insert the correct quotes
    unpacker_skel = unpacker_skel.replace('__{data}'.replace('__', '%'), archive(extr_path))
    
    with open(orig_file['name'], 'w') as f:
        f.write(unpacker_skel.replace('__{unpacker_skel}'.replace('__', '%'), unpacker_skel))
        del unpacker_skel # get rid of the potentially large string, now that it's written to a file
    
    if orig_file['compiled']:
        PyInstaller.__main__.run([
            '%{progname}.py',
            '--onefile'
        ])
        shutil.move(('dist/%{progname}.exe' if sys.platform.startswith('win') else 'dist/%{progname}'), sys.executable) # sys.executable points to the packed EXE if packed,
        # see https://pyinstaller.org/en/stable/runtime-information.html#using-sys-executable-and-sys-argv-0
"""
