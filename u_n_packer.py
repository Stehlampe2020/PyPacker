#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python3-based application (un)packer.
"""

verbose = True

import gzip, os, sys, tempfile, traceback, shutil, l2db, PyInstaller.__main__

def compile(*args):
    return multiprocessing.Process(target=PyInstaller.__main__.run, args=(args,)).start()

def list_only_files_in(path:str)->list:
    return [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

def list_only_dirs_in(path:str)->list:
    return [file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))]

def find_files(path:str, pathlist:list=[])->list:
    for dir in list_only_dirs_in(path):
        try:
            pathlist.append(os.path.join(path, dir, ''))
            find_files(os.path.join(path, dir), pathlist)
        except Exception as e:
            print(f"Could not list directory '{dir}' because of {type(e).__name__}: {e}") #verbose
    for file in list_only_files_in(path):
        pathlist.append(os.path.join(path, file))
    return pathlist

def archive(from_dir:str)->bytes:
    """Puts all files from `from_dir` into a GZip-compressed L2DB and returns that."""
    errs = 0
    db = l2db.L2DB()
    if verbose: print(f'Reading directory structure in {from_dir}')
    for path in find_files(from_dir):
        if verbose: print(f'Packing: {path}')
        if path[-1]==os.path.sep: # Is a directory
            db[path.removeprefix(from_dir if from_dir[-1]==os.path.sep else os.path.join(from_dir, ''))] = b''
        else: # Is a file
            try:
                with open(os.path.join(from_dir, path), 'rb') as file:
                    db[path] = file.read()
            except Exception as e:
                traceback.print_exception(e) # Notify the user of the error
                errs+=1
    print(f'Files packed! ({errs} errors occurred)')
    return gzip.compress(db.syncout_db()) # Return GZip-compressed DB

def extract(data:bytes, run:str='', keep:bool=False)->str:
    """Extracts all files from the GZip-compressed L2DB to `to_dir` and returns the `to_dir` path."""
    tmpdir, cwd = tempfile.mkdtemp(), os.getcwd()
    if verbose: print(f'Extracting to: {tmpdir}')
    errs = 0
    db = l2db.L2DB(source=gzip.decompress(data))
    for path in db:
        if verbose: print(f'Extracting {os.path.join(tmpdir, path)}')
        try:
            if path[-1]==os.path.sep:
                os.mkdir(path.join(tmpdir, path))
            else:
                with open(os.path.join(tmpdir, path), 'wb') as file:
                    file.write(db[path])
        except Exception as e:
            traceback.print_exception(e)
            errs+=1
    print(f'Files extracted! ({errs} errors occurred)')

    try:
        if run:
            if verbose: print(f'Executing in {tmpdir}: {run}')
            os.chdir(tmpdir)
            os.system(run)
        if not keep:
            shutil.rmtree(tmpdir)
        os.chdir(cwd)
    except Exception as e:
        traceback.print_exception(e)

    return tmpdir