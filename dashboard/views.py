from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
import requests
import json
import ipfshttpclient

# Solana RPC endpoint
SOLANA_RPC_URL = "https://api.devnet.solana.com"

# IPFS client
ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

def dashboard(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            
            # Handle certificate image
            if 'certificate_image' in request.FILES:
                product.certificate_image = request.FILES['certificate_image']
            
            # Prepare data for IPFS
            product_data = {
                'name': product.name,
                'description': product.description,
                'status': product.status,
                'certificate_image': product.certificate_image.url if product.certificate_image else None
            }
            
            product.ipfs_hash = upload_to_ipfs(json.dumps(product_data))
            product.solana_tx_hash = send_solana_transaction(product.ipfs_hash)
            
            if product.solana_tx_hash == "TRANSACTION_FAILED":
                form.add_error(None, "Solana transaction failed. Please try again.")
            else:
                product.save()
                return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'dashboard/dashboard.html', {'products': products, 'form': form})





def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print(f"Product: {product.name}")
    print(f"Certificate image: {product.certificate_image.name if product.certificate_image else 'No image'}")
    return render(request, 'dashboard/product_detail.html', {'product': product})



def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})

def push_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.status == "Farm":
        product.status = "Processing"
    elif product.status == "Processing":
        product.status = "Distribution"
    elif product.status == "Distribution":
        product.status = "Retail"
    product.save()
    return redirect('product_detail', product_id=product.id)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')
    return render(request, 'dashboard/delete_product.html', {'product': product})

def upload_to_ipfs(data):
    res = ipfs_client.add_str(data)
    print(f"IPFS response: {res}")  # Add this line
    if isinstance(res, dict):
        return res.get('Hash')
    elif isinstance(res, str):
        return res
    else:
        raise ValueError(f"Unexpected response from IPFS: {res}")

import requests
import base64
import json
import time
import random
import string

def generate_realistic_tx_hash():
    # Solana transaction hashes are 64 character base-58 strings
    # We'll simulate this with a mix of lowercase letters and numbers
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(64))

def send_solana_transaction(ipfs_hash):
    # Simulate network latency
    time.sleep(random.uniform(0.5, 2.0))

    # Generate a realistic-looking transaction hash
    tx_hash = generate_realistic_tx_hash()

    # Simulate a small chance of failure (about 5%)
    if random.random() < 0.05:
        return "TRANSACTION_FAILED"

    return tx_hash


def airdrop_sol(public_key, amount):
    airdrop_tx = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "requestAirdrop",
        "params": [public_key, amount]
    }
    response = requests.post(SOLANA_RPC_URL, json=airdrop_tx)
    return response.json().get('result')