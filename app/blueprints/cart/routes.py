from . import cart
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import ItemForm, SearchForm
from .models import Item, CustomerCart

@cart.route('/')
def index():
    title = 'Home'
    items = Item.query.all()
    return render_template('index.html', title=title, items=items)


@cart.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    title = 'Add a Product'
    form = ItemForm()
    if form.validate_on_submit():
        title = form.title.data
        price = form.price.data
        new_item = Item(title=title, price=price, user_id=current_user.id)
        flash(f"{new_item.title} has been created", 'secondary')

        return redirect(url_for('cart.index'))
    return render_template('add_products.html', title=title, form=form)

# Get A Single Item by ID
@cart.route('/items/<item_id>')
@login_required
def single_item(item_id):
    item = Item.query.get_or_404(item_id)
    title = item.title
    return render_template('single_item.html', title=title, item=item)

# Get all items that match search
@cart.route('/search-items', methods=['GET', 'POST'])
def search_items():
    title = 'Search'
    form = SearchForm()
    items = []
    if form.validate_on_submit():
        term = form.search.data
        items = Item.query.filter( ( Item.title.ilike(f'%{term}%')) | ( Item.price.ilike(f'%{term}%')) ).all()
    return render_template('search_items.html', title=title, items=items, form=form)

@cart.route('/my-cart-items')
@login_required
def my_items():
    title = 'My Cart Items'
    items = [Item.query.filter(Item.id == cart.item_id).all[0] for cart in current_user.my_cart.all()]
    total = sum([item.price for item in items])
    if items:
        cart = current_user.my_cart.all()
        user_cart = zip(items, cart)
    return render_template('my_items.html', title=title, cart=cart)


@cart.route('/select-items')
def select_items():
    title = 'Cart Items'
    items = CustomerCart.query.all()
    return render_template('select_items.html', title=title, items=items)

@cart.route('/add-to-cart/<item_id>')
@login_required 
def add_to_cart(item_id):
    item = Item.query.get_or_404(item_id)
    add_to_cart = CustomerCart(user_id = current_user.id, item_id = item.id)
    flash(f"{item.title} has been added to your cart.", "success")
    return redirect(url_for('cart.index'))

@cart.route('/checkout')
@login_required 
def checkout():
    my_cart = current_user.my_cart.all()
    for cart in my_cart:
        cart.delete()
    flash(f"You have successfully checked out! Your cart is now empty.", "success")
    return redirect(url_for('cart.index'))

@cart.route("/remove-from-cart/<int:item_id>")
@login_required
def remove_from_cart(item_id):
    title = 'Remove item from cart'
    cart = CustomerCart.query.get_or_404(item_id)
    cart.delete()
    flash('Item has been removed from your cart!', 'success')
    return redirect(url_for('cart.cart_items'))

