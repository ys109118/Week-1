import hashlib
import time
from datetime import datetime

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def display(self):
        """Display block information in a formatted way"""
        print(f"{'='*60}")
        print(f"BLOCK {self.index}")
        print(f"{'='*60}")
        print(f"Index:        {self.index}")
        print(f"Timestamp:    {datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data:         {self.data}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Hash:         {self.hash}")
        print(f"Nonce:        {self.nonce}")
        print()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        return Block(0, "Genesis Block", "0")
    
    def get_latest_block(self):
        """Get the last block in the chain"""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the chain"""
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), data, previous_block.hash)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False, f"Block {i} has invalid hash"
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False, f"Block {i} has invalid previous hash"
        
        return True, "Blockchain is valid"
    
    def display_chain(self):
        """Display all blocks in the chain"""
        print(f"\n{'#'*70}")
        print(f"{'BLOCKCHAIN DISPLAY':^70}")
        print(f"{'#'*70}")
        
        for block in self.chain:
            block.display()
        
        # Check validity
        is_valid, message = self.is_chain_valid()
        print(f"{'='*60}")
        print(f"BLOCKCHAIN STATUS: {message}")
        print(f"{'='*60}\n")

def demonstrate_blockchain():
    """Main demonstration function"""
    print("🔗 BLOCKCHAIN SIMULATION DEMO")
    print("=" * 50)
    
    # Create blockchain
    blockchain = Blockchain()
    
    # Add two more blocks
    blockchain.add_block("Alice sends 10 coins to Bob")
    blockchain.add_block("Bob sends 5 coins to Charlie")
    
    print("\n1. ORIGINAL BLOCKCHAIN (3 blocks):")
    blockchain.display_chain()
    
    # Demonstrate tampering
    print("\n2. TAMPERING WITH BLOCK 1:")
    print("Changing data in Block 1 from 'Alice sends 10 coins to Bob' to 'Alice sends 100 coins to Bob'")
    print("-" * 70)
    
    # Tamper with block 1
    original_data = blockchain.chain[1].data
    blockchain.chain[1].data = "Alice sends 100 coins to Bob"
    
    print(f"Original data: {original_data}")
    print(f"New data:      {blockchain.chain[1].data}")
    print()
    
    print("3. BLOCKCHAIN AFTER TAMPERING (without recalculating hashes):")
    blockchain.display_chain()
    
    print("\n4. FIXING THE TAMPERED BLOCK:")
    print("Recalculating hash for Block 1...")
    blockchain.chain[1].hash = blockchain.chain[1].calculate_hash()
    print(f"New hash for Block 1: {blockchain.chain[1].hash}")
    
    print("\n5. BLOCKCHAIN AFTER FIXING BLOCK 1 (but not subsequent blocks):")
    blockchain.display_chain()
    
    print("\n6. FIXING ALL SUBSEQUENT BLOCKS:")
    print("Recalculating hashes for all blocks following the tampered block...")
    
    # Fix all subsequent blocks
    for i in range(2, len(blockchain.chain)):
        blockchain.chain[i].previous_hash = blockchain.chain[i-1].hash
        blockchain.chain[i].hash = blockchain.chain[i].calculate_hash()
        print(f"Fixed Block {i}")
    
    print("\n7. FINAL BLOCKCHAIN (all blocks fixed):")
    blockchain.display_chain()
    
    print("\n🎯 KEY OBSERVATIONS:")
    print("-" * 50)
    print("• Changing data in one block breaks the chain")
    print("• Each block's hash depends on its content")
    print("• Each block references the previous block's hash")
    print("• Tampering requires recalculating ALL subsequent blocks")
    print("• This makes blockchain tamper-evident and secure")

def interactive_demo():
    """Interactive version where user can tamper with blocks"""
    blockchain = Blockchain()
    blockchain.add_block("Transaction 1: Alice -> Bob (10 coins)")
    blockchain.add_block("Transaction 2: Bob -> Charlie (5 coins)")
    
    while True:
        print("\n" + "="*50)
        print("INTERACTIVE BLOCKCHAIN DEMO")
        print("="*50)
        print("1. Display blockchain")
        print("2. Add new block")
        print("3. Tamper with block data")
        print("4. Check blockchain validity")
        print("5. Fix blockchain")
        print("6. Exit")
        
        choice = input("\nChoose an option (1-6): ").strip()
        
        if choice == "1":
            blockchain.display_chain()
        
        elif choice == "2":
            data = input("Enter transaction data: ")
            blockchain.add_block(data)
            print(f"Block added with data: {data}")
        
        elif choice == "3":
            try:
                block_index = int(input(f"Enter block index to tamper (0-{len(blockchain.chain)-1}): "))
                if 0 <= block_index < len(blockchain.chain):
                    new_data = input("Enter new data: ")
                    old_data = blockchain.chain[block_index].data
                    blockchain.chain[block_index].data = new_data
                    print(f"Changed data in Block {block_index}")
                    print(f"Old: {old_data}")
                    print(f"New: {new_data}")
                else:
                    print("Invalid block index!")
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "4":
            is_valid, message = blockchain.is_chain_valid()
            print(f"Validation result: {message}")
        
        elif choice == "5":
            print("Fixing blockchain by recalculating all hashes...")
            for i in range(len(blockchain.chain)):
                if i == 0:
                    blockchain.chain[i].hash = blockchain.chain[i].calculate_hash()
                else:
                    blockchain.chain[i].previous_hash = blockchain.chain[i-1].hash
                    blockchain.chain[i].hash = blockchain.chain[i].calculate_hash()
            print("Blockchain fixed!")
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please select 1-6.")

if __name__ == "__main__":
    # Run the main demonstration
    demonstrate_blockchain()
    
    # Ask if user wants interactive mode
    print("\n" + "="*50)
    interactive = input("Would you like to try the interactive demo? (y/n): ").lower().strip()
    if interactive in ['y', 'yes']:
        interactive_demo()