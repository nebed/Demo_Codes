#!/usr/bin/python
import argparse
import sys
import ftplib
import os
from multiprocessing import Pool

'''
Parse command line arguments to provide input
'''
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--fserver", required=True,
	help="ftp server IP or URL")
ap.add_argument("-u", "--user", required=True,
	help="ftp user")
ap.add_argument("-p", "--pass", required=True,
	help="ftp password")
ap.add_argument("-i", "--source", required=True,
	help="directory in ftp server")
ap.add_argument("-o", "--dest", required=True,
	help="destination locations")
args = vars(ap.parse_args())

server = args['fserver']
user = args['user']
password = args['pass']
source = args['source']
DESTINATION = args['dest']


#function to download files from ftp server
def downloadFiles(filename):
    if(filename.lower().endswith(('.csv'))):
        try:
            ftp.retrbinary("RETR " + filename, open(os.path.join(DESTINATION, filename + '.proc'),"wb").write)
            print("Downloaded: " + filename)
            #rename processed file
            os.rename(filename+'.proc', filename)
            try:
                ftp.delete(filename)
            except ftplib.error_perm:
                print("Error: could not delete " + filename)
            except ftplib.error_reply:
                print("Error: could not delete " + filename)
        except:
            print("Error: File could not be downloaded " + filename)
        return


#function to return files to be downloaded from correct directory
def ftpConnect(path):
    try:
        ftp.cwd(path)       
        os.chdir(DESTINATION)
    except OSError:     
        pass
    except ftplib.error_perm:       
        print("Error: could not change to " + path)
        sys.exit("Ending Application")
    filelist=ftp.nlst()
    return filelist


#multiprocess download of files
if __name__ == '__main__':
#function to establish ftp connection
    ftp = ftplib.FTP(server)
    ftp.login(user, password)
    filelist = ftpConnect(source)
    pool = Pool()
    pool.map(downloadFiles, filelist)
    pool.close() 
    pool.join()


