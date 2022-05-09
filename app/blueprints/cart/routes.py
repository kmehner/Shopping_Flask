from . import cart
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import ProductForm, SearchForm
from .models import Product, Cart
from app import db

@cart.route('/')
def index():
    title = 'Home'
    products = Product.query.all()
    return render_template('index.html', title=title, products=products)

# Creating the product routes (eventually set to admin function)

@cart.route('/create-product', methods=['GET', 'POST'])
@login_required
def create_product():
    title = 'Create a Product'
    form = ProductForm()
    products = Product.query.all()

    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        try:
            new_product = Product(name=name, price=price, description=description, user_id=current_user.id)
        except:
            flash("This product already exists! Please try again with another Product Name", 'danger')
            return redirect(url_for('cart.create_product'))
        else:
            flash(f"{new_product.name} has been created", 'secondary')

        return redirect(url_for('cart.index'))
    return render_template('create_product.html', title=title, form=form)

# Get A Single product by ID
@cart.route('/products/<product_id>')
@login_required
def single_product(product_id):
    product = Product.query.get_or_404(product_id)
    title = "More information"
    return render_template('single_product.html', title=title, product=product)

# Get all products that match search
@cart.route('/search-products', methods=['GET', 'POST'])
def search_products():
    title = 'Search Products'
    form = SearchForm()
    products = []
    message = ""
    if form.validate_on_submit():
        term = form.search.data
        products = Product.query.filter( ( Product.name.ilike(f'%{term}%')) | ( Product.price.ilike(f'%{term}%')) ).all()
        if not products:
            message = "There are no products that match your search"
    return render_template('search_products.html', title=title, products=products, form=form, message=message)

# insert my_products (edit, delete)


# Cart routes 

# @cart.route('/select-products')
# def select_products():
#     title = 'Cart Products'
#     products = Cart.query.all()
#     return render_template('select_products.html', title=title, products=products)

# update the quantity eventually sick 
@cart.route('/add-to-cart/<product_id>')
@login_required 
def add_to_cart(product_id):
    product_to_add = Product.query.get_or_404(product_id)
    if product_to_add:
        user_cart = current_user.my_cart.all()
        product_id = product_to_add.id
        current_user_id = current_user.id
        if product_to_add in user_cart: # update quantity not add
            quantity = product_to_add.quantity + 1
        else:
            quantity = 1
        add_to_cart = Cart(user_id = current_user_id, product_id = product_id, quantity=quantity)
        flash(f"Product has been added to your cart.", "success")
        return redirect(url_for('cart.index'))
    else:
        flash("Sorry, there was an error adding this item to your cart.", "danger")
        return redirect(url_for('cart.index'))

@cart.route('/my-cart-products', methods=['GET', 'POST'])
@login_required
def my_cart_products():
    title = 'My Cart'
    form = SearchForm()


    products = [Product.query.filter(Product.id == cart.product_id).all()[0] for cart in current_user.my_cart.all()]
    total = sum([float(product.price) for product in products])

    duplicate = {}
    cart = []

    for p in products:
        if p.id not in duplicate.keys():
            duplicate[p.id] = 1
            cart.append(p)
        else:
            print("else")
            duplicate[p.id] += 1

    products = cart
    user_cart = zip(products, cart)

    # Apply filter - eventually add clear filter button and add count (else count +=1 and send it through)
    if form.validate_on_submit():
        term = form.search.data
        cart_search = Cart.query.filter(Cart.user_id == current_user.id).all()
        cart = []

        duplicate = {}

        products = db.session.query(Product).join(Cart).filter(Product.id == Cart.product_id).filter(Product.name.ilike(f'%{term}%')).filter(Cart.user_id == current_user.id).all()

        for p in products:
            if p.id not in duplicate.keys():
                cart.append(p)
                count = 0
                for item in cart_search:
                    if item.product_id == p.id:
                        count += 1
                duplicate[p.id] = count

        user_cart = zip(products, cart)
        total = sum([float(product.price) for product in products])
        return render_template('my_cart_products.html', title=title, products=products, total=total, form=form, user_cart=user_cart, duplicate = duplicate)


    return render_template('my_cart_products.html', title=title, form=form, user_cart=user_cart, total=total, duplicate=duplicate)


@cart.route("/remove-from-cart/<int:cart_id>")
@login_required
def remove_from_cart(cart_id):
    title = 'Remove product from cart'
    cart = Cart.query.get_or_404(cart_id)
    cart.delete()
    flash('Product has been removed from your cart!', 'success')
    return redirect(url_for('cart.my_cart_products'))


@cart.route('/checkout')
@login_required 
def checkout():
    my_cart = current_user.my_cart.all()
    for cart in my_cart:
        cart.delete()
    flash(f"You have successfully checked out! Your cart is now empty.", "success")
    return redirect(url_for('cart.index'))
