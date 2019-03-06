import csv, hashlib
hashed = hashlib.sha224("hello")

def writecsv(username,password):
    with open('data.csv','a') as csvfile:
        write = csv.writer(csvfile)
        write.writerow([username,password])
        
def readcsv():
    with open('data.csv', 'rb') as csvfile:
        read = csv.reader(csvfile)
        listify = list(read)
        return listify
        
filelist = readcsv()

def checkexist(username):
    for x in filelist:
        if(x[0] == username):
            return True
    return False

print checkexist("smalick")
print checkexist("sachal")
print checkexist("w")
print filelist
print hashed.hexdigest()
print hashlib.sha224("hello").hexdigest()

