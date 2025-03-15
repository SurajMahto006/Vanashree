import os
import json
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
YOUR_DOMAIN = "http://localhost:5000"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///vanashree.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load product data
with open('static/data/products.json', 'r') as f:
    products = json.load(f)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

@app.route('/')
def index():
    featured_products = products[:4]  # First 4 products as featured
    return render_template('index.html', featured_products=featured_products)

@app.route('/products')
def product_list():
    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return redirect(url_for('product_list'))

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    try:
        cart_items = request.json.get('items', [])
        line_items = []

        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': int(float(item['price']) * 100),  # Convert to paisa
                    'product_data': {
                        'name': item['name'],
                        'description': item['description'],
                        'images': [item['image']],
                    },
                },
                'quantity': item['quantity'],
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 403

@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            remember = bool(request.form.get('remember'))

            app.logger.debug(f"Login attempt for email: {email}")

            # Validate input fields
            if not email:
                flash('Email is required', 'danger')
                return redirect(url_for('login'))
            if not password:
                flash('Password is required', 'danger')
                return redirect(url_for('login'))

            # Check email format
            if '@' not in email or '.' not in email:
                flash('Please enter a valid email address', 'danger')
                return redirect(url_for('login'))

            user = User.query.filter_by(email=email).first()
            app.logger.debug(f"User found: {bool(user)}")

            if user:
                password_check = user.check_password(password)
                app.logger.debug(f"Password check result: {password_check}")

                if password_check:
                    login_user(user, remember=remember)
                    app.logger.debug(f"User {email} logged in successfully")
                    flash('Welcome back, ' + user.username + '!', 'success')
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('index'))
                else:
                    app.logger.debug("Password verification failed")
                    flash('Invalid password. Please try again.', 'danger')
            else:
                app.logger.debug("User not found")
                flash('No account found with this email. Please register first.', 'danger')

            return redirect(url_for('login'))
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            app.logger.debug(f"Registration attempt for email: {email}")

            if not username or not email or not password:
                flash('Please fill in all fields', 'danger')
                return redirect(url_for('register'))

            # Check if username already exists
            if User.query.filter_by(username=username).first():
                flash('Username already taken', 'danger')
                return redirect(url_for('register'))

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))

            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            app.logger.debug(f"Successfully registered user: {email}")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # In a real app, you would send this to an email service
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

# Initialize database
with app.app_context():
    db.create_all()
    app.logger.debug("Database tables created")