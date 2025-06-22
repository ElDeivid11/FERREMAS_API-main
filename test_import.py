import importlib

Configuration = importlib.import_module("transbank.webpay.webpay_plus.configuration").Configuration
Transaction = importlib.import_module("transbank.webpay.webpay_plus.transaction").Transaction

print("Import OK")
