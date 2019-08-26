import requests
import json
import os
import time
import urllib.request
from bs4 import BeautifulSoup
import random
import multiprocessing as mp

FILEPATH = os.path.abspath(__file__)
FILEDIR = FILEPATH.replace(os.path.basename(FILEPATH),'')


version = "0.0.5"

def clear():

    os.system('cls')

    os.system('clear')





def init():
    global tokens, a_proxy, useproxy
    clear()
    def remdupe(lis):
        final = []
        seen = []
        for i in lis:
            if i not in seen:
                final.append(i)
                seen.append(i)
        return final
    tokens = open(FILEDIR + 'TOKENS.txt','r').read().split('\n')
    tokens = remdupe(tokens)
    flagged = []
    print('Verifying \'%s\' User Tokens...\n'%(len(tokens)))
    for token in tokens:
        head = {"authorization":token}
        proxies = {}
        url = 'https://discordapp.com/api/v6/activities'
        r = requests.get(url,headers=head)#proxies=proxies
        try:
            js = str(r.json())
            if '\'code\'' in js:
                flagged.append(token)
        except:
            pass


    for i in flagged:
        tokens.remove(i)

    print('Removed \'%s\' Invalid tokens, as listed below: '%(len(flagged)))
    for i in flagged:
        print('>>> \'%s\''%(i))
    
    print('\nContinuing with \'%s\' valid tokens....'%(len(tokens)))
    

    
    
    print('\n\nGathering proxies...')
    a_proxy = open(FILEDIR + 'PROXIES.txt','r').read().split('\n')
    for i in a_proxy:
        try:
            a_proxy.remove(' ')
        except:
            break
    
    if len(a_proxy) == 0:
        print('No proxies found, this could be because the site accessed is blocked in your country.\n\nContinuing with no proxies...\n')
        useproxy = 'DISABLED'

    else:
        print('Found %s Proxies to use..\n\nContinuing...\n'%(len(a_proxy)))
        useproxy = False

    

    time.sleep(6)
    main()
def isint(n):
    try:
        m = int(n)
        return True
    except:
        return False

def chooseRandomProxy():
    global a_proxy
    return a_proxy[random.randint(0,len(a_proxy)-1)]
def action(actionid,tokens):
    global a_proxy, useproxy



    
    if actionid  == '1':
        print('Please paste the invite')
        invite = input('--> ')
        if '/' in invite:
            try:
                invite = invite.replace('https://','')
            except:
                pass
            try:
                invite = invite.replace('discord.gg/','')
            except:
                pass
        
        print('Sending \'%s\' Token bots to invite \'%s\'....'%(len(tokens),invite))
        success = 0

        

        
            
        jobs = []
        man = mp.Manager()
        success = man.Value('i',0)
        for token in tokens:
            def m(s):
                head = {"authorization":token}
                url = 'https://discordapp.com/api/v6/invite/%s'%(invite)

                if useproxy:
                    def k():
                        try:
                            rproxy = chooseRandomProxy()
                            proxies = {'http': rproxy, 'https': rproxy}
                            print('using proxy %s...'%(rproxy))
                            r = requests.post(url,None,headers=head,proxies=proxies,timeout=2)
                        except:
                            print('proxy failed, retrying..')
                            return k()
                    k()
                else:
                    print('not using proxy...')
                    r = requests.post(url,None,headers=head)
                
                try:
                    js = str(r.json())
                    

                    

                    if 'Unknown Invite' in js or 'The user is banned from this guild.' in js or 'You need to verify your account in order to perform this action.' in js or  '404: Not Found' in js:
                        pass
                    else:
                        s.value += 1
                except:
                    s.value += 1
            process = mp.Process(target=m,args=(success,))
            try:
                process.start()
                jobs.append(process)
            except:
                continue
        
        for job in jobs:
            if job != None:
                job.join()
        print('Successfully sent: \'%s\' bots to invite "%s"'%(success.value,invite))




    elif actionid == '2':
        print('Please paste the guild id')
        guildid = input('--> ')

        if len(guildid) != 18 or not isint(guildid):
            print('--- Invalid Guild ID')
            return
        print('Instructing \'%s\' bots to leave guild id: "%s"..'%(len(tokens),guildid))
        
        jobs = []
        man = mp.Manager()
        success = man.Value('i',0)
        for token in tokens:
            def m(s):
                head = {"authorization":token}
                url = 'https://discordapp.com/api/v6/users/@me/guilds/%s'%(guildid)
                if useproxy:
                    def k():
                        try:
                            rproxy = chooseRandomProxy()
                            print('using proxy %s...'%(rproxy))
                            proxies = {'http': rproxy, 'https': rproxy}
                            r = requests.delete(url,headers=head,proxies=proxies,timeout=2)
                        except:
                            print('Proxy failed, retrying..')
                            return k()
                    k()
                else:
                    print('not using proxy...')
                    r = requests.delete(url,headers=head)

                

                try:
                    js = str(r.json())
                    if 'Invalid Guild' in js or 'You need to verify your account in order to perform this action.' in js:
                        pass
                    else:
                        s.value += 1
                except:
                    s.value += 1
                    pass
            process = mp.Process(target=m,args=(success,))
            try:
                process.start()
                jobs.append(process)
            except:
                continue
            
        
        for job in jobs:
            if job != None:
                job.join()
            

        print('Successfully Made: \'%s\' bots leave guild id: "%s"'%(success.value,guildid))
    


    elif actionid == '3':

        print('type target user id')
        userid = input('--> ')

        if len(userid) != 18 and len(userid) != 20 or not isint(userid):
            print('--- Invalid User ID')
            time.sleep(3)
            return

        print('Instructing \'%s\' Bots to friend user \'%s\''%(len(tokens),userid))
        


        
        
        jobs = []
        man = mp.Manager()
        success = man.Value('i',0)


        for token in tokens:
            def m(s):
                head = {"authorization":token,'content-type':'application/json'}
                url = 'https://discordapp.com/api/v6/users/@me/relationships/%s'%(userid)

                if useproxy:
                    def k():
                        try:
                            rproxy = chooseRandomProxy()
                            proxies = {'http': rproxy, 'https': rproxy}

                            print('using proxy %s...'%(rproxy))
                            r = requests.put(url,headers=head,proxies=proxies,timeout=2)
                        except:
                            print('proxy failed, rertying..')
                            return k()

                    k()
                else:
                    print('not using proxy...')
                    r = requests.put(url,headers=head)
                
                
                try:
                    js = str(r.json())
                    if 'Incoming friend requests disabled' in js or 'Unknown User' in js or 'You need to verify your account in order to perform this action.' in js:
                        print(token + '--- Failed to send request')
                        pass
                    else:
                        s.value += 1
                except:
                    s.value += 1

            process = mp.Process(target=m,args=(success,))
            try:
                process.start()
                jobs.append(process)
            except:
                continue

        for job in jobs:
            if job != None:
                job.join()
            
        print('Successfully Made: \'%s\' bots, friend user at id: "%s"'%(success.value,userid))

    elif actionid == '4':

        print('type text channel id')
        channelid = input('---> ')
        
        if len(channelid) != 18:
            print('--- Invalid Text channel ID')
            time.sleep(3)
            return

        print('type the message you want the bots to send')
        msg = input('---> ')

        print('do you want text to speach on? (y/n)')
        tts = input('---> ').lower()

        if tts not in ['y','n']:
            print('--- Invalid Input')
            time.sleep(3)
            return
        
        if tts == 'y':
            tts = 'true'

        else:
            tts = 'false'


        print('Insructing \'%s\' Bots to send message "%s" in text channel \'%s\' with text to speach as \'%s\''%(len(tokens),msg,channelid,tts))
        
        rproxy = chooseRandomProxy()
        proxies = {'http': rproxy, 'https': rproxy}

        if useproxy:
            print('using proxy %s...'%(rproxy))
        else:
            print('not using proxy...')
        success = 0
        for token in tokens:
            head = {"authorization":token,'content-type':'application/json'}
            content = {"content":msg,'tts':tts}
            url = 'https://discordapp.com/api/v6/channels/%s/messages'%(channelid)
            if useproxy:
                try:
                    r = requests.post(url,data=json.dumps(content),headers=head,proxies=proxies,timeout=2)
                except:
                    print('proxy broken. retrying, last retry..')
                    rproxy = chooseRandomProxy()
                    proxies = {'http': rproxy, 'https': rproxy}
                    r = requests.post(url,data=json.dumps(content),headers=head,proxies=proxies,timeout=2)
            else:
                r = requests.post(url,data=json.dumps(content),headers=head)

            
            try:
                js = str(r.json())

                if 'Missing Permissions' in js:
                    pass
                else:
                    success += 1
            except:
                success += 1
        

        print('\nSuccessfully Made: \'%s\' say "%s" in text channel \'%s\' with text to speach as \'%s\''%(success,msg,channelid,tts))
   
    elif actionid == '5':
        print('--- work in progress')
        return False
    
    elif actionid == '6':
        print('-- work in progress')
        return False

    elif actionid == '99':
        print('\n\n[Thanks for using Ringmaster]\n\nexiting..')
        exit()
    
    else:
        return 'FalseAns'



def main():
    global tokens, a_proxy, cant, useproxy
    if useproxy == 'DISBALED':
        cant = 1
        useproxy == False
    if cant == 1:
        pt ='Proxy is  DISABLED as a result of network error'
    elif useproxy:
        pt = '[x] to toggle proxy use. (use proxies to bypass bans)  ------ [ENABLED]'
    else:
        pt =  '[x] to toggle proxy use. (use proxies to bypass bans)  ------ [DISABLED]'
    clear()
    print("""

        _____  _                                 _            
        |  __ \(_)                               | |           
        | |__) |_ _ __   __ _ _ __ ___   __ _ ___| |_ ___ _ __ 
        |  _  /| | '_ \ / _` | '_ ` _ \ / _` / __| __/ _ \ '__|
        | | \ \| | | | | (_| | | | | | | (_| \__ \ ||  __/ |   
        |_|  \_\_|_| |_|\__, |_| |_| |_|\__,_|___/\__\___|_|   
                        __/ |                                 
                        |___/                                  
                                                                                            
        By: TyperOfCode (Aka Discorpion)

        * Info:

            This python program is a discord spam user application, you must supply your own user tokens in tokens.txt.
            The program works on requests through proxies, The speed of the attack depends on your wifi speed.
            Im not responsible for anything you do with this.

        * Start:

            Choose any of the options below to start an attack choose an option by typing the number alongside it.

            [1] Join Guild

            [2] Leave Guild

            [3] Friend User

            [4] Message Guild Channel

            [5] DM User

            [6] Annoying Chat in guild channel

            {proxystats}
            
            [99] Exit
    """.format(proxystats=pt))
    valid = ['1','2','3','4','5','6','x','99']
    answer = input('Number -->')
    if answer == 'x':
        if useproxy:
            useproxy = False
        else:
            useproxy  = True
        main()
    if answer not in valid:
        print('Please type one of the numbers shown above...')
        time.sleep(2)
        main()
    
    action(answer,tokens)
        
    time.sleep(3)
    main()

cant = 0
init()
        
    






