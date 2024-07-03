import hashlib
import datetime

def hash_file(filename, algorithm='sha256', chunk_size=4096):
    hash_obj = hashlib.new(algorithm)
    with open(filename, 'rb') as file:
        while chunk := file.read(chunk_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def get_current_date_time():
    now = datetime.datetime.now()
    date = str(now.date())
    hour = str(now.hour)
    minute = str(now.minute)
    return "_".join([date, f"{hour}:{minute}"])