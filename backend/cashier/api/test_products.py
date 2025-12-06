from fastapi.testclient import TestClient

def test_all_products(client: TestClient):
    products = client.get("/products")
    assert(products.status_code == 200)
    data = products.json()
    assert(len(data) == 1)
    product_1 = data[0]
    assert(product_1['ean'] == '2052552')
