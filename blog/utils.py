
import datetime
import hashlib
import os
import random

def now():
    return datetime.datetime.now()

def get_time_relative_now(seconds):
    return now() + datetime.timedelta(seconds=seconds)

def md5(s:str):
    hl = hashlib.md5()
    hl.update(s.encode("utf-8"))
    return hl.hexdigest()

def generate_md5_by_file(file):
    hl = hashlib.md5()
    file.seek(0)
    hl.update(file.read())
    return hl.hexdigest()

def generate_token():
    return hashlib.sha1(os.urandom(24)).hexdigest()

def generate_file_name(dirs,name):
    for _,_,files in os.walk(dirs):
        pass
    file_name = name
    while name in files:
        prefix = ranstr(6)
        part_name_list = name.split(".")
        if len(part_name_list) == 1:
            part_name_list[-1] = "%s_%s"%(part_name_list[-1] , prefix)
        else:
            part_name_list = ["%s_%s"%(".".join(part_name_list[:-1]) , prefix)] + part_name_list[-1:]
        file_name = ".".join(part_name_list)
        name = file_name
    return file_name

def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt

def save_file_to_dir(file,name,dirs):
    file_path = os.path.join(dirs,name)
    with open(file_path,"wb") as f:
        file.seek(0)
        f.write(file.read())

if __name__ == "__main__":
    print(generate_file_name("../media","test.d.g"))