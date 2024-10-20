from web3 import Web3
from colorama import init, Fore, Style
import sys
import time
import itertools

# Initialize colorama
init(autoreset=True)

# Header message
def display_header():
    print(Fore.CYAN + Style.BRIGHT + "===============================")
    print(Fore.YELLOW + Style.BRIGHT + "   Auto Claim Humanity Protocol")
    print(Fore.CYAN + Style.BRIGHT + "   Bot created by: " + Fore.GREEN + "https://t.me/AirdropInsiderID")
    print(Fore.CYAN + Style.BRIGHT + "===============================\n")

# Connect to the blockchain network
rpc_url = 'https://rpc.testnet.humanity.org'
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if connected to the network
if web3.is_connected():
    print(Fore.GREEN + "Connected to Humanity Protocol")
else:
    print(Fore.RED + "Connection failed.")
    sys.exit(1)  # Exit if connection fails

# Smart contract address and ABI
contract_address = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
contract_abi = [{"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"bufferSafe","type":"bool"}],"name":"ReferralRewardBuffered","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"enum IRewards.RewardType","name":"rewardType","type":"uint8"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cycleStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vcContract","type":"address"},{"internalType":"address","name":"tkn","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"startTimestamp","type":"uint256"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]  # Masukkan ABI kontrak Anda di sini

# Load the contract
contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contract_abi)

# Function to load private keys from a text file
def load_private_keys(file_path):
    with open(file_path, 'r') as file:
        private_keys = [line.strip() for line in file if line.strip()]
    return private_keys

# Function to claim rewards
def claim_rewards(private_key, account_number):
    try:
        # Derive the sender's address from the private key
        account = web3.eth.account.from_key(private_key)
        sender_address = account.address

        # Tampilkan akun dalam format bold
        print(Fore.YELLOW + Style.BRIGHT + f"\n\n=== Akun {account_number} ===")
        print(Style.BRIGHT + Fore.GREEN + f"Alamat: {sender_address}")
        
        # Loading animation
        loading_animation("Cek Status Claim Reward\n")

        # Check if the genesis reward has already been claimed
        genesis_reward_claimed = contract.functions.userGenesisClaimStatus(sender_address).call()

        # Get the current epoch from the contract
        current_epoch = contract.functions.currentEpoch().call()

        # Check if the reward has already been claimed for the current epoch
        reward_claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()

        # reward_claim_status is a tuple: (buffer, claimStatus)
        buffer_amount, claim_status = reward_claim_status
        
        # If the genesis reward is claimed
        if genesis_reward_claimed:
            # If userClaimStatus is False, proceed to claim the reward
            if not claim_status:
                print(Fore.GREEN + f"✅ Melanjutkan klaim reward untuk alamat: {sender_address} (Genesis reward sudah diklaim).")
                proceed_to_claim(sender_address, private_key)
            else:
                print(Fore.YELLOW + f"🚫 Reward sudah diklaim untuk alamat: {sender_address} di epoch {current_epoch}. Next!.\n")
        else:
            print(Fore.GREEN + f"✅ Melanjutkan klaim reward untuk alamat: {sender_address} (Genesis reward belum diklaim).")
            proceed_to_claim(sender_address, private_key)

    except Exception as e:
        error_message = str(e)

        # Check for specific error: "Rewards: user not registered"
        if "Rewards: user not registered" in error_message:
            print(Fore.RED + f"❌ Error: User {sender_address} tidak terdaftar.")
        else:
            print(Fore.RED + f"❌ Error klaim reward untuk {sender_address}: {error_message}")

def proceed_to_claim(sender_address, private_key):
    try:
        # Estimate gas limit for the claimReward transaction
        gas_amount = contract.functions.claimReward().estimate_gas({
            'chainId': web3.eth.chain_id,
            'from': sender_address,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address)
        })

        # Build the transaction to call the 'claimReward' function
        transaction = contract.functions.claimReward().build_transaction({
            'chainId': web3.eth.chain_id,
            'from': sender_address,
            'gas': gas_amount,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address)
        })

        # Sign the transaction with the private key
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print(Fore.GREEN + f"🎉 Transaksi berhasil untuk {sender_address} dengan hash: {web3.to_hex(tx_hash)}\n")
    
    except Exception as e:
        print(Fore.RED + f"❌ Error dalam proses klaim untuk {sender_address}: {str(e)}\n")

# Function for countdown with spinner animation
def countdown(seconds):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02}:{secs:02}"
        print(Fore.CYAN + f"\rMenunggu selama {timer} " + next(spinner), end="")
        time.sleep(1)
        seconds -= 1
    print(Fore.CYAN + "\n🌟 Selesai menunggu!")

# Loading animation
def loading_animation(message):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    print(Fore.CYAN + message, end="")
    for _ in range(20):  # Adjust the range for the loading duration
        print(next(spinner), end="\r")
        time.sleep(0.1)  # Adjust the speed of the spinner
    print(" " * 20, end="\r")  # Clear the spinner

# Main execution: display header, load private keys, and claim rewards for each
if __name__ == "__main__":
    display_header()
    # Infinite loop to run the process setiap 2 jam
    while True:
        private_keys = load_private_keys('private_keys.txt')
        for i, private_key in enumerate(private_keys):
            claim_rewards(private_key, i + 1)

        # Tunggu selama 2 jam (2 * 60 * 60 detik)
        countdown(2 * 1 * 1 + 1 * 60)  # 2 jam 1 menit
