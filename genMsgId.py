__author__ = 'ajeetjha'

import md5
from datetime import datetime

def genNewId():
    seed = datetime.now()
    id = md5.new(str(seed))

    return id.hexdigest()
