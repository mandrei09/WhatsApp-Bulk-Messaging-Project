import pandas as pd
import time
import methods as met
import textract

#------------------
WAIT_TIME=8
TAB_CLOSE=True
CLOSE_TIME=2
#------------------

met.setScreenDimensions()
print()
message = textract.process("mesaj.docx")
message=message.decode("utf-8")

while True:
    optionNumber=met.start()
    if optionNumber==1: #Trimitere mesaje catre mai multe persoane
            
        # Numerele de telefon extrase din Excel
        phoneNumbers = pd.read_excel(
            io='database.xlsx', 
            sheet_name=2,
            usecols='H'
        )[1:] #1331 a fost ultimul
        #phoneNumbers=['+40743095819']
        
        # Pentru a afisa in terminal progresul
        totalCount=len(phoneNumbers)
        counter=0

        met.startMessage(WAIT_TIME,CLOSE_TIME,totalCount)

        # startTime, endTime, executionTime -> pentru a se afisa cat a durat trimiterea mesajelor in terminal
        startTime=time.time()

        print('--------------------')

        for phoneNumber in phoneNumbers: #1331
            if met.sendMessage(
                phone_no=met.check(phoneNumber),
                message=message,      
                wait_time=WAIT_TIME,         
                
                tab_close=TAB_CLOSE,       
                close_time=CLOSE_TIME        
            ):
                counter+=1
                print('Mesajul s-a trimis la ',counter,'/',totalCount,'numere.')
        
        endTime=time.time()
        break
    
    elif optionNumber==2: #Trimitere mesaje catre mai multe grupuri
             
        # ID-urile de grup extrase din Excel
        # groupIDS = set(pd.read_excel('database.xlsx', sheet_name=2)["ID-uri Grupuri"])

        groupIDS=['DMTX2xBGDjfFijLNhghURJ']*5
        
        # Pentru a afisa in terminal progresul
        totalCount=len(groupIDS)
        counter=0

        met.startMessage()

        # startTime, endTime, executionTime -> pentru a se afisa cat a durat trimiterea mesajelor in terminal
        startTime=time.time()

        print('--------------------')

        for groupID in groupIDS:
            if met.sendMessageToGroup(
                group_id=groupID,
                message=message,      
                wait_time=WAIT_TIME,         
                
                tab_close=TAB_CLOSE,       
                close_time=CLOSE_TIME        
            ):
                counter+=1
                print('Mesajul s-a trimis pe ',counter,'/',totalCount,'grupuri.')
        
        endTime=time.time()
        break
    
    else: #Optiune invalida
        print('--------------------')
        print('Optiune invalida! Introduceti o optiune intre 1 si 2!')
        print('--------------------')
        
executionTime=time.strftime("%H:%M:%S", time.gmtime(endTime-startTime))

if counter==totalCount:  
    print(f'Toate mesajele s-au trimis in {executionTime}!')
else:
    print("""Nu s-au trimis toate mesajele! Verificati fisierul 'mesaje_netrimise.txt' pentru mai multe detalii!""")
    
met.end()