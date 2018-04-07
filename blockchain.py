from flask import Flask
from flask import request
from flask import json
import requests
import json
import hashlib as hasher
import datetime as date
app = Flask(__name__)

# Define what a block is
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

# Generate genesis block
def create_genesis_block():
# Manually construct a block with
# index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), {"from": "none", "to": "none", "amount": 0}, "0")

# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())

peer_nodes = ["http://192.168.0.12:5000"]


@app.route('/')
def hello_world():
    return 'Welcome to the world of Blockchain, Miroslav!'


@app.route('/txion', methods=['POST'])
def transaction():
    # On each new POST request,
    # we extract the transaction data
    new_txion = request.get_json()

    from_who = new_txion.get('from')
    to_who = new_txion.get('to')
    amount = new_txion.get('amount')
    # my code to create block from new txion
    last_block = blockchain[len(blockchain) - 1]

    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    new_block_data = {
    	"from": 	from_who, 
    	"to": 		to_who, 
    	"amount": 	amount
    }

    new_txion_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    blockchain.append(new_txion_block)

    # Then we add the transaction to our list
    # this_nodes_transactions.append(new_txion)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print ("New transaction")
    print ("FROM: {}".format(new_txion['from']))
    print ("TO: {}".format(new_txion['to']))
    print ("AMOUNT: {}\n".format(new_txion['amount']))
    # Then we let the client know it worked out
    return "Transaction submission successful\n"


@app.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain
    blocklist = ""
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        assembled = json.dumps({
        "index": block_index,
        "timestamp": block_timestamp,
        "data": block_data,
        "hash": block_hash
        })
        if blocklist == "":
            blocklist = assembled
        else:
            blocklist += assembled
    return blocklist


@app.route('/chains', methods=['GET'])
def find_new_chains():
    # Get the blockchains of every
    # other node
    other_chains = []
    for node_url in peer_nodes:
        # Get their chains using a GET request
        block = requests.get(node_url + "/blocks").content
        # Convert the JSON object to a Python dictionary
        block = json.loads(block)
        # Add it to our list
        other_chains.append(block)
    return 'Received other nodes blockchain'


@app.route('/myblock', methods=['GET'])
def my_block():

    for i in range(len(blockchain)):
        print("index:", blockchain[i].index)
        print("timestamp:", blockchain[i].timestamp)
        print("data:", blockchain[i].data)
        print("hash:", blockchain[i].hash, "\n")
        
    return 'This is my blockchain'

