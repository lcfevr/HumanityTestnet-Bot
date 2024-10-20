from web3 import Web3
from colorama import init, Fore, Style
import sys
import time
import itertools

# Initialize colorama
init(autoreset=True)

# Display header
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
    sys.exit(1)

# Smart contract address and ABI
contract_address = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
contract_abi = [{"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"bufferSafe","type":"bool"}],"name":"ReferralRewardBuffered","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"enum IRewards.RewardType","name":"rewardType","type":"uint8"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cycleStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vcContract","type":"address"},{"internalType":"address","name":"tkn","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"startTimestamp","type":"uint256"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]  # Masukkan ABI kontrak Anda di sini

# Load the contract
contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contract_abi)

# Load private keys from a text file
def load_private_keys(file_path):
    with open(file_path, 'r') as file:
        private_keys = [line.strip() for line in file if line.strip()]
    return private_keys

# Function to claim rewards
def claim_rewards(private_key, account_number):
    try:
        account = web3.eth.account.from_key(private_key)
        sender_address = account.address

        print(Fore.YELLOW + Style.BRIGHT + f"\n=== Akun {account_number} ===")
        print(Style.BRIGHT + Fore.GREEN + f"Alamat: {sender_address}")
        
        loading_animation("Cek Status Claim Reward\n")

        # Check if genesis reward is already claimed
        genesis_reward_claimed = contract.functions.userGenesisClaimStatus(sender_address).call()

        # Get the current epoch and claim status
        current_epoch = contract.functions.currentEpoch().call()
        reward_claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()
        buffer_amount, claim_status = reward_claim_status

        if genesis_reward_claimed:
            if not claim_status:
                print(Fore.GREEN + f"✅ Melanjutkan klaim reward oleh {sender_address}.")
                proceed_to_claim(sender_address, private_key)
            else:
                print(Fore.YELLOW + f"🚫 Reward sudah diklaim oleh {sender_address}. Next.")
        else:
            print(Fore.GREEN + f"✅ Klaim genesis reward oleh {sender_address}.")
            proceed_to_claim(sender_address, private_key)

    except Exception as e:
        print(Fore.RED + f"❌ Error klaim reward oleh {sender_address}: {str(e)}")

# Function to proceed with reward claim
def proceed_to_claim(sender_address, private_key):
    try:
        tx = contract.functions.claimReward().build_transaction({
            'from': sender_address,
            'nonce': web3.eth.get_transaction_count(sender_address),
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(Fore.CYAN + "⏳ Menunggu konfirmasi transaksi...")
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 1:
            print(Fore.GREEN + f"🎉 Reward berhasil diklaim! Hash transaksi: {web3.to_hex(tx_hash)}\n")
        else:
            print(Fore.RED + "⚠️  Transaksi gagal.")

    except Exception as e:
        print(Fore.RED + f"⚠️  Error saat klaim reward untuk {sender_address}: {str(e)}")

# Countdown function with spinner animation
def countdown(seconds):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while seconds:
        hours, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        timer = f"{hours:02}:{mins:02}:{secs:02}"
        print(Fore.CYAN + f"\rMenunggu selama {timer} " + next(spinner), end="")
        time.sleep(1)
        seconds -= 1
    print(Fore.CYAN + "\n🌟 Selesai menunggu!")

# Loading animation
def loading_animation(message):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    print(Fore.CYAN + message, end="")
    for _ in range(20):
        print(next(spinner), end="\r")
        time.sleep(0.1)
    print(" " * 20, end="\r")

# Main function
def main():
    display_header()

    # Load private keys
    private_keys = load_private_keys('private_keys.txt')

    # Check and claim rewards for each account
    for idx, private_key in enumerate(private_keys, start=1):
        claim_rewards(private_key, idx)

    # Wait for 23 hours 59 minutes (86,340 seconds)
    countdown(86340)

if __name__ == '__main__':
    main()
