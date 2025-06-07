import random
import time
from datetime import datetime

class Validator:
    """Base validator class for all consensus mechanisms"""
    def __init__(self, name, validator_id):
        self.name = name
        self.validator_id = validator_id
        self.blocks_validated = 0
        self.rewards_earned = 0
    
    def __str__(self):
        return f"Validator {self.name} (ID: {self.validator_id})"

class PoWMiner(Validator):
    """Proof of Work Miner"""
    def __init__(self, name, validator_id, hash_power):
        super().__init__(name, validator_id)
        self.hash_power = hash_power  # Hash rate in MH/s
        self.electricity_cost = random.uniform(0.05, 0.15)  # Cost per hash
    
    def mine_attempt(self):
        """Simulate mining attempt - higher hash power = better chance"""
        # Simulate random mining success based on hash power
        return random.randint(1, 1000) <= self.hash_power
    
    def __str__(self):
        return f"PoW Miner {self.name} (Hash Power: {self.hash_power} MH/s)"

class PoSStaker(Validator):
    """Proof of Stake Staker"""
    def __init__(self, name, validator_id, stake_amount):
        super().__init__(name, validator_id)
        self.stake_amount = stake_amount  # Amount of tokens staked
        self.stake_age = random.randint(1, 365)  # Days staked
        self.slashing_risk = 0.01  # Risk of losing stake for bad behavior
    
    def calculate_stake_weight(self):
        """Calculate effective stake weight (can include age factor)"""
        # Some PoS systems give bonus for longer staking
        age_bonus = min(self.stake_age / 365, 0.5)  # Max 50% bonus
        return self.stake_amount * (1 + age_bonus)
    
    def __str__(self):
        return f"PoS Staker {self.name} (Stake: {self.stake_amount:,} tokens, Age: {self.stake_age} days)"

class DPoSDelegate(Validator):
    """Delegated Proof of Stake Delegate"""
    def __init__(self, name, validator_id, reputation_score):
        super().__init__(name, validator_id)
        self.votes_received = 0
        self.voters = []
        self.reputation_score = reputation_score  # 0-100 reputation
        self.commission_rate = random.uniform(0.01, 0.10)  # 1-10% commission
    
    def receive_vote(self, voter, vote_weight):
        """Receive a vote from a token holder"""
        self.votes_received += vote_weight
        self.voters.append({'voter': voter, 'weight': vote_weight})
    
    def __str__(self):
        return f"DPoS Delegate {self.name} (Votes: {self.votes_received:,}, Reputation: {self.reputation_score}/100)"

class Voter:
    """Token holder who votes in DPoS"""
    def __init__(self, name, token_balance):
        self.name = name
        self.token_balance = token_balance
        self.voted_delegate = None
    
    def vote_for_delegate(self, delegate):
        """Vote for a delegate with full token balance"""
        self.voted_delegate = delegate
        delegate.receive_vote(self, self.token_balance)
    
    def __str__(self):
        return f"Voter {self.name} ({self.token_balance:,} tokens)"

class ConsensusSimulator:
    """Main simulator for different consensus mechanisms"""
    
    def __init__(self):
        self.setup_validators()
        self.simulation_round = 0
    
    def setup_validators(self):
        """Initialize validators for all consensus mechanisms"""
        print("🔧 SETTING UP CONSENSUS SIMULATION")
        print("=" * 60)
        
        # Setup PoW Miners
        self.pow_miners = [
            PoWMiner("MegaMiner Corp", "POW001", random.randint(50, 200)),
            PoWMiner("CryptoPool Ltd", "POW002", random.randint(50, 200)),
            PoWMiner("HashForce Inc", "POW003", random.randint(50, 200)),
            PoWMiner("DigitalMining Co", "POW004", random.randint(50, 200))
        ]
        
        # Setup PoS Stakers
        self.pos_stakers = [
            PoSStaker("Alice", "POS001", random.randint(10000, 50000)),
            PoSStaker("Bob", "POS002", random.randint(10000, 50000)),
            PoSStaker("Charlie", "POS003", random.randint(10000, 50000)),
            PoSStaker("Diana", "POS004", random.randint(10000, 50000))
        ]
        
        # Setup DPoS Delegates
        self.dpos_delegates = [
            DPoSDelegate("TechNode", "DPOS001", random.randint(70, 95)),
            DPoSDelegate("CommunityPool", "DPOS002", random.randint(70, 95)),
            DPoSDelegate("SecureValidator", "DPOS003", random.randint(70, 95)),
            DPoSDelegate("PublicService", "DPOS004", random.randint(70, 95))
        ]
        
        # Setup Voters for DPoS
        self.voters = [
            Voter("TokenHolder1", random.randint(1000, 10000)),
            Voter("TokenHolder2", random.randint(1000, 10000)),
            Voter("TokenHolder3", random.randint(1000, 10000)),
            Voter("TokenHolder4", random.randint(1000, 10000)),
            Voter("TokenHolder5", random.randint(1000, 10000)),
            Voter("Whale", random.randint(50000, 100000))  # Large holder
        ]
        
        # Simulate voting for DPoS
        self.simulate_dpos_voting()
        
        print("✅ Setup complete!\n")
    
    def simulate_dpos_voting(self):
        """Simulate voting process for DPoS"""
        print("🗳️  SIMULATING DPoS VOTING PROCESS")
        print("-" * 40)
        
        for voter in self.voters:
            # Vote for random delegate (could be based on reputation or other factors)
            chosen_delegate = random.choice(self.dpos_delegates)
            voter.vote_for_delegate(chosen_delegate)
            print(f"{voter.name} votes for {chosen_delegate.name} with {voter.token_balance:,} tokens")
        
        print()
    
    def display_validators(self):
        """Display all validators and their stats"""
        print("📊 VALIDATOR INFORMATION")
        print("=" * 60)
        
        print("\n🔨 PROOF OF WORK MINERS:")
        for miner in self.pow_miners:
            print(f"  {miner}")
        
        print("\n🏛️  PROOF OF STAKE STAKERS:")
        for staker in self.pos_stakers:
            effective_stake = staker.calculate_stake_weight()
            print(f"  {staker} (Effective: {effective_stake:,.0f})")
        
        print("\n🏆 DELEGATED PROOF OF STAKE DELEGATES:")
        for delegate in self.dpos_delegates:
            print(f"  {delegate}")
        
        print()
    
    def pow_consensus(self):
        """Simulate Proof of Work consensus"""
        print("⛏️  PROOF OF WORK CONSENSUS SIMULATION")
        print("=" * 50)
        print("Logic: Miners compete to solve cryptographic puzzle first")
        print("Selection: Based on computational power and luck")
        print("-" * 50)
        
        # Simulate mining competition
        mining_attempts = {}
        for miner in self.pow_miners:
            # Higher hash power = more attempts = better chance
            attempts = miner.hash_power * random.randint(1, 10)
            mining_attempts[miner] = attempts
            print(f"{miner.name}: {attempts:,} hash attempts")
        
        # Winner is miner with most successful attempts (simplified)
        winner = max(mining_attempts.keys(), key=lambda m: mining_attempts[m])
        
        print(f"\n🏆 PoW WINNER: {winner}")
        print(f"Reason: Highest computational effort ({mining_attempts[winner]:,} attempts)")
        print(f"Block reward: 6.25 BTC + transaction fees")
        print(f"Energy consumption: High (proportional to hash power)")
        
        winner.blocks_validated += 1
        winner.rewards_earned += 6.25
        
        return winner
    
    def pos_consensus(self):
        """Simulate Proof of Stake consensus"""
        print("\n🏛️  PROOF OF STAKE CONSENSUS SIMULATION")
        print("=" * 50)
        print("Logic: Validators chosen based on their stake in the network")
        print("Selection: Weighted random selection by stake amount")
        print("-" * 50)
        
        # Calculate total stake
        total_stake = sum(staker.calculate_stake_weight() for staker in self.pos_stakers)
        
        # Show stake weights
        for staker in self.pos_stakers:
            stake_weight = staker.calculate_stake_weight()
            percentage = (stake_weight / total_stake) * 100
            print(f"{staker.name}: {stake_weight:,.0f} effective stake ({percentage:.1f}% chance)")
        
        # Weighted random selection
        stakes = [staker.calculate_stake_weight() for staker in self.pos_stakers]
        winner = random.choices(self.pos_stakers, weights=stakes)[0]
        
        print(f"\n🏆 PoS WINNER: {winner}")
        print(f"Reason: Selected via weighted randomness based on stake")
        print(f"Block reward: Transaction fees (no new tokens created)")
        print(f"Energy consumption: Very low (no mining required)")
        
        winner.blocks_validated += 1
        winner.rewards_earned += random.uniform(0.1, 0.5)  # Transaction fees
        
        return winner
    
    def dpos_consensus(self):
        """Simulate Delegated Proof of Stake consensus"""
        print("\n🏆 DELEGATED PROOF OF STAKE CONSENSUS SIMULATION")
        print("=" * 55)
        print("Logic: Token holders vote for delegates who validate blocks")
        print("Selection: Delegate with most votes validates next block")
        print("-" * 55)
        
        # Show delegate vote counts
        for delegate in self.dpos_delegates:
            print(f"{delegate.name}: {delegate.votes_received:,} votes (Rep: {delegate.reputation_score}/100)")
        
        # Winner is delegate with most votes
        winner = max(self.dpos_delegates, key=lambda d: d.votes_received)
        
        print(f"\n🏆 DPoS WINNER: {winner}")
        print(f"Reason: Highest vote count from token holders")
        print(f"Block reward: Shared with voters (minus {winner.commission_rate*100:.1f}% commission)")
        print(f"Energy consumption: Very low (predetermined validator)")
        print(f"Voting transparency: All votes are public and auditable")
        
        winner.blocks_validated += 1
        winner.rewards_earned += random.uniform(0.2, 0.8)
        
        return winner
    
    def compare_mechanisms(self):
        """Compare all three consensus mechanisms"""
        print("\n🔄 RUNNING CONSENSUS COMPARISON")
        print("=" * 60)
        
        # Run all three mechanisms
        pow_winner = self.pow_consensus()
        pos_winner = self.pos_consensus()
        dpos_winner = self.dpos_consensus()
        
        # Summary comparison
        print(f"\n📋 CONSENSUS RESULTS SUMMARY")
        print("=" * 60)
        print(f"PoW Winner:  {pow_winner.name} (High energy, high security)")
        print(f"PoS Winner:  {pos_winner.name} (Low energy, stake-based)")
        print(f"DPoS Winner: {dpos_winner.name} (Low energy, vote-based)")
        
        print(f"\n🔍 KEY DIFFERENCES:")
        print("-" * 30)
        print("• PoW: Miners compete with computational power")
        print("• PoS: Validators chosen by stake weight")
        print("• DPoS: Delegates elected by token holder votes")
        print()
        print("• PoW: Highest energy consumption")
        print("• PoS: Low energy, economic security")
        print("• DPoS: Lowest energy, democratic selection")
    
    def run_multiple_rounds(self, rounds=5):
        """Run multiple consensus rounds to show variation"""
        print(f"\n🔄 RUNNING {rounds} CONSENSUS ROUNDS")
        print("=" * 60)
        
        pow_winners = {}
        pos_winners = {}
        dpos_winners = {}
        
        for round_num in range(1, rounds + 1):
            print(f"\n--- ROUND {round_num} ---")
            
            # PoW (simplified display)
            pow_attempts = {miner.name: miner.hash_power * random.randint(1, 10) 
                           for miner in self.pow_miners}
            pow_winner = max(pow_attempts.keys(), key=lambda m: pow_attempts[m])
            pow_winners[pow_winner] = pow_winners.get(pow_winner, 0) + 1
            print(f"PoW: {pow_winner}")
            
            # PoS
            stakes = [staker.calculate_stake_weight() for staker in self.pos_stakers]
            pos_winner = random.choices(self.pos_stakers, weights=stakes)[0].name
            pos_winners[pos_winner] = pos_winners.get(pos_winner, 0) + 1
            print(f"PoS: {pos_winner}")
            
            # DPoS (same winner each time unless votes change)
            dpos_winner = max(self.dpos_delegates, key=lambda d: d.votes_received).name
            dpos_winners[dpos_winner] = dpos_winners.get(dpos_winner, 0) + 1
            print(f"DPoS: {dpos_winner}")
        
        # Show statistics
        print(f"\n📊 {rounds}-ROUND STATISTICS")
        print("=" * 40)
        print("PoW Winners:")
        for winner, count in pow_winners.items():
            print(f"  {winner}: {count}/{rounds} blocks ({count/rounds*100:.1f}%)")
        
        print("\nPoS Winners:")
        for winner, count in pos_winners.items():
            print(f"  {winner}: {count}/{rounds} blocks ({count/rounds*100:.1f}%)")
        
        print("\nDPoS Winners:")
        for winner, count in dpos_winners.items():
            print(f"  {winner}: {count}/{rounds} blocks ({count/rounds*100:.1f}%)")

def interactive_consensus():
    """Interactive consensus mechanism explorer"""
    simulator = ConsensusSimulator()
    
    while True:
        print(f"\n{'='*60}")
        print("INTERACTIVE CONSENSUS MECHANISM SIMULATOR")
        print(f"{'='*60}")
        print("1. Display all validators")
        print("2. Run PoW consensus")
        print("3. Run PoS consensus") 
        print("4. Run DPoS consensus")
        print("5. Compare all mechanisms")
        print("6. Run multiple rounds")
        print("7. Reset simulation")
        print("8. Exit")
        
        choice = input("\nChoose option (1-8): ").strip()
        
        if choice == "1":
            simulator.display_validators()
        elif choice == "2":
            simulator.pow_consensus()
        elif choice == "3":
            simulator.pos_consensus()
        elif choice == "4":
            simulator.dpos_consensus()
        elif choice == "5":
            simulator.compare_mechanisms()
        elif choice == "6":
            try:
                rounds = int(input("How many rounds to simulate? (1-20): "))
                if 1 <= rounds <= 20:
                    simulator.run_multiple_rounds(rounds)
                else:
                    print("Please enter a number between 1-20")
            except ValueError:
                print("Please enter a valid number!")
        elif choice == "7":
            simulator = ConsensusSimulator()
            print("Simulation reset with new random values!")
        elif choice == "8":
            print("Thanks for exploring consensus mechanisms! 🚀")
            break
        else:
            print("Invalid choice! Please select 1-8.")

def main():
    """Main demonstration function"""
    print("🏛️  BLOCKCHAIN CONSENSUS MECHANISMS SIMULATOR")
    print("=" * 60)
    print("This simulation demonstrates three major consensus mechanisms:")
    print("• Proof of Work (PoW) - Bitcoin's approach")
    print("• Proof of Stake (PoS) - Ethereum 2.0's approach") 
    print("• Delegated Proof of Stake (DPoS) - EOS/Tron approach")
    print("=" * 60)
    
    # Create and run simulation
    simulator = ConsensusSimulator()
    simulator.display_validators()
    simulator.compare_mechanisms()
    
    print(f"\n🎯 EDUCATIONAL INSIGHTS:")
    print("=" * 40)
    print("• PoW provides security through computational work")
    print("• PoS aligns incentives through economic stake")
    print("• DPoS enables democratic governance through voting")
    print("• Each has trade-offs in security, energy, and decentralization")
    
    # Ask for interactive mode
    print(f"\n{'='*60}")
    interactive = input("Would you like to try interactive mode? (y/n): ").lower().strip()
    if interactive in ['y', 'yes']:
        interactive_consensus()

if __name__ == "__main__":
    main()