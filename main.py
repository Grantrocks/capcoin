import datetime
import json
import hashlib
from flask import Flask, jsonify, request, render_template
from minerreward import send_reward
import checkaddress
import random
import webapi
pay=158
class Blockchain:
   def __init__(self):
       with open("blockchain.json") as prvdata:
         prev=json.load(prvdata)
         bpd=prev['Blockchain']
         prevt=bpd[-1]
         prevtd=prevt['data']
       self.chain = bpd
       self.create_blockchain(proof=prevtd['proof'], previous_hash=prevtd['previous_hash'],txs=[prevtd['transactions']])
   def create_blockchain(self, proof, previous_hash,txs):
       block = {
           'index': len(self.chain),
           'timestamp': str(datetime.datetime.now()),
           'proof': proof,
           'previous_hash': previous_hash,
           'transactions':txs
       }

       self.chain.append(block)
       return block

   def get_previous_block(self):
       last_block = self.chain[-1]
       return last_block

   def proof_of_work(self, previous_proof):
       # miners proof submitted
       new_proof = 1
       # status of proof of work
       check_proof = False
       while check_proof is False:
           # problem and algorithm based off the previous proof and new proof
           hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
           # check miners solution to problem, by using miners proof in cryptographic encryption
           # if miners proof results in 4 leading zero's in the hash operation, then:
           if hash_operation[:4] == '0000':
               check_proof = True
           else:
               # if miners solution is wrong, give mine another chance until correct
               new_proof += 1
       return new_proof

   # generate a hash of an entire block
   def hash(self, block):
       encoded_block = json.dumps(block, sort_keys=True).encode()
       return hashlib.sha256(encoded_block).hexdigest()

   # check if the blockchain is valid
   def is_chain_valid(self, chain):
       # get the first block in the chain and it serves as the previous block
       previous_block = chain[0]
       # an index of the blocks in the chain for iteration
       block_index = 1
       while block_index < len(chain):
           # get the current block
           block = chain[block_index]
           # check if the current block link to previous block has is the same as the hash of the previous block
           if block["previous_hash"] != self.hash(previous_block):
               return False

           # get the previous proof from the previous block
           previous_proof = previous_block['proof']

           # get the current proof from the current block
           current_proof = block['proof']

           # run the proof data through the algorithm
           hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
           # check if hash operation is invalid
           if hash_operation[:4] != '0000':
               return False
           # set the previous block to the current block after running validation on current block
           previous_block = block
           block_index += 1
       return True


app = Flask(__name__)

blockchain = Blockchain()

@app.route('/', methods=['GET'])
def homepage():
  return render_template("index.html"),200
@app.route('/blog', methods=['GET'])
def blog():
  return render_template('blog.html'),200
@app.route('/article', methods=['GET'])
def article():
  return render_template('article.html'),200
@app.route('/blog/get', methods=['GET'])
def blogget():
  aname=request.args.get('aname')
  blog_file=open("blog.json")
  blog_json=json.load(blog_file)
  blog_posts=blog_json['posts']
  for post in blog_posts:
    article_file=post['Article']
    if str(article_file)==str(aname):
      response={"Article":post['Article'],"Date":post["Date"],"Content":post["Content"],"Author":post['Author'],"Donate":post['Donate']}
      break
    else:
      response={"Article":"404 Article Not Found","Date":"","Content":"It seems the article you are looking for does not exist"}
  return jsonify(response),200
@app.route('/blog/posts', methods=['GET'])
def blogposts():
  b=open("blog.json")
  data=json.load(b)
  posts=data['posts']
  b.close()
  return jsonify(posts),200
@app.route('/blog/post', methods=['GET'])
def blogpost():
  articlename=request.args.get('articlename')
  articledate=request.args.get('articledate')
  articlecontent=request.args.get('articlecontent')
  articledonate=request.args.get('donate')
  articleauthor=request.args.get('author')
  webapi.blogpost(articlename,articledate,articlecontent,articleauthor,articledonate)
  return f"Published {articlename}",200
@app.route('/wallet', methods=['GET'])
def wallet():
  return render_template("wallet.html"),200
@app.route('/wallet/generate', methods=['GET'])
def generateweb():
  words=checkaddress.generate()
  return words,200
@app.route('/wallet/sendcap', methods=['GET'])
def sendcap():
  to=request.args.get('to')
  privks=request.args.get('priv')
  amount=request.args.get('amount')
  webtx=webapi.sendcap(to,amount,privks)
  return webtx
@app.route('/wallet/faucetclaim', methods=['GET'])
def faucetcl():
  status=webapi.faucetclaim(request.args.get('address'))
  return status
@app.route('/wallet/import', methods=['GET'])
def walletimport():
  words=checkaddress.check(request.args.get('seed'))
  address=words[1]
  pub=words[2]
  priv=words[3]
  json_import={"address":address,"pub":pub,"priv":priv}
  return jsonify(json_import),200
@app.route('/wallet/getbalance', methods=['GET'])
def gb():
  addr=request.args.get('address')
  bal=webapi.balance(addr)
  raw=bal
  return raw,200
@app.route('/explore', methods=['GET'])
def explore():
  data=open("blockchain.json")
  jdata=json.load(data)
  data.close()
  return jsonify(jdata['Blockchain']),200
@app.route('/mine', methods=['GET'])
def mine_block():
   address=request.args.get('address')
   if address=="":
     address="MINER REWARDS"
   # get the data we need to create a block
   previous_block = blockchain.get_previous_block()
   previous_proof = previous_block['proof']
   proof = blockchain.proof_of_work(previous_proof)
   previous_hash = blockchain.hash(previous_block)
   #try:
   f=open("pending.json","r+")
   mr=open("mining.json","r+")
   mrd=json.load(mr)
   mrrewards=mrd["MINING REWARDS"]
   pending=json.load(f)
   transactions=pending["new"]
   mr.close()
   urpay=random.randint(0,600)
   if len(transactions)>0:
     checked=0
     for m in transactions:
       td=m['txdata']
       dec=td["Signing"]
       pub=dec["Public Key"]
       addr=dec["Address"]
       cp=checkaddress.miner_check(pub)
       if cp==addr:
         pass
       else:
         transactions.remove(m)
       checked+=1
     block = blockchain.create_blockchain(proof, previous_hash,transactions)
     response = {"index":block['index'],"data":{"confirmed": "True","timestamp": block["timestamp"],"proof": block["proof"],"previous_hash": block["previous_hash"],"transactions": block["transactions"]}}
     r=response['data']
     tr=r['transactions']
     txtotal=0
     for t in tr:
       td=t['txdata']
       capt=td['AMOUNT']
       txtotal+=float(capt)
     rst={"new":[]}
     f.truncate(0)
     f.close()
     send_reward(address,txtotal)
     f=open("pending.json","r+")
     json.dump(rst,f,indent=1)
     f.close()
     f=open("blockchain.json","r+")
     file_data=json.load(f)
     new_data = response
     current_index=file_data['Blockchain'][-1]['index']
     print(current_index)
     file_data["Blockchain"].append(new_data)
     f.seek(0)
     json.dump(file_data, f, indent=1)
     f.close()
     return {"rewarded":False,"msg":f"Your Reward: {txtotal*0.001}","minerpayouts":{"YourNumber":urpay,"PoolNumber":pay}}, 200
   elif len(mrrewards)>0 and pay==urpay:
     block_reward=10
     total_reward=0.0+block_reward
     miner_addresses=[]
     confirm_address=[]
     for w in mrrewards:
       am=w['txdata']
       amoun=am['AMOUNT']
       total_reward+=float(amoun)
       miner_addresses+=[am["TO"]]
     for adr in range(len(mrrewards)):
       for m in mrrewards:
         d=m['txdata']
         addr=d['TO']
         if addr in miner_addresses:
           shares=miner_addresses.count(addr)
           data=[addr,shares]
           for i in miner_addresses:
             if addr==i:
               miner_addresses.remove(addr)
           confirm_address+=[data]
         else:
           pass
     share_reward='{"rewards":[]}'
     share_j_parse=json.loads(share_reward)
     total_shares=0
     for i in confirm_address:
       user_share=i[1]
       total_shares+=user_share
     for i in confirm_address:
       user_share=total_shares-i[1]
       svalue=total_reward/float(user_share)
       share_rhash=hashlib.sha256(str("Reward From Official CapCoin Mining Pool").encode("utf-8")).hexdigest()
       share_rjson={"HASH":share_rhash,"txdata":{"TIME":str(datetime.datetime.now()),"FROM":"MINER REWARDS","TO":i[0],"AMOUNT":svalue,"Signing":share_rhash}}
       share_j_parse['rewards'].append(share_rjson)
     block = blockchain.create_blockchain(proof, previous_hash,share_j_parse)
     response = {"index":block['index'],"data":{"confirmed": "True","timestamp": block["timestamp"],"proof": block["proof"],"previous_hash": block["previous_hash"],"transactions": block["transactions"]}}
     mr=open("mining.json","r+")
     mr.truncate(0)
     mr.close()
     mr=open("mining.json","r+")
     rst={"MINING REWARDS":[]}
     json.dump(rst,mr,indent=1)
     mr.close()
     f=open("blockchain.json","r+")
     file_data=json.load(f)
     new_data = response
     file_data["Blockchain"].append(new_data)
     f.seek(0)
     json.dump(file_data, f, indent=1)
     f.close()
     return {"rewarded":True,"msg":"You guessed the right number check your balance to see how much cap you have now.","minerpayouts":{"YourNumber":urpay,"PoolNumber":pay}}, 200
   else:
     return {"rewarded":False,"msg":"There are no transactions to confirm at this time!","minerpayouts":{"YourNumber":urpay,"PoolNumber":pay}}, 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
   response = {'chain': blockchain.chain,
               'length': len(blockchain.chain)}
   return jsonify(response), 200
@app.route('/pending',methods=['GET'])
def pending():
  f=open("pending.json")
  f.close()
  response=json.load(f)
  return jsonify(response),200
@app.route('/mining',methods=['GET'])
def mining():
  f=open("mining.json")
  f.close()
  response=json.load(f)
  return jsonify(response),200
@app.route('/blockchain',methods=['GET'])
def bchain():
  f=open("blockchain.json")
  data=json.load(f)
  f.close()
  response=data
  return jsonify(response),200