from datetime import datetime
import time

from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys

def return_most_recent_file():

    #print(os.getcwd() + '/static/images/pdfs')
    #Relative or absolute path to the directory
    dir_path = os.getcwd() + '/hello/static/images/pdfs'

    #all entries in the directory w/ stats
    data = (os.path.join(dir_path, fn) for fn in os.listdir(dir_path))
    data = ((os.stat(path), path) for path in data)

    # regular files, insert creation date
    data = ((stat[ST_CTIME], path)
               for stat, path in data if S_ISREG(stat[ST_MODE]))

    all_items = []
    for cdate, path in sorted(data):
        all_items.append(os.path.basename(path))

    most_recent = all_items[-1]
    name_to_return = most_recent.replace('pdf.pdf', '')

    return name_to_return

return_most_recent_file()
