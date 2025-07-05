from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import os
import csv
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import smtplib
from email.message import EmailMessage
import mimetypes

app = Flask(__name__)
app.secret_key = "king_secret_key"
app.config['SESSION_TYPE'] = 'filesystem'

pdfmetrics.registerFont(TTFont('DejaVu', 'assets/DejaVuSans.ttf'))

PRODUCTS_FILE = 'data/products.csv'
os.makedirs('bills', exist_ok=True)
os.makedirs('data', exist_ok=True)

# ✅ Ensure products.csv file exists
PRODUCTS_FILE = 'data/products.csv'
if not os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'price'])

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def load_products():
    products = {}
    with open(PRODUCTS_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products[row['id']] = {
                'name': row['name'],
                'price': float(row['price'])
            }
    return products


def load_products_list():
    """For product manager as list of dicts"""
    product_list = []
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_list.append({
                    'id': row['id'],
                    'name': row['name'],
                    'price': row['price']
                })
    return product_list


def save_products_list(products):
    with open(PRODUCTS_FILE, mode="w", newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "price"])
        writer.writeheader()
        writer.writerows(products)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if 'logged_in' not in session:
        return redirect('/')

    products = load_products()
    cart = session.get('cart', [])

    if request.method == 'POST':
        pid = request.form['product_id']
        qty = int(request.form.get('quantity', 1))
        if pid in products:
            item = products[pid]
            cart.append({
                'id': pid,
                'name': item['name'],
                'price': item['price'],
                'qty': qty,
                'subtotal': item['price'] * qty
            })
            session['cart'] = cart
        return redirect('/dashboard')

    total = sum(item['subtotal'] for item in cart)
    gst = total * 0.18
    discount = total * 0.10
    final = total + gst - discount

    return render_template('dashboard.html', products=products, cart=cart,
                           total=total, gst=gst, discount=discount, final=final)


@app.route('/remove/<int:index>')
def remove_item(index):
    if 'cart' in session:
        session['cart'].pop(index)
    return redirect('/dashboard')


@app.route('/generate_bill', methods=['POST'])
@login_required
def generate_bill():
    name = request.form['customer_name']
    mobile = request.form['customer_mobile']
    payment = request.form['payment_method']
    cart = session.get('cart', [])

    if not cart or not mobile.isdigit() or len(mobile) != 10:
        flash("Invalid data or empty cart.", "error")
        return redirect('/dashboard')

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"bills/bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    total = sum(item['subtotal'] for item in cart)
    gst = total * 0.18
    discount = total * 0.10
    final = total + gst - discount

    c = canvas.Canvas(filename, pagesize=A4)
    y = A4[1] - 50
    c.setFont("DejaVu", 16)
    c.drawString(200, y, "The King's Grocery")
    y -= 30
    c.setFont("DejaVu", 12)
    c.drawString(50, y, f"Date: {now}")
    y -= 20
    c.drawString(50, y, f"Customer: {name}")
    y -= 20
    c.drawString(50, y, f"Mobile: {mobile}")
    y -= 20
    c.drawString(50, y, f"Payment Method: {payment}")
    y -= 30
    c.drawString(50, y, "ID  Name  Qty  Price  Subtotal")
    y -= 20

    for item in cart:
        line = f"{item['id']} {item['name'][:10]} {item['qty']} ₹{item['price']} ₹{item['subtotal']}"
        c.drawString(50, y, line)
        y -= 20

    y -= 20
    c.drawString(50, y, f"Total: ₹{total:.2f}")
    y -= 20
    c.drawString(50, y, f"GST: ₹{gst:.2f}")
    y -= 20
    c.drawString(50, y, f"Discount: ₹{discount:.2f}")
    y -= 20
    c.drawString(50, y, f"Final: ₹{final:.2f}")
    c.drawString(50, y - 40, "Thanks for shopping!")
    c.save()

    session.pop('cart', None)
    return send_file(filename, as_attachment=True)


@app.route('/products', methods=['GET', 'POST'])
def product_manager():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if not session.get('product_verified'):
        return redirect(url_for('product_auth'))
    # else:
    #     session.pop('product_verified')  # Ensure it's one-time access only

    # POST: Add / Update / Delete
    if request.method == 'POST':
        action = request.form.get("action")
        pid = request.form.get("id").strip()
        name = request.form.get("name").strip()
        price = request.form.get("price").strip()

        products = load_products_list()

        if action == "Add":
            for p in products:
                if p["id"] == pid:
                    flash("Product ID already exists!", "error")
                    return redirect("/products")
            products.append({"id": pid, "name": name, "price": price})
            save_products_list(products)
            flash("Product added!", "success")

        elif action == "Update":
            for p in products:
                if p["id"] == pid:
                    p["name"] = name
                    p["price"] = price
                    save_products_list(products)
                    flash("Product updated!", "success")
                    break
            else:
                flash("Product not found.", "error")

        elif action == "Delete":
            products = [p for p in products if p["id"] != pid]
            save_products_list(products)
            flash("Product deleted!", "success")

        return redirect("/products")

    # GET: With search
    search_term = request.args.get("search", "").lower()
    all_products = load_products_list()
    if search_term:
        filtered_products = [p for p in all_products if search_term in p["name"].lower()]
    else:
        filtered_products = all_products

    return render_template("products.html", products=filtered_products, search=search_term)

@app.route('/product-auth', methods=['GET', 'POST'])
def product_auth():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        admin_password = request.form.get('admin_password')
        if admin_password == "jatin123":
            session['product_verified'] = True
            return redirect(url_for('product_manager'))
        else:
            flash("Incorrect admin password.", "danger")

    return render_template('product_auth.html')

from flask import jsonify

@app.route('/update_product', methods=['POST'])
@login_required
def update_product():
    if not session.get('product_access'):
        return jsonify({'status': 'unauthorized'}), 401

    data = request.get_json()
    pid = data.get('id')
    name = data.get('name')
    price = data.get('price')

    if not pid or not name or not price:
        return jsonify({'status': 'error', 'message': 'Missing fields'}), 400

    products = load_products_list()

    for p in products:
        if p['id'] == pid:
            p['name'] = name
            try:
                p['price'] = str(float(price))
            except ValueError:
                return jsonify({'status': 'error', 'message': 'Invalid price'}), 400

            save_products_list(products)
            return jsonify({'status': 'success'})

    return jsonify({'status': 'error', 'message': 'Product not found'}), 404


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
