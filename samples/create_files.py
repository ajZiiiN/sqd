
import sys
from datetime import datetime
import md5

def genNewId():
    seed = datetime.now()
    id = md5.new(str(seed))

    return id.hexdigest()

size_in_kb = 100
count = 1

if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 2:
    size_in_kb = int(sys.argv[1])
elif len(sys.argv) == 3:
    size_in_kb = int(sys.argv[1])
    count = int(sys.argv[2])


fileName = None
for c in range(1,count+1):
    fileName = str(c)+"___"+ str(datetime.now()).replace(" ","__")
    with open("data/"+str(fileName),"w") as fd:
        for i in range(0,(1000/32) * size_in_kb):
                fd.write( genNewId() )


# Run: python create_files.py 100 5  || creates 5 files each of 100KB
# Run: python create_files.py 500    || creates 1 file of 500 KB