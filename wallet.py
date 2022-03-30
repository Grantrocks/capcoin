import hashlib
import random
import json
import requests
from explorer import search
import time
address=""
returne=input("Have you used the wallet before: ")
if returne=="y":
  total=0
  address=input("Address: ")
  pw=input("Password: ")
  recovery=input("Recovery Code: ")
  tpw=hashlib.sha256(str(pw+address).encode('utf-8')).hexdigest()
  if tpw==recovery:
    f=open("importantwalletinfo.txt","a")
    f.truncate()
    f.write(f"Address: {address}\nPassword: {pw}\nRecovery Code: {recovery}")
    f.close()
    bl=open("blockchain.json")
    blj=json.load(bl)
    bl.close()
    blockc=blj["Blockchain"]
    for b in blockc:
      bld=b["data"]
      trx=bld['transactions']
      for w in trx:
        hs=w["txdata"]
        if hs["TO"]==address:
          total+=float(hs["AMOUNT"])
        if hs["FROM"]==address:
          total-=float(hs["AMOUNT"])
    print("You have CAP "+str(total))
  else:
    print("Incorrect Password!")
    exit()
  while True:
    wtd=input("1=Mine | 2=Send | 3=Check Balance | 4=Explorer")
    if wtd=="2":
      to=input("To: ")
      qty=input("Amount: ")
      fee=float(qty)*0.01
      calc=float(qty)+fee
      if float(total)<=float(calc):
        print("You dont have enough CAP to also cover the fees")
      elif float(total)>float(calc):
        data={"FROM":str(address),"TO":str(to),"AMOUNT":str(qty)}
        hash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        ts={"HASH":hash,"txdata":{"FROM":address,"TO":to,"AMOUNT":qty}}
        pend=open("pending.json","r+")
        cur_data=json.load(pend)
        cur_data["new"].append(ts)
        pend.seek(0)
        json.dump(cur_data,pend,indent=4)
        pend.close()
        security={
          "WalletHash":recovery,
          "WalletPassword":pw,
          "WalletAddress":address,
          "SignedByAddress":"True"
        }
        signhash=hashlib.sha256(str(security).encode('utf-8')).hexdigest()
        data={"FROM":str(address),"TO":"MINER REWARDS","AMOUNT":str(fee)}
        hash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        ts={"HASH":hash,"txdata":{"FROM":address,"TO":"MINER REWARDS","AMOUNT":fee,"Signing":signhash}}
        pend=open("pending.json","r+")
        cur_data=json.load(pend)
        cur_data["new"].append(ts)
        pend.seek(0)
        json.dump(cur_data,pend,indent=4)
        pend.close()
        print(f"Transaction ID: {hash}")
        print("Transaction sent. Please wait for it to be confirmed!")
    elif wtd=="3":
      total=0
      bl=open("blockchain.json")
      blj=json.load(bl)
      bl.close()
      blockc=blj["Blockchain"]
      for b in blockc:
        bld=b["data"]
        trx=bld['transactions']
        for w in trx:
          hs=w["txdata"]
          if hs["TO"]==address:
            total+=float(hs["AMOUNT"])
          if hs["FROM"]==address:
            total-=float(hs["AMOUNT"])
      print("You have CAP "+str(total))
    elif wtd=='1':
      htm=input("How many hashes to mine: ")
      for i in range(int(htm)):
        url="https://capcoin.grantrocks.repl.co/mine_block?address="+str(address)
        re=requests.get(url)
        print(re.json())
        time.sleep(5)
    elif wtd=="4":
      search()
else:
  pw=input("Set A Password: ")
  for i in range(24):
    digit=random.randint(1,10000)
    address+=str(digit)
  print(f"Your address is: {address}")
  recover=hashlib.sha256(str(pw+address).encode('utf-8')).hexdigest()
  print("You recovery code is: "+str(recover))
  print("DO NOT LOSE WALLET INFO FUNDS WILL BE UNRECOVERABLE!!!!!!!")
  f=open("importantwalletinfo.txt","a")
  f.write(f"Address: {address}\nPassword: {pw}\nRecovery Code: {recover}")
  f.close()
  total=0
  bl=open("blockchain.json")
  blj=json.load(bl)
  bl.close()
  blockc=blj["Blockchain"]
  for b in blockc:
    bld=b["data"]
    trx=bld['transactions']
    for w in trx:
      hs=w["txdata"]
      if hs["TO"]==address:
        total+=float(hs["AMOUNT"])
      if hs["FROM"]==address:
        total-=float(hs["AMOUNT"])
  while True:
    wtd=input("1=Mine | 2=Send | 3=Check Balance | 4=Explorer")
    if wtd=="2":
      to=input("To: ")
      qty=input("Amount: ")
      fee=float(qty)*0.01
      calc=float(qty)+fee
      if float(total)<=float(calc):
        print("You dont have enough CAP to also cover the fees")
      elif float(total)>float(calc):
        security={
          "WalletHash":recovery,
          "WalletPassword":pw,
          "WalletAddress":address,
          "SignedByAddress":"True"
        }
        signhash=hashlib.sha256(str(security).encode('utf-8')).hexdigest()
        data={"FROM":str(address),"TO":"MINER REWARDS","AMOUNT":str(fee)}
        hash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        ts={"HASH":hash,"txdata":{"FROM":address,"TO":"MINER REWARDS","AMOUNT":fee,"Signing":signhash}}
        pend=open("pending.json","r+")
        cur_data=json.load(pend)
        cur_data["new"].append(ts)
        pend.seek(0)
        json.dump(cur_data,pend,indent=4)
        pend.close()
        data={"FROM":str(address),"TO":"MINER REWARDS","AMOUNT":str(fee)}
        hash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        ts={"HASH":hash,"txdata":{"FROM":address,"TO":"MINER REWARDS","AMOUNT":fee}}
        pend=open("pending.json","r+")
        cur_data=json.load(pend)
        cur_data["new"].append(ts)
        pend.seek(0)
        json.dump(cur_data,pend,indent=4)
        pend.close()
        print(f"Transaction ID: {hash}")
        print("Transaction sent. Please wait for it to be confirmed!")
    elif wtd=="3":
      total=0
      bl=open("blockchain.json")
      blj=json.load(bl)
      bl.close()
      blockc=blj["Blockchain"]
      for b in blockc:
        bld=b["data"]
        trx=bld['transactions']
        for w in trx:
          hs=w["txdata"]
          if hs["TO"]==address:
            total+=float(hs["AMOUNT"])
          if hs["FROM"]==address:
            total-=float(hs["AMOUNT"])
      print("You have CAP "+str(total))
    elif wtd=='1':
      htm=input("How many hashes to mine: ")
      for i in range(int(htm)):
        url="https://grantrocks.pythonanywhere.com/mine_block?address="+str(address)
        re=requests.get(url)
        data=re.json()
        print(data["msg"])
        time.sleep(5)
    elif wtd=="4":
      search()