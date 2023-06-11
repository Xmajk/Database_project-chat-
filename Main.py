import pyodbc as databaze
from Helping_methods import hashing,read_config,validate_password as vp,validate_username as vu
from database_methods import arr_of_all_users,send_mssg,get_basic_dorucene,arr_of_id_all_i_have,delete_dorucene,get_zprava,get_basic_dorucene_limit,arr_of_id_all_i_send,delete_odeslane,get_basic_odeslane,get_basic_odeslane_limit
import json
import time
import sys
from rich.console import Console
from rich.style import Style
from rich.color import Color
from getpass import getpass
from termcolor import colored
import cmd
from enum import Enum

class Tag(Enum):
    dorucene="dorucene"
    odeslane="odeslane"

console = Console()
config_url="konfig\\file.json"
main_user=None
eprint=console.print
einput=console.input

class User:
    _instance = None
    def __init__(self,username):
        self.username=username
    
    @classmethod
    def get_instance(cls, username):
        if not cls._instance:
            cls._instance = cls(username)
        return cls._instance

def login():
    global conn
    try:
        username=input(colored("Username: ","white"))
        #heslo=einput("Heslo: ",password=True)
        heslo = getpass(prompt=colored("Zadejte heslo: ", "white"))
    except KeyboardInterrupt:
        sys.exit()
    except:
        return login()
    try:
        cursor=conn.cursor()
        cursor.execute("SELECT * from MHUsers where username=(?)",(username))
    except SystemError:
        print(colored("Databáze neodpovídá","red"))
        time.sleep(3)
        sys.exit()
    except databaze.ProgrammingError:
        eprint(f'Databáze hlásí chybu',style="red")
        return None
    try:
        tmp_id,tmp_username,tmp_psswd=cursor.fetchone()
    except TypeError:
        eprint(f"Uživatelské jméno \"{username}\" není v databázi",style="red")
        return None
    if tmp_psswd==hashing(heslo):
        eprint("Úspěšně jste se přihlásil",style="green")
        time.sleep(0.5)
        tmp_user=User.get_instance(username)
        return tmp_user
    else:
        eprint("Neúspěšné přihlášení",style="red")
        time.sleep(0.75)
        return None

def register():
    global conn
    cursor=conn.cursor()
    try:
        username=input(colored("Username: ","white"))
        if not vu(username):
            return
        heslo=getpass(prompt=colored("Zadejte heslo: ", "white"))
        heslo_two=getpass(prompt=colored("Zadejte heslo znovu: ", "white"))
    except KeyboardInterrupt:
        sys.exit()
    if not heslo==heslo_two:
        print(colored("Hesla nejsou stejná","red"))
    if not vp(heslo):
        return
    if len(heslo)==0:
        eprint("Heslo nesmí být prázdné",style="red")
        time.sleep(0.5)
    try:
        cursor.execute("Insert into MHUsers(username,psswd) values(?,?)",(username,hashing(heslo)))
        conn.commit()
        print(f'{colored("Úspěšně jste zaregistrovali uživatele","green")} {colored(username,"cyan")} {colored("do databáze","green")}')
    except databaze.ProgrammingError:
        eprint(f'Databáze hlásí chybu',style="red")
        return None
    except SystemError:
        print(colored("Databáze neodpovídá","red"))
        time.sleep(3)
        sys.exit()
    except databaze.IntegrityError:
        print(colored(f'Vámi zadané uživatelské jménu \"{username}\" už má jiný uživatel',"red"))
        return
    except Exception as e:
        register()
        
class MainCMD(cmd.Cmd):
    intro = f'{colored("Vítejte v konzolové aplikaci, pro nápovědu napište příkaz ","green")}{colored("help","magenta")}'
    def __init__(self,user):
        super().__init__()
        self.user=user
        #self.prompt=f'{self.user.username}>'
        self.prompt=colored(f'{self.user.username}>', 'light_green')
        self.poslat_cmd=SendCMD(self.user,root=self.prompt)
        self.dorucene_cmd=DoruceneCMD(self.user,root=self.prompt)
        self.odeslane_cmd=OdeslaneCMD(self.user,root=self.prompt)
        
    def do_dorucene(self,*args):
        self.dorucene_cmd.cmdloop()
    
    def do_poslat(self,*args):
        self.poslat_cmd.cmdloop()
    
    def do_odeslane(self,*args):
        self.odeslane_cmd.cmdloop()

    def emptyline(self):
        # Zabrání volání příkazu s prázdným vstupem.
        pass

    def default(self, line):
        # Zpracování neznámého příkazu.
        print(colored(f'Neznámý příkaz: \"{line}\". Zkuste to znovu.',"red"))

    def do_kill_app(self, line):
        # Metoda pro ukončení aplikace.
        sys.exit()
    
    def do_help(self,*args):
        print(colored('Dostupné příkazy:',"magenta"))
        print(colored('-    poslat',"magenta"))
        print(colored('-    dorucene',"magenta"))
        print(colored('-    odeslane',"magenta"))
        print(colored('-    kill_app',"magenta"))

class SendCMD(cmd.Cmd):
    def __init__(self,user,root=""):
        super().__init__()
        self.user=user
        self.prompt=f'{root}{colored("poslat>","cyan")}'
        
    def emptyline(self):
        # Zabrání volání příkazu s prázdným vstupem.
        pass

    def default(self, line):
        # Zpracování neznámého příkazu.
        print(colored(f'Neznámý příkaz: \"{line}\". Zkuste to znovu.',"red"))

    def do_kill_app(self, line):
        # Metoda pro ukončení aplikace.
        sys.exit()
    
    def do_zpet(self,*args):
        return True
    
    def do_zprava(self,*args):
        try:
            argument=args[0]
        except:
            print(colored("ve zprávě není nebo je špatně zadaný argument","red"))
            return
        argument=argument.split('--', maxsplit=1)
        if len(argument)!=2:
            print(colored("ve zprávě není nebo je špatně zadaný argument","red"))
            return
        argument=argument[1]
        argument=argument.split(';')
        for uzivatel in argument:
            if not uzivatel in arr_of_all_users(conn):
                print(colored(f'Uživatel \"{uzivatel}\" není v databázi',"red"))
                return
        predmet=""
        while predmet=="":
            predmet=input(colored("Předmět: ","cyan"))
            if predmet=="":
                print(colored("Předmět nesmí být prázdný","red"))
                return
        txt =input(colored("text: ","cyan"))
        choice=None
        while not choice in ["ano","ne"]:
            choice=input(colored("Chcete zprávu odeslat [ano],[ne]?","cyan"))
            if choice=="ano":
                for uzivatel in argument:
                    try:
                        send_mssg(conn,self.user.username,uzivatel,predmet,txt)
                    except:
                        print(colored(f'Datábáze hlásí chybu při posílání zprávy uživateli \"{uzivatel}\"',"red"))
                        return
            elif choice=="ne":
                return
        
    
    def do_help(self,*args):
        print(colored('Dostupné příkazy:',"magenta"))
        print(f'{colored("-    zprava","magenta")} {colored("--[username_přijímatele1];[username_přijímatele2];...","cyan")}')
        print(colored("-    zpet","magenta"))
        print(colored('-    kill_app',"magenta"))
        
class DoruceneCMD(cmd.Cmd):
    def __init__(self,user,root=""):
        super().__init__()
        self.user=user
        self.prompt=f'{root}{colored("dorucene>","white")}'
        
    def emptyline(self):
        # Zabrání volání příkazu s prázdným vstupem.
        pass

    def default(self, line):
        # Zpracování neznámého příkazu.
        print(colored(f'Neznámý příkaz: \"{line}\". Zkuste to znovu.',"red"))

    def do_kill_app(self, line):
        # Metoda pro ukončení aplikace.
        sys.exit()
    
    def do_zpet(self,*args):
        return True 
    
    def do_zobrazit_vse(self,*args):
        if args[0]!="":
            try:
                argument=args[0]
                argument=argument.split('--', maxsplit=1)
                argument=argument[1]
                try:
                    argument=int(argument)
                    if argument<1:
                        print(colored(f'Počet zpráv musí být kladné číslo a ne \"{argument}\"',"red"))
                        return
                except:
                    print(colored("Vámi zadaný počet zpráv není číslo","red"))
                    return
                try:
                    data=get_basic_dorucene_limit(conn,self.user.username,argument)
                except:
                    print(colored("Datábáze hlásí chybu","red"))
                    return
                if len(data) ==0:
                    print(colored("Nemáte žádné doručené zprávy","light_yellow"))
                    return
                for id,predmet,odeslano,od in data:
                    print(f'[{id}] {od} => {predmet} {odeslano.strftime("%Y-%m-%d")}')
                return
            except:
                pass
        
        try:
            data=get_basic_dorucene(conn,self.user.username)
        except:
            print(colored("Datábáze hlásí chybu","red"))
            return
        if len(data) ==0:
            print(colored("Nemáte žádné doručené zprávy","light_yellow"))
            return
        for id,predmet,odeslano,od in data:
            print(f'[{id}] {od} => {predmet} {odeslano.strftime("%Y-%m-%d")}')
     
    def do_help(self,*args):
        print(colored('Dostupné příkazy:',"magenta"))  
        print(f'{colored("-    zobrazit_vse","magenta")} {colored("--[počet zobrazených zpráv (nepovinné)]","white")}')
        print(f'{colored("-    rozbalit","magenta")} {colored("--[id zprávy]","white")}')
        print(f'{colored("-    vymazat","magenta")} {colored("--[id zprávy]","white")}')
        print(f'{colored("-    zpet","magenta")}')
        print(colored('-    kill_app',"magenta"))
        
    def do_vymazat(self,*args):
        try:
            argument=args[0]
        except:
            print(colored("ve zprávě není zadaný argument","red"))
            return
        argument=argument.split('--', maxsplit=1)
        if len(argument)!=2:
            print(colored("ve zprávě není nebo je špatně zadaný argument","red"))
            return
        argument=argument[1]
        try:
            argument=int(argument)
        except:
            print(colored("Vámi zadané id není číslo","red"))
            return
        if not argument in arr_of_id_all_i_have(conn,self.user.username):
            print(colored("Tato zpráva není v databázi","red"))
            return
        try:
            delete_dorucene(conn,argument)
            print(colored(f'Zpráva [{argument}] byla úspěšně vymazána',"green"))
        except:
            print(colored(f'Při mazání zprávy [{argument}] nastala chyba'))
  
    def do_rozbalit(self,*args):
        try:
            argument=args[0]
        except:
            print(colored("ve zprávě není zadaný argument","red"))
            return
        argument=argument.split('--', maxsplit=1)
        if len(argument)!=2:
            print(colored("ve zprávě není nebo je špatně zadaný argument","red"))
            return
        argument=argument[1]
        try:
            argument=int(argument)
        except:
            print(colored("Vámi zadané id není číslo","red"))
            return
        if not argument in arr_of_id_all_i_have(conn,self.user.username):
            print(colored("Tato zpráva není v databázi","red"))
            return
        ZpravyCMD(self.user,argument,Tag.dorucene,root=self.prompt).cmdloop()  
        
class OdeslaneCMD(cmd.Cmd):
    def __init__(self,user,root=""):
        super().__init__()
        self.user=user
        self.prompt=f'{root}{colored("odeslane>","light_cyan")}'
        
    def emptyline(self):
        # Zabrání volání příkazu s prázdným vstupem.
        pass

    def default(self, line):
        # Zpracování neznámého příkazu.
        print(colored(f'Neznámý příkaz: \"{line}\". Zkuste to znovu.',"red"))

    def do_kill_app(self, line):
        # Metoda pro ukončení aplikace.
        sys.exit()
    
    def do_zpet(self,*args):
        return True 
    
    def do_zobrazit_vse(self,*args):
        if args[0]!="":
            try:
                argument=args[0]
                argument=argument.split('--', maxsplit=1)
                argument=argument[1]
                try:
                    argument=int(argument)
                    if argument<1:
                        print(colored(f'Počet zpráv musí být kladné číslo a ne \"{argument}\"',"red"))
                        return
                except:
                    print(colored("Vámi zadaný počet zpráv není číslo","red"))
                    return
                try:
                    data=get_basic_odeslane_limit(conn,self.user.username,argument)
                except:
                    print(colored("Datábáze hlásí chybu","red"))
                    return
                if len(data) ==0:
                    print(colored("Nemáte žádné doručené zprávy","light_yellow"))
                    return
                for id,predmet,odeslano,od in data:
                    print(f'[{id}] {od} => {predmet} {odeslano.strftime("%Y-%m-%d")}')
                return
            except:
                pass
        
        try:
            data=get_basic_odeslane(conn,self.user.username)
        except:
            print(colored("Datábáze hlásí chybu","red"))
            return
        if len(data) ==0:
            print(colored("Nemáte žádné odeslané zprávy","light_yellow"))
            return
        for id,predmet,odeslano,od in data:
            print(f'[{id}] {od} => {predmet} {odeslano.strftime("%Y-%m-%d")}')
     
    def do_help(self,*args):
        print(colored('Dostupné příkazy:',"magenta"))  
        print(f'{colored("-    zobrazit_vse","magenta")} {colored("--[počet zobrazených zpráv (nepovinné)]","light_cyan")}')
        print(f'{colored("-    rozbalit","magenta")} {colored("--[id zprávy]","light_cyan")}')
        print(f'{colored("-    vymazat","magenta")} {colored("--[id zprávy]","light_cyan")}')
        print(f'{colored("-    zpet","magenta")}')
        print(colored('-    kill_app',"magenta"))
     
    def do_vymazat(self,*args):
        try:
            argument=args[0]
        except:
            print(colored("ve zprávě není zadaný argument","red"))
            return
        argument=argument.split('--', maxsplit=1)
        if len(argument)!=2:
            print(colored("ve zprávě není nebo je špatně zadaný argument","red"))
            return
        argument=argument[1]
        try:
            argument=int(argument)
        except:
            print(colored("Vámi zadané id není číslo","red"))
            return
        if not argument in arr_of_id_all_i_send(conn,self.user.username):
            print(colored("Tato zpráva není v databázi","red"))
            return
        try:
            delete_odeslane(conn,argument)
            print(colored(f'Zpráva [{argument}] byla úspěšně vymazána',"green"))
        except:
            print(colored(f'Při mazání zprávy [{argument}] nastala chyba'))
            
    def do_rozbalit(self,*args):
        try:
            argument=args[0]
        except:
            print(colored("ve zprávě není zadaný argument","red"))
            return
        argument=argument.split('--', maxsplit=1)
        if len(argument)!=2:
            print(colored("ve zprávě není nebo je špatně zadaný argument","red"))
            return
        argument=argument[1]
        try:
            argument=int(argument)
        except:
            print(colored("Vámi zadané id není číslo","red"))
            return
        if not argument in arr_of_id_all_i_send(conn,self.user.username):
            print(colored("Tato zpráva není v databázi","red"))
            return
        ZpravyCMD(self.user,argument,Tag.odeslane,root=self.prompt).cmdloop()  

#           
class ZpravyCMD(cmd.Cmd):
    def __init__(self,user,id,tag,root=""):
        super().__init__()
        self.user=user
        self.id=id
        self.tag=tag
        self.prompt=f'{root}{colored("[{}]>".format(self.id),"blue")}'  
        
    def emptyline(self):
        # Zabrání volání příkazu s prázdným vstupem.
        pass

    def default(self, line):
        # Zpracování neznámého příkazu.
        print(colored(f'Neznámý příkaz: \"{line}\". Zkuste to znovu.',"red"))

    def do_kill_app(self, line):
        # Metoda pro ukončení aplikace.
        sys.exit()
    
    def do_zpet(self,*args):
        return True 
    
    def do_help(self,*args):
        print(colored('Dostupné příkazy:',"magenta"))  
        print(f'{colored("-    zobrazit","magenta")}')
        print(f'{colored("-    vymazat","magenta")}')
        print(f'{colored("-    zpet","magenta")}')
        print(f'{colored("-    kill_app","magenta")}')
        
    def do_vymazat(self,*args):
        if (self.tag==Tag.dorucene):
            try:
                delete_dorucene(conn,self.id)
                print(colored(f'Zpráva [{self.id}] byla úspěšně vymazána',"green"))
                return True
            except:
                print(colored("Datábáze hlásí chybu","red"))
        elif (self.tag==Tag.odeslane):
            try:
                delete_odeslane(conn,self.id)
                print(colored(f'Zpráva [{self.id}] byla úspěšně vymazána',"green"))
                return True
            except:
                print(colored("Datábáze hlásí chybu","red"))
    
    def do_zobrazit(self,*args):
        try:
            prijimatel,odesilatel,tmp_id,predmet,text,dc_odeslani=get_zprava(conn,self.id)
            print(f'[{tmp_id}]')
            print(f'od: {odesilatel}')
            print(f'pro: {prijimatel}')
            print(f'předmět: {predmet}')
            print(f'odeslano: {dc_odeslani.strftime("%d.%m.%Y %H:%M")}')
            print("zpráva")
            print("---------------------")
            print(text)
            print("---------------------")
        except:
            print(colored("Datábáze hlásí chybu","red"))
            return
        
# připojení k databázi, login, register
konf=None
while konf==None:
    konf=read_config(config_url)
conn=None
try_count=0
ip=True
while conn==None:
    if try_count%5==0 and try_count!=0:
        choice=None
        while choice not in ["ano","ne"]:
            if ip:
                choice=input(colored("Chcete se zkusit přihlásit na local? [ano][ne]","yellow"))
            else:
                choice=input(colored("Chcete se zkusit přihlásit přes heslo? [ano][ne]","yellow"))
            if choice=="ano":
                if ip:
                    ip=False
                else:
                    ip=True
    try:
        if ip:
            conn = databaze.connect(f'DRIVER={konf["ip"]["DRIVER"]};SERVER={konf["ip"]["SERVER"]};DATABASE={konf["ip"]["DATABASE"]};UID={konf["ip"]["UID"]};PWD={konf["ip"]["PWD"]}')
        else:
            conn = databaze.connect(f'DRIVER={konf["local"]["DRIVER"]};SERVER={konf["local"]["SERVER"]};DATABASE={konf["local"]["DATABASE"]};Trusted_Connection={konf["local"]["Trusted_Connection"]}')
    except SystemError:
        print(colored("Databáze neodpovídá","red"))
        time.sleep(3)
        sys.exit()
    except (databaze.ProgrammingError, databaze.InterfaceError):
        eprint(f'Databáze nechce povolit přístup',style="red")
        time.sleep(0.5)  
    except KeyError:
        eprint(f'Konfigura na adrese \"{config_url}\" neobsahuje všechna potřebná data',style="red")
        time.sleep(3)
        sys.exit()   
    except Exception as e:
        print(e)
        eprint(f'Nastala chyba',style="red")
        time.sleep(0.5)
    try_count+=1
if ip:
    console.print(f'Pripojeno k databázi {konf["SERVER"]}',style=Style(color=Color.from_rgb(133, 205, 251)))
else:
    console.print(f'Pripojeno k databázi na localu',style=Style(color=Color.from_rgb(133, 205, 251)))
time.sleep(1.5)

choice=None
while(choice not in [1,2]):
    print(f'{colored("1)přihlásit", "yellow")}')
    print(f'{colored("2)registrovat", "yellow")}')
    try:
        choice=int(input(colored("Váš výběr:", 'black', 'on_light_green')))
    except KeyboardInterrupt:
        sys.exit()
    except:
        continue
    if choice==1:
        main_user=login()
        if main_user==None:choice=None
    elif choice==2:
        register()
        choice=None
#main loop
choice=None
main = MainCMD(main_user)
main.cmdloop()