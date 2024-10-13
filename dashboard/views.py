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

import asyncio
from .solana_ipfs import send_solana_transaction, upload_to_ipfs

def dashboard(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.ipfs_hash = upload_to_ipfs(product.to_dict())
            product.solana_tx_hash = send_solana_transaction(product.ipfs_hash)
            
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    
    products = Product.objects.all()
    return render(request, 'dashboard/dashboard.html', {'products': products, 'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'dashboard/product_detail.html', {'product': product})

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})

def push_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.status == 'Farm':
        product.status = 'Processing'
    elif product.status == 'Processing':
        product.status = 'Distribution'
    elif product.status == 'Distribution':
        product.status = 'Retail'
    product.save()
    return redirect('product_detail', product_id=product.id)

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')
    return render(request, 'dashboard/delete_product.html', {'product': product})

def upload_to_ipfs(data):
    res = ipfs_client.add_str(data)
    print(f"IPFS response: {res}")  
    if isinstance(res, dict):
        return res.get('Hash')
    elif isinstance(res, str):
        return res
    else:
        raise ValueError(f"Unexpected response from IPFS: {res}")

import requests

def airdrop_sol(public_key, amount):
    airdrop_tx = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "requestAirdrop",
        "params": [public_key, amount]
    }
    response = requests.post(SOLANA_RPC_URL, json=airdrop_tx)
    return response.json().get('result')