import ftplib
import time
ftp = ftplib.FTP('192.168.21.209', 'jwrickman18', 'Heap!860')
ftp.cwd('Desktop/code/robo-control')
past = time.time()
gFile = open("ftpTest.txt", "wb")
ftp.retrbinary('RETR ftptestFile.txt', gFile.write)
gFile.close()
ftp.quit()
print "\nReadme File Output:"
gFile = open("ftpTest.txt", "r")
buff = gFile.read()
print buff
print time.time() - past
gFile.close()
