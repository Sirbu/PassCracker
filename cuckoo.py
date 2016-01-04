# python 2.x

import os
import sys
import hashlib
import crypt

from passlib.hash import sha512_crypt

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

        # displaying user information
        if not (passwd_data == "x" or passwd_data == "!" or passwd_data =="!!"):
            print "[+] Cracking password for user '" + user +"'"

            # a number that defines which algorithm
            # has been used to hash the password
            # ex: 6 is SHA2-512
            hash_type = passwd_data.split('$')[1]
            salt = passwd_data.split('$')[2]
            password = passwd_data.split('$')[3]

            # print "[DEBUG] Here is the hash type : " + "'" + hash_type + "'"
            # print "[DEBUG] Here is the salt : " + "'" + salt + "'"
            # print "[DEBUG] Here is the password : " + "'" + password + "'"

            testPass(hash_type, salt, password)

def testPass(hash_type, salt, password):
    if len(password) == 0:
        print "[E] The password is null !"
        exit(4)

    # default dictionnary, must give the possibility
    # to choose another one
    dictionnary = "simple_dico.txt"

    dico = open(dictionnary, 'r')

    # for the moment I only do the sha512
    # algorithm. But later, I'll use the hash_type
    # variable to determine which algo must be used
    cpt = 0
    for word in dico.readlines():
        # first we must strip out the newline
        # because it was causing the problem
        # I've been trying to solve for several hours...
        # Off course the hash was different that the one
        # in the password file... BECAUSE THERE IS NO NEWLINE
        # IN THE PASSWORD FILE !
        word = word.strip('\n')

        # creating hash of the word
        # the result will have the follwing
        # form : $id$salt$Password
        # so the password must be extracted
        dico_hash = crypt.crypt(word, '$'+hash_type+'$'+salt+'$')

        pass_hash = dico_hash.split('$')[3]

        if password == pass_hash:
            print "Password found => " + word
            return

        cpt = cpt+1

        print "[+] Word tested : " + str(cpt) + " -> " + word + "\r",
        # print "[DEBUG] Hash generated : " + dico_hash.digest() + " -- " +       "password hash : " + password

    print "No password found..."


if __name__ == "__main__":
    main()
