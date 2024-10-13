from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
import json
import ipfshttpclient

# Initialize IPFS client
ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

def send_solana_transaction(ipfs_hash):
    try:
        # Initialize Solana client
        client = Client("https://api.devnet.solana.com")

        # Load keypairs
        owner_keypair = Keypair.from_file("/path/to/owner_keypair.json")
        receiver_keypair = Keypair.from_file("/path/to/receiver_keypair.json")

        # Get recent blockhash
        recent_blockhash = client.get_recent_blockhash()["result"]["value"]["blockhash"]

        # Create transfer instruction
        transfer_instruction = transfer(TransferParams(
            from_pubkey=owner_keypair.public_key,
            to_pubkey=receiver_keypair.public_key,
            lamports=1000000  # 0.001 SOL
        ))

        # Create transaction
        transaction = Transaction()
        transaction.add(transfer_instruction)
        transaction.recent_blockhash = recent_blockhash

        # Sign transaction
        transaction.sign(owner_keypair)

        # Send transaction
        tx_hash = client.send_transaction(transaction)

        return tx_hash["result"]
    except Exception as e:
        print(f"Error in Solana transaction: {str(e)}")
        return None

def upload_to_ipfs(data):
    res = ipfs_client.add_str(data)
    return res['Hash']