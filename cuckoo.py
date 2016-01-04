# python 2.x

import os
import sys
import crypt

def checkFile(filename):
    if not os.path.isfile(filename):
        print "[-] The file " + filename + " does not exist !"
        exit(2)
    elif not os.access(filename, os.R_OK):
        print "[-] Access denied to " + filename
        exit(3)

def main():
    if len(sys.argv) < 3:
        print "[E] Usage : " + sys.argv[0] + " <password_file.txt>  <dictionnary.txt>"
        exit(1)

    # First we check the arguments
    password_file = sys.argv[1]
    dictionnary_file = sys.argv[2]
    checkFile(password_file)
    checkFile(dictionnary_file)

    print "[+] Openning file " + password_file + "read-only mode..."
    fic = open(password_file, 'r')

    print "[+] Some information may not be displayed because of reasons..."

    for line in fic.readlines():
        # the password data contains the id,
        # the salt and the hashed password
        user = line.split(':')[0]
        passwd_data = line.split(':')[1]

        # displaying user information
        if not (passwd_data == "x" or passwd_data == "!" or passwd_data =="!!"):
            print "[+] Cracking password for user '" + user +"'"

            # the variable salt is composed of the
            # id of the algorithm used to hash and
            # the cryptgraphic salt : "$id$salt"
            # the variable password is the hashed
            # password stored in the password file
            salt = passwd_data.split('$')[1:3]
            password = passwd_data.split('$')[3]

            testPass(salt, password, dictionnary_file)

def testPass(salt, password, dictionnary_file):
    if len(password) == 0:
        print "[E] The password is null !"
        exit(4)

    dico = open(dictionnary_file, 'r')

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
        dico_hash = crypt.crypt(word, '$'+salt[0]+'$'+salt[1]+'$')

        pass_hash = dico_hash.split('$')[3]

        if password == pass_hash:
            print "Password found => " + word
            return

        cpt = cpt+1

        print "[+] Word tested : " + str(cpt) + "\r",
        # print "[DEBUG] Hash generated : " + dico_hash.digest() + " -- " +       "password hash : " + password

    print "No password found..."


if __name__ == "__main__":
    main()
