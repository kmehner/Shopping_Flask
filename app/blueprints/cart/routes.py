from . import cart
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import ItemForm, SearchForm
from .models import Item

@cart.route('/')
def index():
    title = 'Home'
    items = Item.query.all()
    return render_template('index.html', title=title, items=items)


@cart.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    title = 'Create A Post'
    form = ItemForm()
    if form.validate_on_submit():
        title = form.title.data
        price = form.price.data
        new_item = Item(title=title, price=price, user_id=current_user.id)
        flash(f"{new_item.title} has been created", 'secondary')
        return redirect(url_for('cart.index'))
    return render_template('add_products.html', title=title, form=form)