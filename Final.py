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
