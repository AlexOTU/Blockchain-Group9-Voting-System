# INFR-4900U
# Blockchain
# Group 20 
# Voting System

import datetime, hashlib, json, os, random, string

ROOT_DIR  = os.path.dirname(os.path.abspath(__file__)) # root directory of the script
BLOCK_DIR = f'{ROOT_DIR}\\blocks' # directory of all the blocks in the chain
DIFFICULTY = 3 # difficulty of proof of work (number 0s in hash)

class Block: # defining the Block class
    # initializing the attributes of the block
    def __init__(self,
                id = None,
                timestamp = int(datetime.datetime.now().timestamp()),
                parentID = None,
                content = None,
                PoW = None,
                hash = None):
        self.id = id
        self.timestamp = timestamp
        self.parentID = parentID
        self.content = content
        self.PoW = PoW
        self.hash = hash

    def writeBlockToJSON(self, filename = '0'):
        # place all the block attributes in a dictionary called payload
        payload = {
            'id': self.id,
            'timestamp': self.timestamp,
            'parentID': self.parentID,
            'content': self.content,
            'PoW': self.PoW,
            'hash': self.hash          
        }
        # dumping the attributes into the JSON file (block)
        with open(f'{BLOCK_DIR}\\{filename}.json', 'w', encoding='utf-8') as f: 
            json.dump(payload, f, ensure_ascii=False, indent=4)

    def getParentBlock(self):
        # iterates through all the blocks in the directory, opens the contents and loads it in temp, and compares the temp[id] to the parentID of the block, and return the parentID
        for block in os.listdir(BLOCK_DIR):
            with open(f'{BLOCK_DIR}\\{block}', 'r', encoding='utf-8') as f:
                temp = json.load(f)
                if str(temp['id']) == str(self.parentID):
                    return temp
                
def load(blockchain):
    # if the block directory is empty, call the generateGenesis function and recall the function
    if os.listdir(BLOCK_DIR) == []:
        generateGenesis()
        load(blockchain)
    else:
        # open each block in the directory, load the attributes into a new Block object and append it to the blockchain list
        for block in os.listdir(BLOCK_DIR):
            with open(f'{BLOCK_DIR}\\{block}', 'r', encoding='utf-8') as f:
                content = json.load(f)
                blockchain.append(Block(
                    content['id'],
                    content['timestamp'],
                    content['parentID'],
                    content['content'],
                    content['PoW'],
                    content['hash'],
                    ))
        order(blockchain)
# sort the blocks by timestamp
def order(blockchain):
    return blockchain.sort(key=lambda x: x.timestamp, reverse=True)
# generates the genesis block
def generateGenesis():
    print('Genesis block not detected. Creating Genesis.')
    Block(id="0", timestamp = int(datetime.datetime.now().timestamp()), parentID="0", content=str(input("ENTER POLL QUESTION > ")), PoW=DIFFICULTY, hash="0").writeBlockToJSON()

def generateHash(parent, PoW):
    count = 0
    # read the ID of the latest block
    with open(f'{BLOCK_DIR}\\{parent.id}.json', 'rb') as f:
        while True:
            # hash the ID and 64 random string bytes
            hash = hashlib.pbkdf2_hmac('sha256', str(f.read()).encode(), str(os.urandom(64)).encode(), 1, dklen=128).hex()
            count += 1
            # checking if the number of 0s in the hash is equal to the PoW, then return the hash
            if str('0' * PoW) == str(hash)[0: PoW]:
                print(f'\r{count} Hashes Checked. Difficulty set to {PoW}.\n')
                return hash
