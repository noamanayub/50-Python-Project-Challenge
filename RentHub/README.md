# RentHub - Rental Marketplace

A complete rental marketplace website where users can rent anything from vehicles to electronics, similar to Amazon, eBay, and Daraz.

## Features

- **Complete Marketplace**: Browse and rent items from various categories
- **User Authentication**: Sign up, sign in, and manage your account
- **Product Management**: Detailed product pages with images, specifications, and reviews
- **Shopping Cart**: Add items to cart with rental period selection
- **Checkout Process**: Complete checkout with delivery options and payment methods
- **User Dashboard**: Manage orders, wishlist, profile settings, and more
- **Categories**: Vehicles, Electronics, Tools, Furniture, Sports, and more
- **Review System**: Leave reviews and ratings for rented items
- **Wishlist**: Save favorite items for later

## Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Font Awesome 6.4.0 for icons
- Responsive design

**Backend:**
- Django 5.0 (Python web framework)
- SQLite database
- Django templating engine (Jinja2 syntax)

## Brand Colors

- Primary: #b21900 (Red)
- Secondary: #173641 (Teal)
- Background: White

## Project Structure

```
website/
├── assest/
│   └── logo/                  # Logo files
├── backend/
│   ├── renthub/              # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py       # Project configuration
│   │   ├── urls.py           # Main URL routing
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── core/                 # Main Django app
│   │   ├── __init__.py
│   │   ├── admin.py          # Admin panel configuration
│   │   ├── apps.py
│   │   ├── models.py         # Database models
│   │   ├── views.py          # View functions
│   │   └── urls.py           # App URL patterns
│   ├── manage.py             # Django management script
│   └── requirements.txt      # Python dependencies
└── frontend/
    ├── templates/            # Django HTML templates
    │   ├── layout.html       # Base template with header/footer
    │   ├── index.html        # Homepage
    │   ├── register/         # Authentication pages
    │   ├── cart/             # Shopping cart
    │   ├── product-detail/   # Product details
    │   ├── account/          # User dashboard
    │   └── checkout/         # Checkout process
    ├── static/               # Static files (CSS, JS, images)
    │   ├── css/
    │   ├── js/
    │   └── logo/
    └── template/             # Original HTML templates
```

## Installation

1. **Install Python** (3.10 or higher recommended)

2. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

3. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate    # On Windows
   source venv/bin/activate # On Mac/Linux
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the website:**
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Database Models

- **Category**: Product categories with icons
- **Product**: Rental items with pricing, images, and specifications
- **ProductImage**: Multiple images for products
- **Order**: Rental orders with delivery details
- **OrderItem**: Individual items in orders
- **Review**: Product reviews and ratings
- **Wishlist**: User's saved items
- **UserProfile**: Extended user information

## Usage

### Admin Panel
1. Access admin at `/admin/`
2. Add categories with Font Awesome icon classes
3. Create products with details and images
4. Manage orders and reviews

### User Features
- Browse products by category
- Search for items
- View detailed product information
- Add items to cart with rental periods
- Complete checkout process
- Manage account and orders
- Leave reviews and ratings
- Save items to wishlist

## Development Notes

- All templates extend `layout.html` base template
- Static files are served from `frontend/static/`
- Logos are stored in `assest/logo/` directory
- Brand colors are defined in CSS custom properties
- Cart functionality uses localStorage on frontend
- Django handles backend data and user authentication

## Next Steps

1. Configure email settings for notifications
2. Integrate payment gateway
3. Add image upload functionality for products
4. Implement search filtering
5. Add real-time availability calendar
6. Create mobile app version
7. Add messaging system between renters and owners

## License

All rights reserved © 2024 RentHub
