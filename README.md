# WareHome

PoC for simple home supplies management app.

## Idea

Managing home supplies of multiple products. 
Main problem to solve is to avoid buying 9th can of chopped tomatoes, 
cause noone remembered to check if there is any home, before going to shop.

### PoC flow

1. Buy products
2. Come home
3. Scan barcodes of all products

Simple as that...

And in reverse:
1. Scan product which you are about to use
2. Go shopping
3. Be sure, that you are not buying 4th packaging of toilet paper this week


### Biggest problems to overcome

- Barcode databases/apis are mostly very costly to use, and "some" products always are missing, 
or some important details are missing. There are some 'free' apis with some items, 
and most notable I was able to find is https://upcdatabase.org/dashboard, 
which allows 100 free requests per day, and has option to submit missing products. 
- Making UI somehow reasonable, so adding and removing supplies is fast and easy.
- Making neat UI to list and search stocked items, and notify about expiring products.
