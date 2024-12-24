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
        self.timestamp = time.time()  # Instance variable for unique timestamp
        self.nonce = 0
        self.block_number = block_number
        self.previous_hash = "0" * 64

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
    difficulty = 6 #this mainly decide how much difficult or complex the block would be to mine

    def __init__(self):
        self.chain = []

    def add(self, block):
        self.chain.append({
            'Block Number': block.block_number,
            'Time Stamp': block.timestamp,
            'Nonce': block.nonce,
            'Data': block.data,
            'Previous Hash': block.previous_hash,
            'Current Hash': block.hash()
        })

    def mine(self, block):
        # Update the block's previous_hash to the last block's hash in the chain
        if self.chain:
            block.previous_hash = self.chain[-1]['Current Hash']

        # Proof-of-work: find a nonce that produces the required difficulty
        while True:
            if block.hash()[:self.difficulty] == '0' * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

def main():
    print(f"Start time is {time.time()}")
    my_block_chain = Blockchain()
    datas = ["Transaction1", "Transaction2", "Transaction3", "Transaction4"]

    for num, data in enumerate(datas, start=1):
        block = Block(data, num)
        my_block_chain.mine(block)

    for i, block_dict in enumerate(my_block_chain.chain, start=1):
        # Convert the dictionary back to Block object for readable output
        block = Block(
            data=block_dict['Data'],
            block_number=block_dict['Block Number']
        )
        block.timestamp = block_dict['Time Stamp']
        block.nonce = block_dict['Nonce']
        block.previous_hash = block_dict['Previous Hash']
        print(f"Block {i}:\n{block}")


if __name__ == '__main__':
    main()
