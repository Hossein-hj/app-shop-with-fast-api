import requests


class Database():
    

    def __init__(self, debug=True):
        self.site = "http://127.0.0.1:8000/"
        self.timeout = 10
        self.debug = debug   # True: کد وضعیت و جواب json رو چاپ می‌کنه (مثل crud.py)

    # ---------------------- helper -------------------
    def _call(self, method, path, silent=False, **kwargs):
        
        url = f"{self.site}{path}"
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"connection error: {e}")
            return None

        try:
            result = response.json()
        except ValueError:
            result = None

        if self.debug and not silent:
            print(response.status_code)
            print(result)

        if response.status_code == 200:
            return result
        return None

    @staticmethod
    def _int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value

    @staticmethod
    def _product_row(p):
        return (p["id"], p["name"], p["price"])

    @staticmethod
    def _customer_row(c):
        return (c["id"], c["username"], c.get("pic") or "")

    def _factor_rows(self, factors):
        customers = self._call("get", "customers/", silent=True) or []
        names = {c["id"]: c["username"] for c in customers}
        rows = []
        for f in factors:
            rows.append((
                f["id"],
                names.get(f["customer_id"], ""),
                f.get("jalalidate") or f["date"],
                f["total"]
            ))
        return rows

    # ---------------------- products -------------------
    def create_new_products(self, name, price):
        my_data = {
            "name": name,
            "price": self._int(price)   
        }
        return self._call("post", "products/", json=my_data)

    def read_all_products(self):
        result = self._call("get", "products/") or []
        return [self._product_row(p) for p in result]

    def read_products_by_id(self, id):
        result = self._call("get", f"products/{id}")
        if result is None:
            return None
        return self._product_row(result)

    def update_product(self, id, pname_new, price_new):
        my_data = {
            "name": pname_new,
            "price": self._int(price_new)
        }
        return self._call("put", f"products/{id}", json=my_data)

    def delete_product_by_id(self, id):
        return self._call("delete", f"products/{id}")

    def delete_all_products(self):
        
        products = self._call("get", "products/", silent=True) or []
        for p in products:
            self._call("delete", f"products/{p['id']}")

    # ---------------------- customers -------------------
    def create_new_person(self, name, pic, password=""):
        
        my_data = {
            "username": name,
            "password": password,
            "pic": "" if pic is None else str(pic)
        }
        result = self._call("post", "customers/", json=my_data)
        if result is None:
            return None
        return result["id"]

    def read_all_customers(self):
        result = self._call("get", "customers/") or []
        return [self._customer_row(c) for c in result]

    def find_customer(self, name='', id=''):
        if id != '':
            result = self._call("get", f"customers/{id}")
            return [self._customer_row(result)] if result else []

        result = self._call("get", "customers/") or []
        if name != '':
            
            result = [c for c in result if str(name).lower() in c["username"].lower()]
        return [self._customer_row(c) for c in result]

    def update_customer(self, id, user_name, password, pic=None):
        my_data = {
            "id": id,
            "username": user_name,
            "password": password,
            "pic": pic          
        }
        return self._call("put", "customers/", json=my_data)

    def delete_customer(self, id):
        return self._call("delete", f"customers/{id}")

    def delete_all_customers(self):
        return self._call("delete", "customers/")

    def login(self, user_name, password):
        my_params = {
            "username": user_name,
            "password": password
        }
        return self._call("get", "customers/login/", params=my_params)

    # ---------------------- factors -------------------
    def create_new_factor(self, customer_id, date, total=0):
        """id فاکتور جدید رو برمی‌گردونه. date همون تاریخ شمسی‌ایه که main.py می‌فرسته.
        total رو سرور خودش از جمع آیتم‌ها حساب می‌کنه"""
        my_data = {
            "customer_id": customer_id,
            "jalalidate": date
        }
        result = self._call("post", "factors/", json=my_data)
        if result is None:
            return None
        return result["id"]

    def read_all_factors(self):
        result = self._call("get", "factors/") or []
        return self._factor_rows(result)

    def search_factor(self, text):
        
        text = str(text).lower()
        return [r for r in self.read_all_factors()
                if text in str(r[1]).lower() or text in str(r[0])]

    def read_factor(self, factor_id):
        """مثل database.py: (factor, details) برمی‌گردونه
        factor  = {'customer_id', 'customer_name'}
        details = [{'product_id', 'product_name', 'count', 'price', 'total'}, ...]"""
        data = self._call("get", f"factors/{factor_id}")
        if data is None:
            return {"customer_id": None, "customer_name": ""}, []

        customer = self._call("get", f"customers/{data['customer_id']}", silent=True)
        factor = {
            "customer_id": data["customer_id"],
            "customer_name": customer["username"] if customer else ""
        }

        products = self._call("get", "products/", silent=True) or []
        product_names = {p["id"]: p["name"] for p in products}

        details = []
        for item in data["items"]:
            details.append({
                "product_id": item["product_id"],
                "product_name": product_names.get(item["product_id"], ""),
                "count": item["no"],
                "price": item["fee"],
                "total": item["sum_fee"]
            })
        return factor, details

    def update_factor(self, customer_id, total, factor_id, jalalidate=None):
        
        if jalalidate is None:
            current = self._call("get", f"factors/{factor_id}", silent=True)
            if current is None:
                return None
            jalalidate = current["jalalidate"]
        my_data = {
            "customer_id": customer_id,
            "jalalidate": jalalidate
        }
        return self._call("put", f"factors/{factor_id}", json=my_data)

    def delete_factor(self, factor_id):
        return self._call("delete", f"factors/{factor_id}")

    # ---------------------- factor items -------------------
    def _make_items(self, factor_list):
        
        items = []
        for item in factor_list:
            items.append({
                "product_id": item.get("product_id", item.get("id")),
                "no": item.get("no", item.get("No")),
                "fee": item.get("fee", item.get("price"))
            })
        return items

    def save_factor_details(self, factor_id, factor_list):
        
        return self._call("post", f"factors/{factor_id}/items",
                          json=self._make_items(factor_list))

    def update_factor_details(self, factor_id, factor_list):
        
        return self._call("put", f"factors/{factor_id}/items",
                          json=self._make_items(factor_list))


if __name__ == '__main__':
    db = Database()
    print(db.read_all_products())
