#!/usr/bin/python
#
############################################
#
# This python script is intended to copy a
# database from one server to another.
#
############################################

import os, sys
import subprocess
import time
import pdb;
import argparse;

parser = argparse.ArgumentParser(usage='%(prog)s [source_hostname] [source_user] [source_db] [target_hostname] [target_user]')
parser.add_argument("source_hostname", help="Source Mysql Hostname")
parser.add_argument("source_user", help="Source Mysql Username")
parser.add_argument("source_db", help="Database to be migrated")
parser.add_argument("target_hostname",help="Target Mysql Hostname")
parser.add_argument("target_user", help="Target Mysql Username")
args = parser.parse_args()

# Check for arguments
if (len(sys.argv) != 6):
    print("Error: Incorrect number of arguments " + str(len(sys.argv)) + ". Type migratedb.py -h for usage")
    sys.exit(1)

# Get Parameters
source_hostname = str(sys.argv[1])
source_user = str(sys.argv[2])
source_db = str(sys.argv[3])
target_hostname = str(sys.argv[4])
target_user = str(sys.argv[5])


timestamp = str(int(time.time()))
filename = "dump_" + source_hostname + "-" + timestamp + ".sql";

# Database backup function
def runbackup(source_hostname, source_user, source_db):
    if not source_db:
        mysql_db_opt = "-all-databases"
    else:
        mysql_db_opt = "--databases " + source_db

    try:
        print("Connecting to source host: %s" % source_hostname)
        p = subprocess.Popen("mysqldump -h" + source_hostname + " -u" + source_user + " -p " + mysql_db_opt + " > " + filename , shell=True)
        output, error = p.communicate()

        if(p.returncode != 0):
            raise
        print("Backup done for", source_hostname)
        p.terminate()
        p.kill()

    except subprocess.CalledProcessError as e:
        print("Backup failed for", source_hostname)
        print(e.output)

# Restore database
def restoredb(target_hostname, target_user, source_db):
    filepath = os.getcwd()
    files = os.listdir(filepath)
    #print("Files in '%s': %s" % (filepath, files))

    #pdb.set_trace()
    try:
        print("Connecting to target host: %s" % target_hostname)
        r = subprocess.Popen("mysql -h" + target_hostname  + " -u " + target_user + " -p " +  " < " + filepath + "/" + filename , shell=True)
        output, error = r.communicate()

        if(r.returncode != 0):
            raise
        print("Restore done for", target_hostname)

    except subprocess.CalledProcessError as e:
        print("Restore failed for", target_hostname)
        print(e.ouput)
        

if __name__=="__main__":
    #Backup DB
    runbackup(source_hostname,source_user,source_db)

    time.sleep(10)

    #Restore DB
    restoredb(target_hostname,target_user,source_db)

