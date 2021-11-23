
import datetime
import hashlib
import os

def now():
    return datetime.datetime.now()

def get_time_relative_now(seconds):
    return now() + datetime.timedelta(seconds=seconds)

def md5(s:str):
    hl = hashlib.md5()
    hl.update(s.encode("utf-8"))
    return hl.hexdigest()

def generate_token():
    return hashlib.sha1(os.urandom(24)).hexdigest()