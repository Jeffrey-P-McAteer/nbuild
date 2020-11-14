
"""
Misc. utilities which are not specific to any module
"""

import hashlib
import shutil
import os

def hash16(data):
    """
    Return a hex string of the data's hash. Currently uses md5.
    """
    hash_object = hashlib.md5(bytes(data, 'utf-8'))
    return hash_object.hexdigest()

def deflate_dir(dst_path):
    """
    We move files up until there is more than 1 item at the root (dst_path)
    This avoids messy issues where we extract to "ABC/" and get
    "ABC/ABC-1.2.3/<actual stuff we wanted under ABC>"
    """
    remaining_loops = 5
    while len(os.listdir(dst_path)) < 2 and remaining_loops > 0:
        remaining_loops -= 1
        # Move everything in dst_path/<directory>/* into dst_path
        child_dir = os.path.join(dst_path, os.listdir(dst_path)[0])
        for child_f in os.listdir(child_dir):
            shutil.move(os.path.join(child_dir, child_f), os.path.join(dst_path, child_f))
        os.rmdir(child_dir)

