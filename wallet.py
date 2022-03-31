import hashlib
import random
import json
import requests
from mnemonic import Mnemonic
import bip32utils
import checkaddress
mnemon = Mnemonic('english')
from explorer import search
import time
def wallet(rs):
    total=0
    walletdata=checkaddress.check(rs)
    recover=walletdata[0]
    address=walletdata[1]
    pubkey=walletdata[2]
    pvk=walletdata[3]
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
    while True:
      print(f"Address: {address}")
      wtd=input("1=Mine | 2=Send | 3=Check Balance | 4=Explorer")
      if wtd=="2":
        to=input("To: ")
        qty=input("Amount: ")
        fee=float(qty)*0.01
        calc=float(qty)+fee
        if float(total)<=float(calc):
          print("You dont have enough CAP to also cover the fees")
        elif float(total)>float(calc):
          security={"Public Key":pubkey,"Address":address}
          data={"FROM":str(address),"TO":to,"AMOUNT":str(qty)}
          hash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
          ts={"HASH":hash,"txdata":{"FROM":address,"TO":to,"AMOUNT":qty,"Signing":security}}
          pend=open("pending.json","r+")
          cur_data=json.load(pend)
          cur_data["new"].append(ts)
          pend.seek(0)
          json.dump(cur_data,pend,indent=1)
          pend.close()
          security={"Public Key":pubkey,"Address":address}
          data={"FROM":str(address),"TO":"MINER REWARDS","AMOUNT":str(fee)}
          hash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
          ts={"HASH":hash,"txdata":{"FROM":address,"TO":"MINER REWARDS","AMOUNT":fee,"Signing":security}}
          pend=open("pending.json","r+")
          cur_data=json.load(pend)
          cur_data["new"].append(ts)
          pend.seek(0)
          json.dump(cur_data,pend,indent=1)
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
          url="https://cryptoandpicoin.herokuapp.com/mine?address="+str(address)
          re=requests.get(url)
          data=re.json()
          try:
            blocki=i['index']
            bdata=i["data"]
            ph=bdata['previous_hash']
            btime=bdata['timestamp']
            print(f"Block Number: {blocki} Block Hash: {ph} Time: {btime}")
          except:
            print(f"Message: {data['msg']} Info: {data['miner payouts']}")
          time.sleep(5)
      elif wtd=="4":
        search()
def init():
  returne=input("Have you used the wallet before: ")
  if returne=="y":
    recoveryu=input("Recovery Seed: ")
    wallet(recoveryu)
  else:
    walletdata=checkaddress.generate()
    recover=walletdata[0]
    print("You recovery seed: "+str(recover))
    print("DO NOT LOSE WALLET INFO FUNDS WILL BE UNRECOVERABLE!!!!!!!")
    f=open("importantwalletinfo.txt","a")
    f.truncate(0)
    f.write(f"Recovery Seed: {recover}\n")
    f.close()
    wallet(recover)
init()