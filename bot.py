from web3 import Web3
from colorama import init, Fore, Style
import sys
import time
import itertools
from config import rpc_url, contract_address, contract_abi

# Initialize colorama
init(autoreset=True)

# Address kontrak Reward Token (RWT)
reward_token_address = "0x693cB8de384f00A5c2580D544B38013BFB496529"

# ABI minimal untuk fungsi balanceOf ERC20
erc20_abi = '''
[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]
'''

# Header message
def display_header():
    print(Fore.CYAN + Style.BRIGHT + "===============================")
    print(Fore.YELLOW + Style.BRIGHT + "Auto Claim Humanity Protocol")
    print(Fore.CYAN + Style.BRIGHT + "Bot created by: " + Fore.GREEN + "https://t.me/AirdropInsiderID")
    print(Fore.CYAN + Style.BRIGHT + "===============================\n")

# Connect to the blockchain network
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if connected to the network
if web3.is_connected():
    print(Fore.GREEN + "Connected to Humanity Protocol")
else:
    print(Fore.RED + "Connection failed.")
    sys.exit(1)  # Exit if connection fails

# Load the contract
contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contract_abi)

# Load the reward token contract (RWT) with ERC20 minimal ABI
reward_token_contract = web3.eth.contract(address=Web3.to_checksum_address(reward_token_address), abi=erc20_abi)

# Function to load private keys from a text file
def load_private_keys(file_path):
    with open(file_path, 'r') as file:
        private_keys = [line.strip() for line in file if line.strip()]
    return private_keys

# Function to get RWT balance for an account
def get_rwt_balance(account_address):
    balance = reward_token_contract.functions.balanceOf(account_address).call()
    return web3.from_wei(balance, 'ether')  # Assuming RWT has 18 decimals like typical ERC20 tokens

# Function to claim rewards
def claim_rewards(private_key):
    try:
        account = web3.eth.account.from_key(private_key)
        sender_address = account.address

        # Cek status klaim rewards
        genesis_reward_claimed = contract.functions.userGenesisClaimStatus(sender_address).call()
        current_epoch = contract.functions.currentEpoch().call()
        reward_claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()
        buffer_amount, claim_status = reward_claim_status

        
        if genesis_reward_claimed:
            if not claim_status:
                print(Fore.GREEN + f"Proceeding to claim reward for address: {sender_address} (Genesis reward claimed).")
                proceed_to_claim(sender_address, private_key)
            else:
                print(Fore.YELLOW + f"Reward already claimed for address: {sender_address} in epoch {current_epoch}.")
                return True  # Return True untuk menandakan sudah diklaim
        else:
            print(Fore.GREEN + f"Proceeding to claim reward for address: {sender_address} (Genesis reward not claimed).")
            proceed_to_claim(sender_address, private_key)

    except Exception as e:
        error_message = str(e)
        if 'replacement transaction underpriced' in error_message:
            print(Fore.RED + f"Error for address {sender_address}: Replacement transaction underpriced. Retrying with higher gas price.")
        elif 'insufficient funds for gas' in error_message:
            print(Fore.RED + f"Error for address {sender_address}: Insufficient funds for gas.")
        else:
            print(Fore.RED + f"Error for address {sender_address}: {error_message}")
    
    return False  

# Function to claim the reward
def proceed_to_claim(sender_address, private_key):
    try:
        transaction = contract.functions.claimReward().build_transaction({
            'from': sender_address,
            'gas': 250000,
            'gasPrice': web3.to_wei('2', 'gwei'),
            'nonce': web3.eth.get_transaction_count(sender_address),
            'chainId': 11235
        })

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(Fore.CYAN + f"Transaction sent for address {sender_address}. Transaction hash: {web3.to_hex(tx_hash)}")

        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] == 1:
            print(Fore.GREEN + f"Transaction confirmed for address {sender_address}. Reward claimed successfully.")
        else:
            print(Fore.RED + f"Transaction failed for address {sender_address}.")
    except Exception as e:
        print(Fore.RED + f"Error in proceed_to_claim for address {sender_address}: {str(e)}")

# Function to display animated countdown with spinner and progress bar
def animated_countdown(seconds):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    start_time = time.time()
    end_time = start_time + seconds
    total_duration = seconds
    
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60

        progress = 1 - (remaining_time / total_duration)
        progress_bar = '#' * int(progress * 30) + '-' * (30 - int(progress * 30))

        sys.stdout.write(
            Fore.YELLOW + f"\rWaiting... {next(spinner)} [{progress_bar}] {hours:02}:{minutes:02}:{seconds:02} remaining"
        )
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 80 + "\r")

# Main execution loop with infinite cycle
if __name__ == '__main__':
    display_header()
    private_keys = load_private_keys('private_keys.txt')

    try:
        while True:  # Loop terus menerus sampai dihentikan oleh user (misalnya dengan Ctrl+C)
            all_claimed = True
            for idx, private_key in enumerate(private_keys, start=1):
                account = web3.eth.account.from_key(private_key)
                sender_address = account.address

                # Countdown sebelum memproses klaim reward
                animated_countdown(5)
                
                # Tampilkan akun dan alamatnya
                print(Fore.CYAN + f"Akun {idx} - {sender_address}")

                # Proses klaim reward terlebih dahulu
                claimed = claim_rewards(private_key)

                # Cek saldo RWT setelah pengecekan klaim reward
                rwt_balance = get_rwt_balance(sender_address)
                print(Fore.MAGENTA + f"Balance = {rwt_balance} RewardToken (RWT)\n")

                # Jika ada akun yang belum meng-claim reward, maka set all_claimed menjadi False
                current_epoch = contract.functions.currentEpoch().call()
                reward_claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()
                _, claim_status = reward_claim_status

                if not claim_status:
                    all_claimed = False

                n
                print(Fore.CYAN + "-------------------------------------------")

            if all_claimed:
                print(Fore.CYAN + "All accounts have claimed their rewards. Waiting before the next cycle.")
                animated_countdown(6 * 60 * 60)  
            else:
                print(Fore.CYAN + "Some accounts still have pending rewards. Continuing to the next round.")
                
    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess terminated by user.")
