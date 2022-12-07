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
#Adding the block that is created to the blockchain
def add(blockchain, block = None):
    blockchain.append(block)
    #Writing the block to JSON to see the information if required
    block.writeBlockToJSON(block.id)
#The Generating Block function
#The proof difficulty is set at the top of the code
def generateBlock(blockchain, proof = DIFFICULTY):
    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
    timestamp = int(datetime.datetime.utcnow().timestamp())
    parentID = blockchain[-1].id
    content = input('Enter your vote > ')
    #Calling generateHash function above
    hash = generateHash(blockchain[-1], proof)
    PoW = proof
    #This sends the details pertaining to the users vote and will add it to the blockchain
    add(blockchain, Block(id, timestamp, parentID, content.lower(), PoW, hash))
#This function will show the current inputted votes
def showTally(blockchain):
    temp = {}
    order(blockchain)
    #Values in the blockchain are called and put into the temp variable
    for i in blockchain:
        if i.content in temp: temp[i.content] += 1
        else: temp[i.content] = 1
    #Putting the values on the screen in the format of (Candidate  | Number of votes)
    print(f'\n\nQuestion: {list(temp.keys())[-1]:10}\n\nPoll Results\n\nAnswer | Votes')
    for i in range(len(temp) - 1):
        print(f'{list(temp.keys())[i]:8} | {list(temp.values())[i]:3}')
    print("\n***\n")
#This section is the interface part of the code or what will show to the user.
if __name__ == '__main__':
    blockchain = []
    load(blockchain)
    inp = True
    while inp:
	#Formmated to show the 3 options of casting a vote, showing total votes/results and exiting
        user_input = input('Please select an operation\n\n[1] Add A New Vote\n[2] Display Current Tally\n[3] Quit\n\n\n> ').lower()
        if user_input == '1':
            generateBlock(blockchain, proof=DIFFICULTY)
        if user_input == '2':
            showTally(blockchain)
        if user_input == '3' or user_input.lower() == 'quit':
            inp = False
    print('Closing blockchain program.')
