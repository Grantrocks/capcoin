import json
def search():
  with open("blockchain.json") as f:
    file = json.load(f)
    data = file["Blockchain"]
  lookfor=input("Transaction hash to look for: ")
  for i in data:
    da=i['data']
    confirmed=da['confirmed']
    timestamp=da['timestamp']
    blockhash=da['previous_hash']
    d=da['transactions']
    if confirmed=="True":
      confirmed="Confirmed at "+str(timestamp)
    else:
      confirmed="No"
    for t in d:
      if lookfor in t['HASH']:
        tx=t['txdata']
        print(f"TX ID: {lookfor} Confirmed: {confirmed} Blockhash: {blockhash}")
        print(f"CapCoin Amount: {round(float(tx['AMOUNT'])):f} From: {tx['FROM']} Sent To: {tx['TO']}")
      else:
        print("Not Found")