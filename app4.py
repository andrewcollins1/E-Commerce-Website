from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import cast, Float

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '10'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
db = SQLAlchemy(app)

# --- Models ---
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    price = db.Column(db.String(16))  # still stored as string
    environment = db.Column(db.String(255))  # also string
    description = db.Column(db.Text)
    full_description = db.Column(db.Text)
    imageId = db.Column(db.String(255))

# --- Forms ---
class ItemNumberForm(FlaskForm):
    item_number = StringField('Number to Add:', validators=[DataRequired()])
    submit = SubmitField('Submit')

# --- Utility Function ---
def add_product_to_basket(product_id, quantity):
    if 'basket' not in session:
        session['basket'] = {}

    basket = session['basket']
    product_id_str = str(product_id)

    if product_id_str in basket:
        basket[product_id_str] += quantity
    else:
        basket[product_id_str] = quantity

    session['basket'] = basket
    session.modified = True

# --- Routes ---
@app.route('/')
def galleryPage():
    sort_by = request.args.get('sort', 'name')

    if sort_by == 'price':
        products = Product.query.order_by(
            cast(Product.price, Float)
        ).all()
    elif sort_by == 'environment':
        products = Product.query.order_by(
            cast(Product.environment, Float)
        ).all()
    else:
        products = Product.query.order_by(Product.name.asc()).all()

    return render_template('index.html', products=products, current_sort=sort_by)

@app.route('/add-to-basket', methods=['POST'])
def add_to_basket():
    try:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))

        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        add_product_to_basket(product_id, quantity)

    except (ValueError, TypeError):
        pass  # You can add flash messaging here

    return redirect(url_for('galleryPage'))

@app.route('/product/<int:productId>', methods=['GET', 'POST'])
def singleProductPage(productId):
    product = Product.query.get_or_404(productId)

    form = ItemNumberForm()
    error_message = None

    if form.validate_on_submit():
        try:
            quantity = int(form.item_number.data)
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")

            add_product_to_basket(productId, quantity)

        except ValueError:
            error_message = "Please enter a valid positive number."

    return render_template('SingleTech.html', product=product, form=form, basket=session.get('basket', {}), error_message=error_message, Product=Product)

@app.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_basket(product_id):
    product_id_str = str(product_id)

    if 'basket' in session and product_id_str in session['basket']:
        session['basket'].pop(product_id_str)
        session.modified = True

    return redirect(request.referrer or url_for('galleryPage'))

@app.route('/basket')
def view_basket():
    basket = session.get('basket', {})
    basket_items = []

    for product_id_str, quantity in basket.items():
        product = Product.query.get(int(product_id_str))
        if product:
            basket_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity
            })

    return render_template('basket.html', basket_items=basket_items)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    basket = session.get('basket', {})
    basket_items = []
    total = 0.00

    for product_id_str, quantity in basket.items():
        product = Product.query.get(int(product_id_str))
        if product:
            price = float(product.price.strip("£")) if "£" in product.price else float(product.price)
            subtotal = price * quantity
            total += subtotal
            basket_items.append({
                'name': product.name,
                'price': price,
                'quantity': quantity,
                'subtotal': subtotal
            })

    if request.method == 'POST':
        return render_template('confirmation.html', total=total)

    return render_template('checkout.html', basket_items=basket_items, total=total)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
