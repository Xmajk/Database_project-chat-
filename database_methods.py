import pyodbc
from datetime import datetime

def arr_of_id_all_i_have(conn,username):
    cursor=conn.cursor()
    cursor.execute("exec mp_obdzel_id ?",(username))
    arr=[]
    for i in cursor.fetchall():
        arr.append(i[0])
    return arr

def arr_of_id_all_i_send(conn,username):
    cursor=conn.cursor()
    cursor.execute("exec mp_sended_id ?",(username))
    arr=[]
    for i in cursor.fetchall():
        arr.append(i[0])
    return arr

def get_id_by_username(conn,username):
    cursor=conn.cursor()
    cursor.execute("exec mp_select_id_by_username ?",(username))
    return cursor.fetchone()[0]
def arr_of_all_users(conn):
    #conn=pyodbc.connect()
    cursor=conn.cursor()
    cursor.execute("exec mp_select_all_users")
    arr=[]
    for i in cursor.fetchall():
        arr.append(i[0])
    return arr
def send_mssg(conn,od,pro,predmet,text):
    cursor=conn.cursor()
    cas = datetime.now()
    cas= cas.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("insert into MHMssgs(predmet,od,pro,txt,odeslano) values(?,?,?,?,?)",(predmet,get_id_by_username(conn,od),get_id_by_username(conn,pro),text,cas))
    cursor.commit()
    return True

def get_basic_dorucene(conn,username):
    cursor=conn.cursor()
    cursor.execute("exec mp_select_dorucene_basic ?",(username))
    return cursor.fetchall()

def delete_dorucene(conn,id):
    cursor=conn.cursor()
    cursor.execute("exec mp_delete_pro ?",(id))
    cursor.commit()
    
def get_zprava(conn,id):
    cursor=conn.cursor()
    cursor.execute("exec mp_select_mssg_by_id ?",(id))
    return cursor.fetchone()

def get_basic_dorucene_limit(conn,username,lim):
    cursor=conn.cursor()
    cursor.execute("exec mp_select_dorucene_basic_limit ?,?",(username,lim))
    return cursor.fetchall()

def delete_odeslane(conn,id):
    cursor=conn.cursor()
    cursor.execute("exec mp_delete_od ?",(id))
    cursor.commit()
    
def get_basic_odeslane(conn,username):
    cursor=conn.cursor()
    cursor.execute("exec mp_select_odeslane_basic ?",(username))
    return cursor.fetchall()

def get_basic_odeslane_limit(conn,username,lim):
    cursor=conn.cursor()
    cursor.execute("exec mp_select_odeslane_basic_limit ?,?",(username,lim))
    return cursor.fetchall()