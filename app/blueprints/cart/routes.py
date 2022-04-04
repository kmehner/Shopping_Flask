from . import cart
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import ItemForm, SearchForm, CustomerCartForm
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


@cart.route('/my-items')
@login_required
def my_items():
    title = 'My Items'
    items = current_user.cart_items.all()
    return render_template('my_items.html', title=title, items=items)

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

@cart.route('/cart-items')
def cart_items():
    title = 'Home'
    items = CustomerCart.query.all()
    return render_template('cart_items.html', title=title, items=items)