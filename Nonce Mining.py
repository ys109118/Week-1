import hashlib
import time
from datetime import datetime
import threading
import sys

class Block:
    def __init__(self, index, data, previous_hash, difficulty=0):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = ""
        self.mining_time = 0
        self.attempts = 0
        
        # If difficulty is set, mine the block
        if difficulty > 0:
            self.mine_block(difficulty)
        else:
            self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine the block using Proof-of-Work"""
        target = "0" * difficulty  # Target pattern (e.g., "0000")
        
        print(f"\n⛏️  MINING BLOCK {self.index}")
        print(f"Target: Hash must start with '{target}'")
        print(f"Difficulty: {difficulty} leading zeros")
        print("-" * 50)
        
        start_time = time.time()
        self.attempts = 0
        
        # Keep incrementing nonce until hash meets difficulty requirement
        while True:
            self.nonce += 1
            self.attempts += 1
            self.hash = self.calculate_hash()
            
            # Print progress every 10000 attempts
            if self.attempts % 10000 == 0:
                print(f"Attempt {self.attempts:,}: nonce={self.nonce}, hash={self.hash[:20]}...")
            
            # Check if hash meets difficulty requirement
            if self.hash.startswith(target):
                self.mining_time = time.time() - start_time
                print(f"\n✅ BLOCK MINED SUCCESSFULLY!")
                print(f"Final hash: {self.hash}")
                print(f"Nonce found: {self.nonce:,}")
                print(f"Total attempts: {self.attempts:,}")
                print(f"Mining time: {self.mining_time:.2f} seconds")
                print(f"Hash rate: {self.attempts/self.mining_time:.0f} hashes/second")
                break
    
    def display(self):
        """Display block information"""
        print(f"{'='*60}")
        print(f"BLOCK {self.index}")
        print(f"{'='*60}")
        print(f"Index:        {self.index}")
        print(f"Timestamp:    {datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data:         {self.data}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Nonce:        {self.nonce:,}")
        print(f"Hash:         {self.hash}")
        if self.difficulty > 0:
            print(f"Difficulty:   {self.difficulty} (target: {'0' * self.difficulty})")
            print(f"Mining Time:  {self.mining_time:.2f} seconds")
            print(f"Attempts:     {self.attempts:,}")
        print()

class MiningBlockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2  # Default difficulty
    
    def create_genesis_block(self, difficulty=0):
        """Create the first block in the chain"""
        genesis = Block(0, "Genesis Block", "0", difficulty)
        self.chain.append(genesis)
        return genesis
    
    def get_latest_block(self):
        """Get the last block in the chain"""
        return self.chain[-1] if self.chain else None
    
    def add_block(self, data, difficulty=None):
        """Add a new block to the chain with mining"""
        if not self.chain:
            # Create genesis block first
            self.create_genesis_block()
        
        previous_block = self.get_latest_block()
        mining_difficulty = difficulty if difficulty is not None else self.difficulty
        
        new_block = Block(len(self.chain), data, previous_block.hash, mining_difficulty)
        self.chain.append(new_block)
        return new_block
    
    def display_chain(self):
        """Display all blocks in the chain"""
        print(f"\n{'#'*70}")
        print(f"{'MINING BLOCKCHAIN DISPLAY':^70}")
        print(f"{'#'*70}")
        
        total_time = 0
        total_attempts = 0
        
        for block in self.chain:
            block.display()
            if block.difficulty > 0:
                total_time += block.mining_time
                total_attempts += block.attempts
        
        if total_attempts > 0:
            print(f"{'='*60}")
            print(f"MINING STATISTICS")
            print(f"{'='*60}")
            print(f"Total mining time: {total_time:.2f} seconds")
            print(f"Total attempts: {total_attempts:,}")
            print(f"Average hash rate: {total_attempts/total_time:.0f} hashes/second")
            print(f"{'='*60}")

def difficulty_comparison():
    """Compare mining times for different difficulty levels"""
    print("🎯 DIFFICULTY COMPARISON DEMO")
    print("=" * 50)
    
    difficulties = [1, 2, 3, 4]  # Don't go too high for demo purposes
    results = []
    
    for diff in difficulties:
        print(f"\n🔍 Testing Difficulty Level: {diff}")
        print(f"Target: Hash must start with {'0' * diff}")
        
        # Create a test block
        test_block = Block(1, f"Test block for difficulty {diff}", "0" * 64, diff)
        
        results.append({
            'difficulty': diff,
            'attempts': test_block.attempts,
            'time': test_block.mining_time,
            'hash_rate': test_block.attempts / test_block.mining_time if test_block.mining_time > 0 else 0
        })
    
    # Display comparison
    print(f"\n{'='*80}")
    print(f"DIFFICULTY COMPARISON RESULTS")
    print(f"{'='*80}")
    print(f"{'Difficulty':<12} {'Attempts':<12} {'Time (s)':<12} {'Hash Rate':<15} {'Multiplier'}")
    print(f"{'-'*80}")
    
    base_attempts = results[0]['attempts']
    for result in results:
        multiplier = result['attempts'] / base_attempts
        print(f"{result['difficulty']:<12} {result['attempts']:<12,} {result['time']:<12.2f} {result['hash_rate']:<15.0f} {multiplier:<.1f}x")

def interactive_mining():
    """Interactive mining simulation"""
    blockchain = MiningBlockchain()
    
    while True:
        print(f"\n{'='*60}")
        print("INTERACTIVE MINING SIMULATION")
        print(f"{'='*60}")
        print("1. Mine a new block")
        print("2. Set difficulty level")
        print("3. Display blockchain")
        print("4. Mine multiple blocks")
        print("5. Quick difficulty comparison")
        print("6. Exit")
        
        choice = input(f"\nCurrent difficulty: {blockchain.difficulty} | Choose option (1-6): ").strip()
        
        if choice == "1":
            data = input("Enter block data: ")
            print(f"\nMining block with difficulty {blockchain.difficulty}...")
            blockchain.add_block(data)
        
        elif choice == "2":
            try:
                new_difficulty = int(input("Enter new difficulty (1-5 recommended): "))
                if 1 <= new_difficulty <= 6:
                    blockchain.difficulty = new_difficulty
                    print(f"Difficulty set to {new_difficulty}")
                else:
                    print("Difficulty should be between 1-6 for reasonable demo times")
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "3":
            blockchain.display_chain()
        
        elif choice == "4":
            try:
                count = int(input("How many blocks to mine? "))
                if count > 0:
                    print(f"\nMining {count} blocks with difficulty {blockchain.difficulty}...")
                    for i in range(count):
                        data = f"Block {len(blockchain.chain)} - Transaction {i+1}"
                        blockchain.add_block(data)
                else:
                    print("Please enter a positive number!")
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "5":
            print("Running quick difficulty comparison (1-3)...")
            quick_comparison()
        
        elif choice == "6":
            print("Happy mining! 🎉")
            break
        
        else:
            print("Invalid choice! Please select 1-6.")

def quick_comparison():
    """Quick comparison of difficulties 1-3"""
    difficulties = [1, 2, 3]
    print(f"\n{'Difficulty':<12} {'Attempts':<12} {'Time (s)':<12}")
    print(f"{'-'*40}")
    
    for diff in difficulties:
        block = Block(1, f"Test block", "0" * 64, diff)
        print(f"{diff:<12} {block.attempts:<12,} {block.mining_time:<12.2f}")

def demonstrate_mining():
    """Main demonstration function"""
    print("⛏️  PROOF-OF-WORK MINING SIMULATION")
    print("=" * 50)
    
    # Create blockchain
    blockchain = MiningBlockchain()
    blockchain.difficulty = 3  # Start with moderate difficulty
    
    print(f"\n1. CREATING GENESIS BLOCK (no mining required)")
    blockchain.create_genesis_block()
    
    print(f"\n2. MINING FIRST TRANSACTION BLOCK")
    blockchain.add_block("Alice sends 10 BTC to Bob")
    
    print(f"\n3. MINING SECOND TRANSACTION BLOCK")
    blockchain.add_block("Bob sends 5 BTC to Charlie")
    
    print(f"\n4. DISPLAYING COMPLETE BLOCKCHAIN")
    blockchain.display_chain()
    
    print(f"\n5. TESTING HIGHER DIFFICULTY")
    print("Mining a block with difficulty 4...")
    blockchain.difficulty = 4
    blockchain.add_block("Charlie sends 2 BTC to Dave")
    
    blockchain.display_chain()

if __name__ == "__main__":
    print("🚀 PROOF-OF-WORK MINING SIMULATOR")
    print("=" * 50)
    print("Choose your experience:")
    print("1. Automatic demonstration")
    print("2. Interactive mining")
    print("3. Difficulty comparison")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        demonstrate_mining()
    elif choice == "2":
        interactive_mining()
    elif choice == "3":
        difficulty_comparison()
    else:
        print("Running automatic demonstration...")
        demonstrate_mining()