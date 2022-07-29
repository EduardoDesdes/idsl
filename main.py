#!/bin/python3
# To - Do :D .I.
# -f
import codecs
from hermetrics.metric_comparator import JaroWinkler
import os
import requests
import time
import ast
import subprocess

def ismalicious(sospechoso,comandos):
    for comando in comandos:
        #print(comando)
        mc = JaroWinkler()
        comando=comando[:-1]
        valuexd = mc.similarity(sospechoso, comando)
        print('|'+sospechoso+'|','=','|'+comando+'|','=',valuexd)
        if valuexd > 0.8:
            return True
    return False

def get_user_dictionary(files):
    users={}
    for file in files:
        username=file.split('.')[1]
        users[username]=0
    return users

def get_files(files_command):
    return os.listdir(files_command)

def get_pids(user,files_command):
    pids=[]
    for file_command in files_command:
        if file_command.split('.')[1] == user:
            pids.append(file_command.split('.')[0])
    return pids

def shellkiller(pids):
    for pid in pids:
        os.system("kill -9 "+str(pid)+'>/dev/null 2>&1')

def file_to_score(filename):
    #print(filename)
    user=filename.split('.')[1]
    filename=path+"/commands/"+filename
    score=0
    new_command = ""
    pront=0
    valuepront=""
    with open(filename, 'r', encoding='UTF-8') as file:
        while (line := file.readline().rstrip()):
            line2=','.join(line.split(',')[1:-1])[2:-1]
            #print(line2)
            if line2 == '\\n':
                new_command = codecs.decode(new_command, 'unicode_escape')
                if ismalicious(new_command,malicious_list):
                    score+=1
                new_command=""
                pront=1
                continue
            elif pront == 1:
                valuepront=line2
                pront=0
                continue
            elif valuepront in line2:
                continue
            elif line2 == '"\\7"':
                continue
            else:
                new_command += line2
                continue
    return user,score

def send_message_t(username,chat_id):
    msg="[*] El usuario " + username + " fue detectado como malicioso, todas sus terminales y las proximas estan siendo bloqueadas."
    try:
        url = BASE_URL + TOKEN_API + SEND_MESSAGE + "?chat_id=" + chat_id + "&text=" + msg
        requests.get(url)
    except Exception as e:
        print("")  # al log
    return True

def write_user_in_file(username):
    # Open a file with access mode 'a'
    file_object = open('/root/idsl/users.txt', 'a')
    # Agregando el usuario
    file_object.write(username+'\n')
    # Close the file
    file_object.close()
    return True

def verify_user_not_notified(username):
    with open('/root/idsl/users.txt') as f:
        usuarios_notificados = f.readlines()
    #print("La lista es:",usuarios_notificados)
    for usernoti in usuarios_notificados:
        if usernoti.replace('\n','') == username:
            return False
    return True

#Variables globales
path = '/root/idsl'
malicious_list_file=path+'/command-bank'
limite_comandos_maliciosos = 5

#Telegram env
BASE_URL = "https://api.telegram.org/bot"
TOKEN_API = "5488024266:AAERewqT5sZ7lqwIm_8bjtqoVWjjl4uxPEE"
SEND_MESSAGE = "/sendMessage"

#Iniciamos el validador de strings
#mc = hermetrics.JaroWinkler()

#Leemos el conjunto de comandos maliciosos
with open(malicious_list_file) as f:
    malicious_list = f.readlines()
#print(malicious_list)
#Iniciamos la ejecucion

#Obtenemos la lista de archivos
files_command = get_files(path+"/commands/")

#Obtenemos el diccionario de usuarios en 0
user_scores=get_user_dictionary(files_command)

#Revisamos cada archivo
for file_command in files_command:
    usr,scor=file_to_score(file_command)
    #print('Usuario',usr,"Score:",scor)
    value=user_scores[usr]
    user_scores[usr]=value+scor

#Mostrando el resultado
print("El reporte de los usuarios es:",user_scores)

#Validando cual es un usuario peligroso
bad_users=[]
for key in user_scores:
    if user_scores[key] > limite_comandos_maliciosos:
        bad_users.append(key)

#Obteniendo los PID del usuario peligroso
for bad_user in bad_users:
    print("[*] El usuario",bad_user,"es un intruso!!!")
    bad_user_pids=get_pids(bad_user,files_command)
    print("[*] Los PIDs de",bad_user," son:",bad_user_pids)
    print("[*] Eliminando sus terminales, expulsando usuario")
    shellkiller(bad_user_pids)
    print("[*] Usuario expulsado")
    if verify_user_not_notified(bad_user):
        print("[*] Generando notificacion por telegram")
        send_message_t(bad_user,"189999091")
        print("[*] Registrando la notificacion")
        write_user_in_file(bad_user)
        print("[*] Notificacion enviada")
    else:
        print("[*] El usuario ya esta notificado")