import hashlib
import datetime
import random
import json
import checkaddress
import bitcoin
def faucetclaim(to):
  rs="unfold air buddy obtain good soup fashion health problem youth angle lecture kitten current draw flock sense tone sausage setup dog because winner bargain"
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
  pd=open("pending.json")
  pdj=json.load(pd)
  pd.close()
  pdc=pdj["new"]
  for b in pdc:
    hs=b["txdata"]
    if hs["TO"]==to and hs["FROM"]=="1PJt5vUjLjCZShavTf531vpCAp1zTP7W65":
      return "You already have a claim pending!"
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
    return "Not enough CAP in the facuet!"
  elif float(tototal)>0.0:
    return "You can only withdraw from faucet if you have less than 1 CAP!"
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
    fhash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
    ts={"HASH":fhash,"txdata":{"Time Sent":str(datetime.datetime.now()),"FROM":address,"TO":"MINER REWARDS","AMOUNT":fee,"Signing":security}}
    pend=open("pending.json","r+")
    cur_data=json.load(pend)
    cur_data["new"].append(ts)
    pend.seek(0)
    json.dump(cur_data,pend,indent=1)
    pend.close()
    return f"Transaction ID: {hash}"
def sendcap(to,qty,priv):
    address=bitcoin.privtoaddr(priv)
    pubkey=bitcoin.privtopub(priv)
    fee=float(qty)*0.01
    calc=float(qty)+fee
    total=0
    pending=0
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
    pend=open("pending.json")
    pendj=json.load(pend)
    pend.close()
    blockc=pendj["new"]
    for b in blockc:
      hs=b["txdata"]
      if hs["FROM"]==address:
        pending+=float(hs["AMOUNT"])
    total-=pending
    if float(total)>float(calc):
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
      fhash=hashlib.sha256(str(data).encode('utf-8')).hexdigest()
      ts={"HASH":fhash,"txdata":{"Time Sent":str(datetime.datetime.now()),"FROM":address,"TO":"MINER REWARDS","AMOUNT":fee,"Signing":security}}
      pend=open("pending.json","r+")
      cur_data=json.load(pend)
      cur_data["new"].append(ts)
      pend.seek(0)
      json.dump(cur_data,pend,indent=1)
      pend.close()
      return f"Transaction ID: {hash}"
    else:
      return "Not enough confimred cap to send transaction"
def balance(address):
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
  pend=open("pending.json")
  pendj=json.load(pend)
  pend.close()
  blockc=pendj["new"]
  for b in blockc:
    hs=b["txdata"]
    if hs["TO"]==address:
      total+=float(hs["AMOUNT"])
    if hs["FROM"]==address:
      total-=float(hs["AMOUNT"])
  return str(total)
def blogpost(articlename,articledate,articlecontent):
  data={"Article":articlename,"Date":articledate,"Content":articlecontent}
  blog_file=open("blog.json","r+")
  blog=json.load(blog_file)
  blog_file.truncate(0)
  blog_file.close()
  blog_file=open('blog.json','r+')
  blog['posts'].append(data)
  json.dump(blog,blog_file,indent=1)
  blog_file.close()