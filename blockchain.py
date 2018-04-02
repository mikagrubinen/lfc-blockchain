from flask import Flask
from flask import request
from flask import json
import requests
import json
app = Flask(__name__)


peer_nodes = ["http://192.168.0.12:5000"]


@app.route('/')
def hello_world():
    return 'Welcome to the world of Blockchain, Miroslav!'


@app.route('/txion', methods=['POST'])
def transaction():
    # On each new POST request,
    # we extract the transaction data
    new_txion = request.get_json()
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
    chain_to_send = {
        "index": "prvi",
        "timestamp": "Prvi_block_timestamp",
        "data": "Prvi_block_data",
        "hash": "Prvi_block_hash"
    }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send


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
    print(other_chains)
    return 'Received other nodes blockchain'


    



