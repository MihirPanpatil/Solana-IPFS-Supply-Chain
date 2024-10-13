from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.publickey import PublicKey
from solana.account import Account
import ipfshttpclient
import json

solana_client = Client("https://api.devnet.solana.com")
ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

def upload_to_ipfs(data):
    res = ipfs_client.add_str(data)
    return res['Hash']

def send_solana_transaction(tx_data):
    # Load the keypair files
    owner_keypair = Account(json.load(open('~/.config/solana/owner_keypair.json')))
    receiver_keypair = Account(json.load(open('~/.config/solana/receiver_keypair.json')))

    # Create a new transaction
    tx = Transaction()
    tx.add(
        tx.create_account(
            owner=owner_keypair.public_key(),
            lamports=1000000000,  # 1 SOL
            space=1024,
            new_account=receiver_keypair.public_key(),
        )
    )

    # Sign and send the transaction
    tx_hash = solana_client.send_transaction(tx, owner_keypair)
    return tx_hash