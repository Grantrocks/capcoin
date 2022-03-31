import datetime
import json
import hashlib
from flask import Flask, jsonify, request, render_template
from minerreward import send_reward
import checkaddress
import random
pay=158
class Blockchain:
   def __init__(self):
       self.chain = []
       self.create_blockchain(proof=1, previous_hash='0',txs=[])
   def create_blockchain(self, proof, previous_hash,txs):
       block = {
           'index': len(self.chain) + 1,
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
@app.route('/explore', methods=['GET'])
def explore():
  data=open("blockchain.json")
  jdata=json.load(data)
  data.close()
  print(type(jdata))
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
   urpay=random.randint(0,200)
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
         transactions.pop(checked)
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
     file_data["Blockchain"].append(new_data)
     f.seek(0)
     json.dump(file_data, f, indent=1)
     f.close()
     mined=f"Your Reward: {txtotal*0.01}  Wait for a miner to get the right number so you can get your reward."
     return {"msg":mined,"minerpayouts":{"YourNumber":urpay,"PoolNumber":pay}}, 200
   elif len(mrrewards)>0 and pay==urpay:
     block = blockchain.create_blockchain(proof, previous_hash,mrrewards)
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
     return {"msg":response,"minerpayouts":{"YourNumber":urpay,"PoolNumber":pay}}, 200
   else:
     return {"msg":"There are no transactions to confirm at this time!","minerpayouts":{"YourNumber":urpay,"PoolNumber":pay}}, 200
   #except:
     #return {"msg":"Something went wrong!"},200


@app.route('/get_chain', methods=['GET'])
def get_chain():
   response = {'chain': blockchain.chain,
               'length': len(blockchain.chain)}
   return jsonify(response), 200
@app.route('/pending',methods=['GET'])
def pending():
  f=open("pending.json")
  data=f.read()
  f.close()
  response=json.load(f)
  return jsonify(response),200
@app.route('/mining',methods=['GET'])
def mining():
  f=open("mining.json")
  data=f.read()
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