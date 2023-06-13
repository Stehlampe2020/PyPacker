#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter, subprocess
from tkinter import messagebox

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
        import PyInstaller.__main__
        PyInstaller.__main__.run([
            
        ])
        shutil.move(f'dist/%{progname}', sys.executable) # sys.executable points to the packed EXE if packed,
        # see https://pyinstaller.org/en/stable/runtime-information.html#using-sys-executable-and-sys-argv-0
"""

class TerminalWindow(tkinter.Frame):
    def __init__(self, master, command):
        super().__init__(master)
        self.master = master
        command = command.split('') if type(command) == str else command if type(command) == list else\
                                                                                                 ['echo', 'No command!']
        self.pack(fill=tkinter.BOTH, expand=True)

        # Create a Text widget to display the terminal output
        self.terminal_output = tkinter.Text(self, bg='#250826', fg='#c8c8c8', wrap=tkinter.WORD)
        self.terminal_output.pack(fill=tkinter.BOTH, expand=True)

        # Start a subprocess to run the terminal command
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                                                                  stdin=subprocess.PIPE)

        # Create a separate thread to continuously update the terminal output
        self.update_terminal()

    def update_terminal(self):
        # Read the output from the subprocess
        output = self.process.stdout.readline().decode('utf-8')

        if output:
            # Insert the output into the Text widget
            self.terminal_output.insert(tkinter.END, output)
            self.terminal_output.see(tkinter.END)  # Scroll to the bottom

        # Schedule the next update after 10ms
        self.master.after(10, self.update_terminal)

window = tkinter.Tk()
window.title(f'PyPacker {version} - © {copyright_name}')

t_frame = TerminalWindow(window, )