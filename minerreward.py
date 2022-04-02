import json
import os
import hashlib
import datetime
def send_reward(address,total):
  reward=total*0.001
  mr=open("mining.json","r+")
  j=json.load(mr)
  hash=hashlib.sha256(str(j).encode('utf-8')).hexdigest()
  signhash=hashlib.sha256(str("Reward From Official CapCoin Server").encode('utf-8')).hexdigest()
  ts={"HASH":hash,"txdata":{"TIME":str(datetime.datetime.now()),"FROM":"MINER REWARDS","TO":address,"AMOUNT":reward,"Signing":signhash}}
  j["MINING REWARDS"].append(ts)
  mr.close()
  os.unlink("mining.json")
  t=open("mining.json","a")
  t.close()
  mr=open("mining.json","r+")
  json.dump(j,mr,indent=1)
  mr.close()