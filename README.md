# VANASHREE - Plant E-commerce Website

A beautiful e-commerce website for selling plants, built with Flask and Bootstrap.

## Getting Started

### 1. Install Required Software

Download and install these programs:

- [Python 3.11 or higher](https://www.python.org/downloads/)
  - During installation, make sure to check "Add Python to PATH"
  - Click "Install Now" for the recommended installation
- [Git](https://git-scm.com/downloads)
  - Use all default options during installation
- [Visual Studio Code](https://code.visualstudio.com/) (recommended editor)

### 2. Download the Project

Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
# Clone the project
git clone https://github.com/your-username/vanashree.git

# Go to project folder
cd vanashree
```

### 3. Install Required Packages

In the same Command Prompt/Terminal window:

```bash
# Install all required packages
pip install flask flask-login flask-sqlalchemy flask-wtf email-validator gunicorn psycopg2-binary
```

### 4. Run the Website

Still in Command Prompt/Terminal:

```bash
# Set the Flask application
# For Windows:
set FLASK_APP=main.py

# For Mac/Linux:
export FLASK_APP=main.py

# Run the application
python main.py
```

Open your web browser and go to: http://localhost:5000

## Project Structure

```
vanashree/
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   ├── js/
│   │   ├── cart.js          # Shopping cart functionality
│   │   ├── checkout.js      # Checkout process
│   │   └── products.js      # Product display and filtering
│   └── data/
│       └── products.json    # Product information
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   ├── products.html       # Product listing
│   ├── cart.html          # Shopping cart
│   ├── checkout.html      # Checkout page
│   ├── login.html         # Login page
│   └── register.html      # Registration page
├── app.py                 # Main application logic
├── main.py               # Application entry point
└── models.py             # Database models
```

## Making Changes

### 1. Modifying Products

Edit `static/data/products.json` to:
- Add new products
- Change prices
- Update descriptions
- Change product images

Example product format:
```json
{
    "id": 1,
    "name": "Plant Name",
    "price": 999,
    "description": "Plant description",
    "image": "https://example.com/image.jpg",
    "category": "Indoor Plants"
}
```

### 2. Changing Styles

Edit `static/css/style.css` to modify:
- Colors
- Fonts
- Layouts
- Spacing

### 3. Modifying Pages

HTML templates are in the `templates` folder:
- Edit `templates/index.html` for homepage changes
- Modify `templates/products.html` for product listing layout
- Update `templates/cart.html` for shopping cart changes

### 4. Adding Features

Main application logic is in:
- `app.py` - Routes and server-side logic
- `models.py` - Database models
- JavaScript files in `static/js/` for client-side features

## Common Issues

1. **"Module not found" errors**
   - Make sure you installed all packages using pip
   - Check if you're in the correct folder

2. **Database errors**
   - Delete the `vanashree.db` file and restart the application
   - It will be recreated automatically

3. **Images not showing**
   - Check internet connection
   - Verify image URLs in products.json

4. **Page not found (404)**
   - Make sure the application is running
   - Check if you're using the correct URL (http://localhost:5000)

## Need Help?

If you encounter any issues:
1. Check the error message in the Command Prompt/Terminal
2. Make sure all required packages are installed
3. Verify all files are in the correct folders
4. Try restarting the application
