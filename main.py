from fastapi import FastAPI

app = FastAPI()

# -----------------------------
# Sample Products Data
# -----------------------------

products = [
    {"product_id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"product_id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"product_id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"product_id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []


# -----------------------------
# CREATE ORDER
# -----------------------------

@app.post("/orders")
def create_order(customer_name: str, product_id: int):

    order_id = len(orders) + 1

    order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "product_id": product_id
    }

    orders.append(order)

    return {
        "message": "Order created successfully",
        "order": order
    }


# -----------------------------
# SEARCH PRODUCTS
# -----------------------------

@app.get("/products/search")
def search_products(keyword: str):

    results = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            results.append(product)

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }


# -----------------------------
# SORT PRODUCTS
# -----------------------------

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# -----------------------------
# PAGINATION
# -----------------------------

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    total_products = len(products)
    total_pages = (total_products + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": products[start:end]
    }


# -----------------------------
# SEARCH ORDERS (Q4)
# -----------------------------

@app.get("/orders/search")
def search_orders(customer_name: str):

    results = []

    for order in orders:
        if customer_name.lower() in order["customer_name"].lower():
            results.append(order)

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }


# -----------------------------
# SORT BY CATEGORY THEN PRICE (Q5)
# -----------------------------

@app.get("/products/sort-by-category")
def sort_by_category():

    sorted_products = sorted(
        products,
        key=lambda p: (p["category"], p["price"])
    )

    return {"products": sorted_products}


# -----------------------------
# SEARCH + SORT + PAGINATION (Q6)
# -----------------------------

@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = products

    # SEARCH
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # SORT
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # PAGINATION
    total_found = len(result)
    total_pages = (total_found + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_products = result[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paginated_products
    }


# -----------------------------
# BONUS - ORDERS PAGINATION
# -----------------------------

@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):

    total_orders = len(orders)
    total_pages = (total_orders + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "orders": orders[start:end]
    }


# -----------------------------
# GET PRODUCT BY ID
# -----------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["product_id"] == product_id:
            return product

    return {"error": "Product not found"}