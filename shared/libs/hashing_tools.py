import os, sys, json, shutil, getpass, atexit, time, hashlib

this_dir = libs_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.dirname(libs_dir)
cache_path = os.path.join(shared_dir_path, "cache")

def underscore_nonalnum(input_string):
    return "".join([c if c.isalnum() else "_" for c in input_string])

def hybrid_hashname(full_hashable_string,hash_length=6,filename_length=64):
    hashstring = hashlib.md5(full_hashable_string.encode()).hexdigest()
    filename = underscore_nonalnum(full_hashable_string[:filename_length-len(hashstring)]) + "_" + hashstring[:hash_length]
    return filename

def hybrid_hash_filename(filename,hash_length=6,filename_length=64):
    noext = ".".join(filename.split(".")[:-1])
    ext = filename.split(".")[-1]
    return hybrid_hashname(noext,hash_length,filename_length) + "." + ext
