from hashlib import sha256
import time

def updateHash(*args):
    to_be_hashed = ""
    hashfunc = sha256()
    for arg in args:
        to_be_hashed += str(arg)
    hashfunc.update(to_be_hashed.encode('utf-8'))

    return hashfunc.hexdigest()

class Block:
    def __init__(self, data, block_number=0):
        self.data = data
        self.timestamp = time.time()
        self.nonce = 0
        self.block_number = block_number
        self.previous_hash = "0" * 64
        
    def return_time_of_block(self):
        return (self.timestamp)
    
    def hash(self):
        return updateHash(self.block_number, self.timestamp, self.nonce, self.data, self.previous_hash)

    def __str__(self):
        return (
            f"Block Number: {self.block_number}\n"
            f"Time Stamp: {self.timestamp}\n"
            f"Nonce: {self.nonce}\n"
            f"Data: {self.data}\n"
            f"Previous Hash: {self.previous_hash}\n"
            f"Current Hash: {self.hash()}\n"
        )

class Blockchain:
    difficulty = 5

    def __init__(self):
        self.chain = []

    def add(self, block):
        self.chain.append(block)

    def mine(self, block):
        # Update the block's previous_hash to the last block's hash in the chain
        if self.chain:
            block.previous_hash = self.chain[-1].hash()

        # Proof-of-work: find a nonce that produces the required difficulty
        while True:
            if block.hash()[:self.difficulty] == '0' * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

    def isValid(self):
        for hash in range(1,len(self.chain)):
            previous = self.chain[hash].previous_hash
            current = self.chain[hash-1].hash()

            if previous != current or current[:self.difficulty] != '0' * self.difficulty:
                return False
                    
        return True            

def main():
    a = time.time()
    print(f"Start time is {a}")

    my_block_chain = Blockchain()
    datas = ["Transaction1", "Transaction2", "Transaction3", "Transaction4"]
    times = []
    for num, data in enumerate(datas, start=1):
        block = Block(data, num)
        my_block_chain.mine(block)
        times.append(block.return_time_of_block())

    #my_block_chain.chain[1].data = 'Transaction2'  #toggle the data field to see the change in verfication

    for i in my_block_chain.chain:
        print(i)    
        
    x = 0 
    print("Total time taken after each block is mined:  ")
    for i in times :
        x = i-a + x
        print(x)

    print(f"\nThe validity of the BlockChain : {my_block_chain.isValid()}\n")

if __name__ == '__main__':
    main()
