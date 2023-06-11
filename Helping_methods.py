import hashlib
import json
import rich
from rich.console import Console
from rich.style import Style
import time
from termcolor import colored

console=Console()
eprint=console.print
einput=console.input
banned_chars=[";"]

# funkce na zahešování hesla
def hashing(string):
    hash_object = hashlib.sha224()
    hash_object.update(string.encode())
    return hash_object.hexdigest()

#funkce, která načte konfigurační soubor
def read_config(config_url):
    try:
        with open(config_url,"r") as open_file:
            return dict(json.load(open_file))
    except:
        eprint(f'Konfigurace na adrese \"{config_url}\" není přítomna',style="red")
        time.sleep(0.5)
        return None

#funkce na validaci přezdívky
def validate_username(username):
    if len(username)<4:
        print(colored("Username musí být dlouhý minimálně 4 písmena","red"))
        return False
    if len(username)>50:
        print(colored("Username musí být dlouhý maximálně 50 písmen","red"))
        return False
    return True

#funkce na validaci hesla
def validate_password(psswd):
    bool=True
    if len(psswd)<8:
        print(colored("Heslo musí být dlouhé minimálně 8 písmena","red"))
        bool=False
    if not any(char.isupper() for char in psswd):
        print(colored("Heslo musí obsahova minimálně jedno velké písmeno","red"))
        bool=False
    if not any(char.isnumeric() for char in psswd):
        print(colored("Heslo musí obsahova minimálně jednu číslici","red"))
        bool=False
    if any(char in banned_chars for char in psswd):
        print(colored(f'Heslo nesmí obsahova ani jeden znak z {banned_chars}',"red"))
        bool=False
    return bool