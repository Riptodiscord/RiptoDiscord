from traceback import format_exc
import requests, random, json, time, os, secrets, threading,subprocess, sys
from colorama import Fore


mail_type = "OUTLOOK"
kopeechka_apikey = ""
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
xsup = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkzLjAuNDU3Ny42MyBTYWZhcmkvNTM3LjM2IEVkZy85My4wLjk2MS40NyIsImJyb3dzZXJfdmVyc2lvbiI6IjkzLjAuNDU3Ny42MyIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiaHR0cHM6Ly9kaXNjb3JkLmNvbS9jaGFubmVscy81NTQxMjU3Nzc4MTg2MTU4NDQvODcwODgxOTEyMzQyODUxNTk1IiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk3NTA3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
os.system("cls")

count = 0

captcha_count = 0

verified = 0
retry = 0

proxylist = []
captcha_token = []

def selectproxy():
    with open("proxy.txt", 'r+') as f:

        result = secrets.choice(f.readlines())

    return result


def solv():
    global count,retry
    while True:
        try:
            
            url = "http://127.0.0.1:8080/solve?site_key=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34&host=discord.com/login&proxy=0.0.0.0:80"

            r = requests.get(url)
            
            if len(r.text) < 10:
                print("Bad resposne")
            else:
                count+=1
                captcha_token.append(r.text)
        except:
            retry+=1
            pass

def solver():
    global retry
    try:
        global captcha_count
        captcha_count += 1
        return captcha_token[captcha_count]
    except:
        retry+=1
        pass

def verif_mail(link, token):
    global retry
    proxy = selectproxy()

    proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy,
    }

    upn = link.replace('https://click.discord.com/ls/click?upn=', "")

    path = link.replace('https://click.discord.com/', '')

    headers = {

        "authority": "click.discord.com",
        "method": "GET",
        "path": f"{path}",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "__stripe_mid=954ac7da-b7ac-42ff-85d1-2258e79c2aac371992; _ga=GA1.2.1545728695.1660153056; OptanonConsent=isIABGlobal=false&datestamp=Thu+Aug+11+2022+16%3A00%3A17+GMT%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0; __cf_bm=HEwuMYLmp.0ntKPkKIi.Xra9bpbT0HsuMb49kRM.vJc-1661032750-0-Abe6WyT6WMi22p5KTON0igVLj8BSD/VLpRa+v+VDzH0VFoy4AcMP1pBSSKey1pAe3z5ezqYHuxRpdbMfRzB1jz1040C4qHTb6J7Hmp7rOtdta27IpuL7cpzLkd1pYug/IQ==",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": f"{ua}"

    }

    payload = {

        "upn": f"{upn}"

    }

    r = requests.get(link, headers=headers, data=payload, allow_redirects=False)

    temp_link = r.text.replace('<a href="', '')
    verif_link = temp_link.replace('">Found</a>.', '')
    for i in range(5):
        verif_link = verif_link.replace("\n", "")

    verif_header = {

        "authority": "discord.com",
        "method": "POST",
        "path": "/api/v9/auth/verify",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"{token}",
        "content-type": "application/json",
        "cookie": f"__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}; __stripe_mid=954ac7da-b7ac-42ff-85d1-2258e79c2aac371992; _ga=GA1.2.1545728695.1660153056; OptanonConsent=isIABGlobal=false&datestamp=Thu+Aug+11+2022+16%3A00%3A17+GMT%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0",
        "origin": "https://discord.com",
        "referer": "https://discord.com/verify",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": f"{ua}",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "fr",
        "x-super-properties": f"{xsup}"

    }

    spoofed_token = verif_link.replace("https://discord.com/verify#token=", "")

    captcha_solved = solver()

    r = requests.post("https://discord.com/api/v9/auth/verify", headers=verif_header,json={"token": f"{spoofed_token}", "captcha_key": f"{captcha_solved}"}, proxies=proxies)

def get_cookies():

    
    while True:
        try:
            proxies = {
                'http': 'http://' + selectproxy(),
                'https': 'http://' + selectproxy(),
            }
            state = 1
            global __dcfduid
            global __sdcfduid
            response = requests.get('https://discord.com', proxies=proxies)
            for cookie in response.cookies:
                if state == 1:
                    __dcfduid = cookie.value
                else:
                    __sdcfduid = cookie.value
                state += 1
            break
        except:
            pass




def get_mail():
    print("Getting Email")
    while True:
        try:
            r = requests.get(
            f"http://api.kopeechka.store/mailbox-get-email?site=discord.com&mail_type={mail_type}&token={kopeechka_apikey}&soft=$SOFT_ID&investor=$INVESTOR&type=json&api=2.0")
            print(r.content)
            values = json.loads(r.content.decode('utf-8'))
            mail = values['mail']
            id = values['id']
            combo = f"{mail}:{id}"
            print("Mail recovered successfully")
            break
        except:
            pass
    return combo

def get_mail_content(mail_id, token):
    global verified, retry
    step = 0
    r = requests.get(f"http://api.kopeechka.store/mailbox-get-message?full=0&id={mail_id}&token={kopeechka_apikey}&type=json&api=2.0")
    if r.text == '{"status":"ERROR","value":"WAIT_LINK"}':
        print("Retrying to get verification link")
        while r.text == '{"status":"ERROR","value":"WAIT_LINK"}':
            if step!= 12:
                time.sleep(5)
                step+=1
                print("Retrying to get verification link")
                r = requests.get(
                    f"http://api.kopeechka.store/mailbox-get-message?full=0&id={mail_id}&token={kopeechka_apikey}&type=json&api=2.0")
            else:
                retry+=1
                retryfun()

    print("Mail link getted successfully")
    values = json.loads(r.content.decode('utf-8'))
    verif_link = values['value']
    verif_mail(verif_link, token)

    print("Mail changed successfully " + old_mail + " --> " + new_mail)
    verified+=1

    with open("verified.txt", "a+") as v:
        v.write(f"{new_mail}:{password}:{token}\n")

def change(mail,password,token, id):

    
    get_cookies()
    # try:
    proxi = {
        'http': 'http://' + selectproxy(),
        'https': 'http://' + selectproxy(),
    }



    url = "https://discord.com/api/v9/users/@me"


    headers = {

        "authority": "discord.com",
        "method": "PATCH",
        "path": "/api/v9/users/@me",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9",
        "authorization": f"{token}",
        "content-type": "application/json",
        "cookie": f"__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}; __stripe_mid=954ac7da-b7ac-42ff-85d1-2258e79c2aac371992; _ga=GA1.2.1545728695.1660153056; OptanonConsent=isIABGlobal=false&datestamp=Thu+Aug+11+2022+16%3A00%3A17+GMT%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImZyLUZSIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE1MzAxMywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        
        }


    jsondata = {"email":f"{mail}","":"null","password":f"{password}"}

    r = requests.patch(url, headers=headers, json=jsondata, proxies=proxi)
    get_mail_content(id, token)
    # except:
    #     pass
    


def loop():
    os.system(f"title Token Verified: {str(verified)}  // Retry: {str(retry)}  // Captcha solved: {str(count)}")


threads = input("How many threads u want?")

if __name__ == "__main__":
    lp = threading.Thread(target=loop,)
    lp.start()
    for i in range(int(threads)):
        i = threading.Thread(target=solv,)
        i.start()
    time.sleep(50)
    print("Warming up captcha solving ...")
    with open("account.txt", "r", encoding="utf-8") as t:
        
        for lines in t:

            mailid = get_mail()
            new_mail = mailid.split(':')[0]
            id = mailid.split(':')[1]

            old_mail,password,token = lines.split(":", 2)
            token = token.replace(" ", "")
            token = token.replace("\n","")
            change(new_mail,password,token, id)
        exit()

def retryfun():
    mailid = get_mail()
    new_mail = mailid.split(':')[0]
    id = mailid.split(':')[1]
    change(new_mail,password,token, id)