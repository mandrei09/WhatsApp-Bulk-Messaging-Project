import re
import webbrowser as web
from urllib.parse import quote
import pyautogui as pg
from pywhatkit.core import core, exceptions, log
import time
import os
import keyboard as k
import ctypes
import time


#------------------
SCALE = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
WIDTH = None
HEIGHT = None
#------------------

def setScreenDimensions():
    if SCALE == 1.0:
        WIDTH = core.WIDTH * 0.90 
        HEIGHT = core.HEIGHT * 0.92
    elif SCALE == 1.25:
        WIDTH = core.WIDTH * 0.961  
        HEIGHT = core.HEIGHT * 0.907
    elif SCALE == 1.5:
        WIDTH = core.WIDTH * 0.96875  
        HEIGHT = core.HEIGHT * 0.9166666667
    elif SCALE == 1.75:
        WIDTH = core.WIDTH * 0.96875  
        HEIGHT = core.HEIGHT * 0.9027777778
    
def errorSending(_time: time.struct_time, receiver: str) -> None:
    
    """Creeaza un fisier.txt cu numerele unde mesajele nu s-au trimis."""
    
    if not os.path.exists("mesaje_netrimise.txt"):
        file = open("mesaje_netrimise.txt", "w+")
        file.close()

    with open("mesaje_netrimise.txt", "a", encoding="utf-8") as file:
        file.write(
            f"Date: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nTime: {_time.tm_hour}:{_time.tm_min}\n"
            f"Phone Number: {receiver}"
        )
        file.write("\n--------------------\n")
        file.close()
    
def check(phoneNumber):
    
    """Verifica daca numarul de telefon dat ca input are structura potrivita, iar daca nu il modifica.\n
    Exemplu structura corecta: +40 123 456 789 sau +40123456789 
    """
    phoneNumber=str(phoneNumber)
    if re.match(r"^\+\d{2} \d{3} \d{3} \d{3}$",phoneNumber) or re.match(r"^\+\d{11}$",phoneNumber):
        return phoneNumber
    elif re.match(r"^\d{9}$",phoneNumber):
        return " ".join(['+40',phoneNumber[:3],phoneNumber[3:6],phoneNumber[6:]])
    return None

# Functie din pywhatkit modificata
def sendMessage(
    phone_no: str, #numarul de telefon
    message: str,  #mesajul pe care vrei sa-l trimiti
    
    wait_time: int = 15, #cate secunde sa astepte inainte sa trimita mesajul, trebuie selectat un timp cat mesajul sa se si trimita
    tab_close: bool = False, #inchiderea tabului de whatsapp dupa trimiterea mesajului (pentru fiecare mesaj trimis se mai deschide un tab)
    close_time: int = 3, #cate secunde sa astepte dupa ce a trimis mesajul
):

    """Trimite un mesaj pe WhatsApp unui numar specificat."""

    if phone_no==None:
        errorSending(_time=time.localtime(), receiver=phone_no)
        return 0
    elif not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")
    else:
        web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)},")
        
        time.sleep(4)
        pg.click(WIDTH,HEIGHT)
        
        time.sleep(wait_time - 4)
        pg.press("enter")
        
        log.log_message(_time=time.localtime(), receiver=phone_no, message=message)
        
        if tab_close:
            core.close_tab(wait_time=close_time)
        return 1
    
    
def sendMessageToGroup(
    group_id: str, #id-ul grupului. https://chat.whatsapp.com/DMTX2xBGDjfFijLNhghURJ => DMTX2xBGDjfFijLNhghURJ
    message: str,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
):
    current_time = time.localtime()

    time.sleep(wait_time)
    core.send_message(message=message, receiver=group_id, wait_time=wait_time)
    log.log_message(_time=current_time, receiver=group_id, message=message)
    if tab_close:
        core.close_tab(wait_time=close_time)
    
def start():
    print('--------------------')   
    print('Alegeti o optiune din lista de mai jos:')
    print('1. Trimiterea unui mesaj mai multor persoane.')
    print('2. Trimiterea unui mesaj pe mai multe grupuri.')
    print('Optiune: ',end='')
    return int(input())
        
def startMessage(WAIT_TIME,CLOSE_TIME,totalCount):
    
    """Afiseaza un warning cand se ruleaza scriptul si asteapta input de la user pentru a incepe."""
    
    print('--------------------')
    print('VA INCEPE PROCESUL DE TRIMITERE AL MESAJULUI INTRODUS LA NUMERELE DE TELEFON MENTIONATE!')
    print('ESTE FOARTE IMPORTANT CA IN TIMPUL TRIMITERII SA NU UTILIZATI CALCULATORUL!')
    print('PROCESUL SE VA TERMINA CAND VA APAREA DIN NOU FEREASTRA TERMINALULUI PE ECRAN!')
    print('Timp estimat: ', time.strftime("%H:%M:%S", time.gmtime((WAIT_TIME + CLOSE_TIME)*totalCount)))
    print('--------------------')
    time.sleep(5)
    
def startMessageGroups():
    """Afiseaza un warning cand se ruleaza scriptul si asteapta input de la user pentru a incepe."""
    
    print('--------------------')
    print('VA INCEPE PROCESUL DE TRIMITERE AL MESAJULUI INTRODUS PE GRUPURILE MENTIONATE!')
    print('ESTE FOARTE IMPORTANT CA IN TIMPUL TRIMITERII SA NU UTILIZATI CALCULATORUL!')
    print('PROCESUL SE VA TERMINA CAND VA APAREA DIN NOU FEREASTRA TERMINALULUI PE ECRAN!')
    print('--------------------')
    time.sleep(5)
    
def end():
    """Schimba ferestrele dupa ce scriptul a terminat de rulat."""
    pg.hotkey('alt', 'tab')
         
# def sendwhats_image(
#     receiver: str,
#     img_path: str,
#     caption: str = "",
#     wait_time: int = 15,
#     tab_close: bool = False,
#     close_time: int = 3,
# ) -> None:
#     """Send Image to a WhatsApp Contact or Group at a Certain Time"""

#     if (not receiver.isalnum()) and (not core.check_number(number=receiver)):
#         raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

#     current_time = time.localtime()
#     core.send_image(
#         path=img_path, caption=caption, receiver=receiver, wait_time=wait_time
#     )
#     log.log_image(_time=current_time, path=img_path, receiver=receiver, caption=caption)
#     if tab_close:
#         core.close_tab(wait_time=close_time)