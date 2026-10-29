import requests
import json

url = 'https://giqmhpoinnnkfrbqrlid.supabase.co/auth/v1/token?grant_type=password'
headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdpcW1ocG9pbm5ua2ZyYnFybGlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0ODE5NTQsImV4cCI6MjA5MzA1Nzk1NH0.sxMrQCqLfBIIls1mgmWzlCHTlgX2RQ1sW8RBt_GiSzo',
    'Content-Type': 'application/json'
}
data = {
    'email': 'muzaffarzed12@gmail.com',
    'password': '12345678m'
}

r = requests.post(url, headers=headers, json=data)
res = r.json()
if 'access_token' in res:
    print('SUCCESS: Logged in successfully!')
    print('User ID:', res['user']['id'])
    print('Email:', res['user']['email'])
    token = res['access_token']
    auth_headers = {'apikey': headers['apikey'], 'Authorization': f'Bearer {token}'}

    # Query products
    p_url = 'https://giqmhpoinnnkfrbqrlid.supabase.co/rest/v1/products?select=id,name,category&order=name'
    p_res = requests.get(p_url, headers=auth_headers).json()
    print(f"\nPRODUCTS (Jami {len(p_res)} ta):")
    for p in p_res:
        print(f"  - {p['name']} | Kategoriya: {p.get('category')} | ID: {p['id']}")

    # Query warehouses
    w_url = 'https://giqmhpoinnnkfrbqrlid.supabase.co/rest/v1/warehouses?select=id,name'
    w_res = requests.get(w_url, headers=auth_headers).json()
    print(f"\nSKLADLAR (Warehouses):")
    for w in w_res:
        print(f"  - {w['name']} (ID: {w['id']})")

    # Query branches
    b_url = 'https://giqmhpoinnnkfrbqrlid.supabase.co/rest/v1/branches?select=id,name'
    b_res = requests.get(b_url, headers=auth_headers).json()
    print(f"\nFILIALLAR (Branches):")
    for b in b_res:
        print(f"  - {b['name']} (ID: {b['id']})")

    # Query customers
    c_url = 'https://giqmhpoinnnkfrbqrlid.supabase.co/rest/v1/customers?select=id,name,phone,balance,credit_limit&order=name'
    c_res = requests.get(c_url, headers=auth_headers).json()
    print(f"\nMIJOZLAR (Jami {len(c_res)} ta):")
    for c in c_res:
        print(f"  - {c['name']} | Tel: {c.get('phone')} | Qarz: {c.get('balance')} | Limit: {c.get('credit_limit')}")

    # Query pricelist overrides
    po_url = 'https://giqmhpoinnnkfrbqrlid.supabase.co/rest/v1/pricelist_overrides?select=*'
    po_res = requests.get(po_url, headers=auth_headers).json()
    print(f"\nNARX O'ZGARISHLARI (Pricelist Overrides, jami {len(po_res)} ta):")
    for po in po_res:
        print(f"  - Product ID: {po.get('product_id')} | Narx: {po.get('price')} | Ustama: {po.get('markup')}%")

    # Query inventory batches (Qoldiqlar)
    ib_url = 'https://giqmhpoinnnkfrbqrlid.supabase.co/rest/v1/inventory_batches?select=product_id,remaining,cost_price,warehouse_id&remaining=gt.0'
    ib_res = requests.get(ib_url, headers=auth_headers).json()
    print(f"\nQOLDIQLAR (Inventory Batches, jami {len(ib_res)} ta partiya):")
    for ib in ib_res[:10]:
        print(f"  - Product ID: {ib.get('product_id')} | Qoldiq: {ib.get('remaining')} | Tannarx: {ib.get('cost_price')}")

else:
    print('LOGIN FAILED:', res)
