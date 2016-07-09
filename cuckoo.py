# python 2.x
# encoding= utf-8

import os
import sys
import crypt
from threading import *

screeLock = Semaphore(value=1)
wordsTested = 0

def checkFile(filename):
    if not os.path.isfile(filename):
        print("[-] The file " + filename + " does not exist !")
        exit(2)
    elif not os.access(filename, os.R_OK):
        print("[-] Access denied to " + filename)
        exit(3)

def main():
    if len(sys.argv) < 3:
        print("[E] Usage : " + sys.argv[0] + " <password_file.txt>  <dictionnary.txt>")
        exit(1)

    # First we check the arguments
    password_file = sys.argv[1]
    dictionnary_file = sys.argv[2]
    checkFile(password_file)
    checkFile(dictionnary_file)

    print("[+] Openning file " + password_file)
    fic = open(password_file, 'r', encoding='utf-8')

    for line in fic.readlines():
        # the password data contains the id,
        # the salt and the hashed password
        user = line.split(':')[0]
        passwd_data = line.split(':')[1]

        # displaying user information for
        # users that have a password set
        if not (passwd_data == "x" or passwd_data == "!" or passwd_data =="!!"):
            print("[+] Cracking password for user '" + user +"'")

            # the variable salt is composed of the
            # id of the algorithm used to hash and
            # the cryptgraphic salt : "$id$salt"
            # the variable password is the hashed
            # password stored in the password file
            salt = passwd_data.split('$')[1:3]
            password = passwd_data.split('$')[3]

            # impossible to know if it works for the moment.
            # calls to print do not work :(
            t = Thread(target=testPass, args=(salt, password, dictionnary_file, user))
            t.start()

def testPass(salt, password, dictionnary_file, user):
    if len(password) == 0:
        screeLock.acquire()
        print("[E] The password is null !")
        screeLock.release()
        exit(4)

    dico = open(dictionnary_file, 'r', encoding='utf-8')

    # for the moment I only do the sha512
    # algorithm. But later, I'll use the hash_type
    # variable to determine which algo must be used
    cpt = 0
    try:
        for word in dico.readlines():
            # first we must strip out the newline
            # because it was causing the problem
            # I've been trying to solve for several hours...
            # Off course the hash was different that the one
            # in the password file... BECAUSE THERE IS NO NEWLINE
            # AFTER EACH PASSWORD IN THE PASSWORD FILE !
            word = word.strip('\n')

            # creating hash of the word
            # the result will have the follwing
            # form : $id$salt$Password
            # so the password must be extracted
            dico_hash = crypt.crypt(word, '$'+salt[0]+'$'+salt[1]+'$')
            pass_hash = dico_hash.split('$')[3]

            if password == pass_hash:
                screeLock.acquire()
                print("Password found !\n " + word)
                screeLock.release()
                return 0

            cpt = cpt+1

            screeLock.acquire()
            print("[+] Word tested : " + str(cpt), end='\r')
            screeLock.release()

    except Exception as e:
        screeLock.acquire()
        print("[E] Error : " + str(e))
        screeLock.release()
        dico.close()

    print("No password found...")
    return -1

if __name__ == "__main__":
    main()
