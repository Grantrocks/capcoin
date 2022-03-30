import hashlib
import datetime
import random
import json
import checkaddress
def faucet(rs):
  total=0
  walletdata=checkaddress.check(rs)
  recover=walletdata[0]
  address=walletdata[1]
  pubkey=walletdata[2]
  pvk=walletdata[3]
  qty="1"
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
  to=input("Your Address: ")
  pd=open("pending.json")
  pdj=json.load(pd)
  pd.close()
  pdc=pdj["new"]
  for b in pdc:
    hs=b["txdata"]
    if hs["TO"]==to and hs["FROM"]=="1PJt5vUjLjCZShavTf531vpCAp1zTP7W65":
      exit("You already have a claim pending!")
  tototal=0
  for b in blockc:
    bld=b["data"]
    trx=bld['transactions']
    for w in trx:
      hs=w["txdata"]
      if hs["TO"]==to:
        tototal+=float(hs["AMOUNT"])
      if hs["FROM"]==to:
        tototal-=float(hs["AMOUNT"])
  fee=float(qty)*0.01
  calc=float(qty)+fee
  if float(total)<=float(calc):
    print("Not enough CAP in the facuet!")
  elif float(tototal)>0.0:
    print("You can only withdraw from faucet if you have less than 1 CAP!")
  elif float(total)>float(calc) and float(tototal)==0.0:
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
    ts={"HASH":hash,"txdata":{"Time Sent":str(datetime.datetime.now()),"FROM":address,"TO":"MINER REWARDS","AMOUNT":fee,"Signing":security}}
    pend=open("pending.json","r+")
    cur_data=json.load(pend)
    cur_data["new"].append(ts)
    pend.seek(0)
    json.dump(cur_data,pend,indent=1)
    pend.close()
    print(f"Transaction ID: {hash}")
    print("Transaction sent. Please wait for it to be confirmed!")
faucet("tomato sand noodle recipe slam broken poverty outside come execute copper caught initial live faint bench donate casual glow life empty rally parent fan")