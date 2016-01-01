# python 2.x
# coding= utf-8

import os
import sys
import hashlib

def main():
    if len(sys.argv) != 2:
        print "[E] Please give the path to a password file"
        exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print "[-] The file " + filename + " does not exist !"
        exit(2)
    elif not os.access(filename, os.R_OK):
        print "[-] Access denied to " + filename
        exit(3)

    print "[+] Openning file " + filename + "read-only mode..."
    fic = open(filename, 'r')

    print "[+] Some information may not be displayed because of reasons..."

    for line in fic.readlines():
        user = line.split(':')[0]
        passwd_data = line.split(':')[1]
        # a number that defines which algorithm
        # has been used to hash the password
        # ex: 6 is SHA2-512
        hash_type = passwd_data[1:2]
        password = passwd_data[3:]

        # displaying user information
        if not (passwd_data == "x" or passwd_data == "!" or passwd_data =="!!"):
            print "[+] Cracking password for user '" + user +"'"
            testPass(password, hash_type)

def testPass(password, hash_type):
    if len(password) == 0:
        print "[E] The password is null !"
        exit(4)

    # default dictionnary, must give the possibility
    # to choose another one
    dictionnary = "rockyou.txt"

    dico = open(dictionnary, 'r')

    # for the moment I only do the sha512
    # algorithm. But later, I'll use the hash_type
    # variable to determine which algo must be used
    cpt = 0
    for word in dico.readlines():
        # creating hash of the word
        dico_hash = hashlib.sha512()
        dico_hash.update(word)

        print "[+] Word tested : " + str(cpt) + "\r",

        if password == dico_hash.digest():
            print "Password found => " + word
            return

        cpt = cpt+1

    print "No password found..."


if __name__ == "__main__":
    main()
