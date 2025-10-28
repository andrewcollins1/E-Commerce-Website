from app4 import app, db, Product

products = [
    { "name": "Shirt", "price": "50.00", "environment": "8.1", "description": "A Navy Slim Fitted Shirt with Silk Cuffs", "full_description": "This slim fitted navy shirt is a great piece to have for many occassions, with the slim fit and clean colour making it perfect for dinners and events. The carbon footprint of 8.1 Kg of C02 being low compared to competitors.", "imageId": "shirt.jpg" },
    { "name": "T-Shirt", "price": "25.00", "environment": "7.9", "description": "100% Cotton Oversized Washed Black Tee", "full_description": "This oversized tee is smooth and unassuming making it the perfect piece to go along with many other clothes, the oversized fit makes it ideal for many customers who prefer this style and cotton composition makes it extremely comfortable. The carbon footprint of this tee is 7.9 Kg of C02, the lowest of all our pieces. ", "imageId": "t-shirt.jpg" },
    { "name": "Hoodie", "price": "45.00", "environment": "8.4", "description": "Oversized Boxy Black Hoodie", "full_description": "This hoodie is the perfect hoodie for those want both comfort and looks with the boxy fit being extremely popular nowadays and the heavy material making for a comfortable wear this works for people with any needs. The carbon footprint of this piece is only 8.4 Kg of C02 which is right in line with market average.", "imageId": "hoodie.jpg" },
    { "name": "Jeans", "price": "60.00", "environment": "33.4", "description": "Washed Denim Wide Leg Jean", "full_description": "These wide leg denim jeans are the perfect choice for anyone, the design makes their size very forgiving for those with larger legs, and also perfect for anyone who is looking for a baggier fitted jean, the washed colour also makes them go with many different pieces. The carbon footprinto of 33.4 Kg of C02 may seem high but the process for jeans makes all of them produce more than other items.", "imageId": "jeans.jpg" }

]

with app.app_context():
    db.drop_all( )
    db.create_all()

    for product in products:
        newItem = Product(name = product["name"], price = product["price"], environment = product["environment"], description=product["description"], full_description=product['full_description'], imageId=product["imageId"])
        db.session.add(newItem)

    db.session.commit()