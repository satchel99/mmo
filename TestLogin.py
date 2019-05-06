import unittest
import csv
def checkexist(username):
    for x in filelist:
        if(x[0] == username):
            return True
    return False
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



class TestLogin(unittest.TestCase):

    def test_login(self):
        val1 = checkexist("smalick")
        val2 = checkexist("sachal")
        val3 = checkexist("w")
        self.assertTrue(val1 and val2 and val3)

if __name__ == '__main__':
    unittest.main()
