# intramirror-api-wrapper
a simple and dummy wrapper for http://www.intramirror.com/


# Disclaimer
This deployment is NOT intended for a user-friendly production environment, 'cause is designed for specific use by a developer.

## Author

giuseppechecchia@gmail.com

## Examples

products = [] # load your products here
stocks = [] # load your stocks here
start_created = '' # example: 1631700508331
end_created = '' # example: 1632132508000

IntramirrorApi = IntramirrorApi("{your ecommerce ID here}")

result = IntramirrorApi.createProducts(products)
result = IntramirrorApi.updateStocks(stocks)
result = IntramirrorApi.getOrders(start_created, end_created, 0, 50)