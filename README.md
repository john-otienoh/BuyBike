# 🚴 BikeShop — Production-Ready Django eCommerce Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

A fully featured, production-grade bicycle eCommerce store built with Django 6.0.2. Includes everything from product browsing, cart management, and order tracking to a full admin panel — awaiting only your payment provider of choice.

</div>

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Feature Summary](#2-feature-summary)
3. [Technology Stack](#3-technology-stack)
4. [Project Structure](#4-project-structure)
5. [Data Models](#5-data-models)
6. [URL Routes Reference](#6-url-routes-reference)
7. [Prerequisites](#7-prerequisites)
8. [Installation — Local Development](#8-installation--local-development)
9. [Environment Variables](#9-environment-variables)
10. [Database Setup and Migrations](#10-database-setup-and-migrations)
11. [Seeding Sample Data](#11-seeding-sample-data)
12. [Running the Development Server](#12-running-the-development-server)
13. [Admin Panel Guide](#13-admin-panel-guide)
14. [Authentication System](#14-authentication-system)
15. [Shopping Cart Behaviour](#15-shopping-cart-behaviour)
16. [Checkout and Order Flow](#16-checkout-and-order-flow)
17. [Payment Integration Guide](#17-payment-integration-guide)
18. [Static and Media Files](#18-static-and-media-files)
19. [Deployment to Production](#19-deployment-to-production)
20. [Deployment: PythonAnywhere](#20-deployment-pythonanywhere)
21. [Deployment: Railway and Render](#21-deployment-railway-and-render)
22. [Deployment: VPS with Ubuntu Nginx and Gunicorn](#22-deployment-vps-with-ubuntu-nginx-and-gunicorn)
23. [Security Hardening Checklist](#23-security-hardening-checklist)
24. [Customisation Guide](#24-customisation-guide)
25. [Management Commands](#25-management-commands)
26. [Troubleshooting](#26-troubleshooting)
27. [Contributing](#27-contributing)
28. [License](#28-license)

---

## 1. Project Overview

BikeShop is a full-stack Django eCommerce application designed around a premium bicycle retail experience. The project is architected to be maintainable, extensible, and immediately deployable. It follows Django best practices throughout — class-based views, a custom context processor system, model-level business logic via `@property` methods, and a multiple-app structure that keeps the codebase navigable.

The key design decisions are:

**Single Django app** (`store`) — keeps imports and navigation simple for a project of this scope.

**Session and auth cart merging** — guest carts persist in the session and merge automatically when a user logs in, so no items are ever lost at login.

**Order snapshots** — product names, SKUs, and prices are copied into `OrderItem` at checkout time so historical orders remain accurate even if products are later edited or deleted.

**Payment-provider agnostic** — the checkout flow creates and stores the order, then redirects to a dedicated payment view. You wire in any provider (Stripe, Razorpay, PayPal, M-Pesa) without touching the rest of the flow.

**Real Unsplash images via seed command** — running `python manage.py seed_data` downloads and stores product images, category images, and banner images automatically using Python's built-in `urllib.request` — no API key required.

---

## 2. Feature Summary

### Storefront

| Feature | Details |
|---|---|
| Hero carousel | Full-width banner slides with image, title, subtitle, CTA button, and configurable display order |
| Category browsing | Hierarchical categories (parent to children), each with image and slug-based URLs |
| Product catalog | Filterable by category, brand, bike type, price range, and condition; sortable by price, date, rating, and popularity |
| Full-text search | Searches name, description, brand name, and category name simultaneously |
| Product detail | Multi-image gallery with thumbnail switcher, variant selector, star rating summary, specification table, and related products grid |
| Product reviews | Star rating 1 to 5, title and body fields; verified-purchase badge; admin approval queue |
| Wishlist | Toggle add/remove via AJAX; persisted per user account; count shown live in navbar badge |
| Brand showcase | Brand logos on homepage with greyscale to colour hover effect |
| Newsletter | Email subscription with duplicate-safe upsert and active/inactive flag |

### Cart and Checkout

| Feature | Details |
|---|---|
| Guest cart | Session-keyed cart — no login required to browse and add items |
| Cart merging | Guest cart merges into user cart automatically on login |
| AJAX add-to-cart | Uses fetch() to add items and update badge count without page reload |
| Quantity controls | Plus and minus buttons with stock-capped maximum |
| Coupon codes | Percentage-off, fixed-amount, or free-shipping types with expiry dates and use-count limits |
| Shipping methods | Standard (free), Express ($15), Overnight ($35) with real-time total update via JavaScript |
| Saved addresses | Checkout pre-fills from the user's default shipping address |
| Order notes | Optional free-text field recorded on each order |

### Orders and Account

| Feature | Details |
|---|---|
| Order lifecycle | 8 statuses: Pending, Confirmed, Processing, Shipped, Out for Delivery, Delivered, Cancelled, Refunded |
| Payment statuses | Unpaid, Paid, Partially Refunded, Refunded, Failed |
| Status history | Every status change is logged with a timestamp and the actor who made it |
| Order tracking | Tracking number and carrier fields on each order |
| Account dashboard | Summary stats (total orders, wishlist count, review count) plus recent orders |
| Address book | Multiple saved addresses per user with a default flag per address type |
| Profile editing | Name, email, phone number, avatar, bio, date of birth, newsletter opt-in toggle |
| Password change | Authenticated change using Django's PasswordChangeForm with session re-auth |

### Admin Panel

| Feature | Details |
|---|---|
| Product admin | Inline images and variants; live-editable price, stock, and availability from the list view |
| Order admin | Inline order items and status history; status changes are auto-logged with the acting admin user |
| Review moderation | Bulk approve and reject actions |
| Coupon management | Full CRUD with real-time use-count tracking |
| Banner management | Orderable slides with active toggle and image upload |

---

## 3. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Language | Python | 3.10 or higher | Application logic |
| Framework | Django | 4.2.x | Web framework, ORM, admin |
| Frontend CSS | Bootstrap | 5.3.2 | Responsive grid and UI components |
| Frontend Icons | Bootstrap Icons | 1.11.3 | Icon set loaded from CDN |
| Fonts | Google Fonts Inter | latest | UI typography loaded from CDN |
| Forms | django-crispy-forms | 2.1 | Form rendering helper |
| Forms | crispy-bootstrap5 | 0.7 | Bootstrap 5 template pack for crispy |
| Static files | WhiteNoise | 6.6.0 | Serves compressed static files in production |
| Configuration | python-decouple | 3.8 | Reads settings from .env file |
| Images | Pillow | 10.2.0 | ImageField processing and validation |
| Database (dev) | SQLite | built-in | Zero-config development database |
| Database (prod) | PostgreSQL | 14 or higher | Recommended production database |
| Web server (prod) | Gunicorn | 21 or higher | WSGI application server |
| Reverse proxy (prod) | Nginx | 1.24 or higher | Static file serving and SSL termination |

---

## 4. Project Structure

```
BuyBike/
│
├── manage.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
├── config/                     # Project configuration (core settings)
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py            # Shared settings
│   │   ├── development.py     # Dev environment
│   │   ├── production.py      # Prod environment
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                      # All domain apps live here
│   ├── __init__.py
│
│   ├── accounts/              # Auth & user management
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── signals.py
│   │   └── admin.py
│
│   ├── products/              # Catalog system
│   │   ├── models.py          # Product, Category, Review
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── filters.py         # Filtering logic
│   │   ├── services.py        # Business logic
│   │   └── admin.py
│
│   ├── cart/                  # Shopping cart logic
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── services.py
│   │   └── context_processors.py
│
│   ├── orders/                # Order lifecycle
│   │   ├── models.py          # Order, OrderItem
│   │   ├── services.py
│   │   ├── signals.py
│   │   └── admin.py
│
│   ├── checkout/              # Checkout orchestration
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── services.py
│
│   ├── payments/              # Payment abstraction layer
│   │   ├── gateways/
│   │   │   ├── stripe.py
│   │   │   ├── mpesa.py
│   │   ├── services.py
│   │   └── webhooks.py
│
│   ├── core/                  # Shared utilities
│   │   ├── models.py          # Base models (timestamps, etc.)
│   │   ├── utils.py
│   │   ├── mixins.py
│   │   └── constants.py
│
│   └── marketing/             # Newsletter, SEO, engagement
│       ├── models.py
│       ├── views.py
│       └── services.py
│
├── templates/                 # Global templates
│   ├── base.html
│   ├── includes/
│   ├── products/
│   ├── cart/
│   ├── checkout/
│   └── accounts/
│
static/
|   ├── images/
│   │   └── logo.png                       Source static files collected to staticfiles/ for production
│   ├── css/
│   │   └── main.css               Custom design system using CSS variables
│   └── js/
│       └── main.js          
│
└── media/                         
|    ├── products/                  Product images
|    ├── categories/                Category images
|    ├── banners/                   Hero carousel banner images
|    ├── brands/                    Brand logo images
|    └── avatars/ 
|
├── infrastructure/            # DevOps / deployment
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── nginx/
│   └── scripts/
│
└── tests/                     # Centralized tests (optional)
    ├── test_products.py
    ├── test_cart.py
    └── test_checkout.py
```

---

## 5. Data Models

There are 14 models across three conceptual groups.

### Catalogue Models

**Category** — Hierarchical categories using a self-referential parent foreign key. The slug is auto-generated from the name on first save. Each category has an optional image and an `is_active` flag.

**Brand** — Manufacturer record with logo, country of origin, and website URL. Products link to brands via a nullable foreign key.

**Product** — The central model. Key fields and their purposes:

| Field | Type | Notes |
|---|---|---|
| sku | CharField | Auto-generated UUID prefix if left blank |
| slug | SlugField | Auto-generated from name; used in all product URLs |
| bike_type | CharField | 11 choices: mountain, road, electric, bmx, gravel, kids, cruiser, folding, accessories, clothing, other |
| price | DecimalField | Current selling price |
| compare_price | DecimalField | Struck-through original price; drives the discount_percentage property |
| stock | PositiveIntegerField | Decremented on confirmed order; triggers low-stock warning when at threshold |
| specifications | JSONField | Arbitrary key-value pairs rendered as a spec table on the product detail page |
| is_featured | BooleanField | Controls inclusion in the Featured Bikes section on the homepage |
| is_new_arrival | BooleanField | Controls inclusion in the New Arrivals section on the homepage |
| views_count | PositiveIntegerField | Incremented via a non-locking UPDATE on each product detail page view |

Computed properties on Product: `is_in_stock`, `is_low_stock`, `discount_percentage`, `average_rating`, `review_count`, `primary_image`.

**ProductImage** — One-to-many images per product. Setting `is_primary=True` on one image clears the flag on all others for that product via pre-save logic.

**ProductVariant** — Handles size, colour, or spec variants. Each variant has independent stock and a `price_modifier` (positive or negative) added to the base product price.

**Review** — User reviews linked to both a product and a user. A `unique_together` constraint prevents duplicate reviews from the same user on the same product. `is_verified_purchase` is set automatically at submission time by checking whether the user has a paid order containing this product.

### Commerce Models

**Cart** — Dual-mode cart: authenticated users have the `user` field set; guests have `session_key` set. On login, the `get_or_create_cart()` helper merges all guest `CartItem` records into the user's cart.

**CartItem** — A `unique_together` constraint on `(cart, product, variant)` prevents duplicate line items. Adding the same product again increments the quantity instead.

**Coupon** — Three discount types: percentage, fixed, free_shipping. The `is_valid` property checks active status, date window, and use count atomically.

**Order** — Stores a full denormalised snapshot of the shipping address (not a foreign key to Address) so address edits or deletions never corrupt historical order records. Auto-generates a unique order number with prefix BS followed by 8 random digits.

**OrderItem** — Denormalised snapshot of product name, SKU, variant name, and unit price at checkout time. The product foreign key is SET_NULL so deleting a product does not cascade-delete historical order records.

**OrderStatusHistory** — Append-only log. The admin automatically creates a history entry whenever an order's status field is changed and saved.

### User Models

**UserProfile** — One-to-one extension of Django's built-in User model. Adds avatar, phone, date of birth, bio, and newsletter opt-in. Created automatically inside `RegisterView.post()`.

**Address** — Multiple addresses per user with `address_type` (billing or shipping) and `is_default` flag. Setting an address as default clears the flag on all others of the same type via pre-save logic.

**Wishlist** — One-to-one with User using a ManyToManyField to Product. Created on first use via `get_or_create`.

**NewsletterSubscriber** — Stores email with an `is_active` flag. Re-subscribing a known email sets it active rather than raising a duplicate error.

**Banner** — Homepage hero carousel slides. Configurable title, subtitle, image, link, CTA text, and display order integer.

---

## 6. URL Routes Reference

All routes are under the `store` app namespace. Use them in templates as `{% url 'store:name' %}`.

| Name | Path | Auth Required |
|---|---|---|
| store:home | / | No |
| store:about | /about/ | No |
| store:contact | /contact/ | No |
| store:product_list | /products/ | No |
| store:product_list_by_category | /products/category/slug/ | No |
| store:product_detail | /products/slug/ | No |
| store:add_review | /products/slug/review/ | Yes |
| store:search | /search/ | No |
| store:cart | /cart/ | No |
| store:add_to_cart | /cart/add/id/ | No |
| store:update_cart | /cart/update/id/ | No |
| store:remove_from_cart | /cart/remove/id/ | No |
| store:apply_coupon | /cart/apply-coupon/ | No |
| store:checkout | /checkout/ | No |
| store:order_success | /checkout/success/order_number/ | No |
| store:order_list | /orders/ | Yes |
| store:order_detail | /orders/order_number/ | Yes |
| store:wishlist | /wishlist/ | Yes |
| store:toggle_wishlist | /wishlist/toggle/id/ | Yes |
| store:register | /register/ | No |
| store:login | /login/ | No |
| store:logout | /logout/ | Yes |
| store:account | /account/ | Yes |
| store:profile | /account/profile/ | Yes |
| store:address_list | /account/addresses/ | Yes |
| store:address_create | /account/addresses/add/ | Yes |
| store:address_update | /account/addresses/pk/edit/ | Yes |
| store:address_delete | /account/addresses/pk/delete/ | Yes |
| store:change_password | /account/change-password/ | Yes |
| store:newsletter_subscribe | /newsletter/subscribe/ | No |
| store:payment_initiate | /payment/initiate/order_number/ | No |
| store:payment_callback | /payment/callback/ | No |
| store:payment_webhook | /payment/webhook/ | No |

The Django admin is available at `/admin/`.

---

## 7. Prerequisites

Ensure the following are installed on your machine before proceeding.

| Requirement | Minimum Version | How to Check |
|---|---|---|
| Python | 3.10 | `python3 --version` |
| pip | 23 or higher | `pip --version` |
| git | 2.x | `git --version` |
| venv | built into Python 3 | `python3 -m venv --help` |

Optional but recommended for production deployments: PostgreSQL 14+, Nginx 1.24+, Certbot for Let's Encrypt SSL.

---

## 8. Installation — Local Development

Follow each step in order. Do not skip the virtual environment step.

### Step 1 — Obtain the source code

Clone from GitHub:
```bash
git clone https://github.com/your-username/bikeshop.git
cd bikeshop
```

Or from a zip file:
```bash
unzip bikeshop.zip
cd bikeshop
```

### Step 2 — Create a virtual environment

```bash
python3 -m venv venv
```

### Step 3 — Activate the virtual environment

macOS and Linux:
```bash
source venv/bin/activate
```

Windows Command Prompt:
```cmd
venv\Scripts\activate.bat
```

Windows PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

Your shell prompt should now show `(venv)` confirming activation.

### Step 4 — Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs Django 4.2.9, Pillow, django-crispy-forms, crispy-bootstrap5, python-decouple, and whitenoise.

### Step 5 — Create your environment file

```bash
cp .env.example .env
```

Open `.env` in a text editor. At minimum you must set `SECRET_KEY`. Generate one now:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it into `.env` after `SECRET_KEY=`. Save the file.

### Step 6 — Apply database migrations

```bash
python manage.py migrate
```

You will see each migration being applied, ending with `Applying store.0001_initial... OK`.

### Step 7 — Seed sample data

```bash
python manage.py seed_data
```

This creates 8 categories, 8 brands, 12 products with real Unsplash photos, 3 banner slides, and 2 coupon codes.

### Step 8 — Create an admin superuser

```bash
python manage.py createsuperuser
```

Enter a username, email address, and password when prompted.

### Step 9 — Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser. The store is running.

---

## 9. Environment Variables

All configuration is read from the `.env` file by `python-decouple`. Never commit your `.env` file to version control — it is listed in `.gitignore`.

| Variable | Required | Default | Description |
|---|---|---|---|
| SECRET_KEY | Yes | none | Django cryptographic secret. Must be unique and kept private. |
| DEBUG | No | True | Set to False in production. Disables error pages and enables security headers. |
| ALLOWED_HOSTS | Production | localhost,127.0.0.1 | Comma-separated list of hostnames Django will serve. |
| EMAIL_HOST | No | smtp.gmail.com | SMTP server hostname. |
| EMAIL_PORT | No | 587 | SMTP server port. |
| EMAIL_HOST_USER | No | empty | SMTP login username. |
| EMAIL_HOST_PASSWORD | No | empty | SMTP login password or app-specific password. |
| DEFAULT_FROM_EMAIL | No | noreply@bikeshop.com | The From address on all outgoing emails. |
| PAYMENT_PROVIDER | No | stripe | Informational label. Set to stripe, razorpay, or paypal. |
| STRIPE_PUBLIC_KEY | For Stripe | empty | Publishable key from your Stripe dashboard, starts with pk_. |
| STRIPE_SECRET_KEY | For Stripe | empty | Secret key from your Stripe dashboard, starts with sk_. |
| STRIPE_WEBHOOK_SECRET | For Stripe | empty | Webhook signing secret from your Stripe dashboard, starts with whsec_. |

---

## 10. Database Setup and Migrations

The project uses SQLite by default. No database software installation is needed for local development.

### Standard migration commands

```bash
python manage.py makemigrations   # Generate new migration files after model changes
python manage.py migrate          # Apply pending migrations to the database
```

### Switching to PostgreSQL

Install the Python adapter:
```bash
pip install psycopg2-binary
```

Create the database and user in psql:
```sql
CREATE DATABASE bikeshop_db;
CREATE USER bikeshop_user WITH PASSWORD 'your_strong_password';
ALTER ROLE bikeshop_user SET client_encoding TO 'utf8';
ALTER ROLE bikeshop_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE bikeshop_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE bikeshop_db TO bikeshop_user;
\q
```

Update `config/settings.py` to replace the DATABASES block:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='bikeshop_db'),
        'USER': config('DB_USER', default='bikeshop_user'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

Add the four new variables to `.env`, then run `python manage.py migrate` again.

---

## 11. Seeding Sample Data

The `seed_data` management command creates realistic sample content and optionally downloads real product images from Unsplash.

```bash
# Full seed with image downloads — requires internet access
python manage.py seed_data

# Skip image downloads for faster setup or offline environments
python manage.py seed_data --no-images
```

The command is idempotent — running it multiple times will not create duplicate records because it uses `get_or_create` throughout.

### What gets created

| Entity | Count | Examples |
|---|---|---|
| Categories | 8 | Mountain Bikes, Road Bikes, Electric Bikes, BMX and Dirt, Kids Bikes, Accessories |
| Brands | 8 | Trek, Giant, Specialized, Cannondale, Scott, Cube, Shimano, SRAM |
| Products | 12 | Trek Marlin 7, Giant Fathom 29, Trek Allant+ 7 e-bike, Shimano XT groupset, MIPS helmet |
| Banners | 3 | Ride the Mountain, Electric Revolution, Road Season is Here |
| Coupons | 2 | WELCOME10 gives 10% off orders over $50. SAVE50 gives $50 off orders over $300. |

### How image downloading works

Each entity has a hardcoded Unsplash URL pointing to a specific photo at a defined resolution. The seed command uses Python's built-in `urllib.request` to fetch the image bytes and then calls Django's `ImageField.save()` to write the file into the correct `media/` subdirectory. If a download fails due to a network issue or timeout, the command logs the failure and continues — it never crashes on a bad image URL.

---

## 12. Running the Development Server

### Start the server

```bash
python manage.py runserver
```

### Useful URLs

| URL | Description |
|---|---|
| http://127.0.0.1:8000/ | Storefront homepage |
| http://127.0.0.1:8000/admin/ | Django admin panel |
| http://127.0.0.1:8000/products/ | Full product catalog |
| http://127.0.0.1:8000/register/ | New account registration |
| http://127.0.0.1:8000/login/ | Login with username or email |
| http://127.0.0.1:8000/account/ | Account dashboard |

### Running on a different host or port

```bash
python manage.py runserver 0.0.0.0:8080
```

---

## 13. Admin Panel Guide

Access the admin panel at `http://127.0.0.1:8000/admin/` with your superuser credentials.

### Products

The product list view has live-editable columns for price, stock, is_available, and is_featured — you can update these without opening the full edit form. Click any product name to open the detail form which includes:

- **Inline Images** — Upload multiple images. Tick the Is Primary checkbox on the image you want to show as the gallery hero. The pre-save signal ensures only one image per product can have is_primary set.
- **Inline Variants** — Add size, colour, or spec variants. Each variant has its own stock count and a price modifier that is added to (or subtracted from) the base product price.
- **Specifications** — Enter as a JSON object such as `{"Frame": "Aluminum", "Gears": "21-speed"}`. This renders as a table on the product detail page.

### Orders

Changing the Status dropdown on any order and saving it will automatically create an `OrderStatusHistory` record attributed to the currently logged-in admin user. Fill in Tracking Number and Carrier when shipping an order. Admin Notes is an internal field not shown to customers.

### Reviews

Navigate to Store then Reviews. Use the Approve Selected Reviews bulk action to make reviews visible on product pages. Rejected or pending reviews are hidden from customers.

### Coupons

Set valid_from and valid_to to control the active date window. Leave max_uses blank for unlimited uses. The current_uses counter is automatically incremented each time a coupon is successfully applied at checkout.

### Banners

The Order integer field controls the position of each slide in the homepage carousel. Lower numbers appear first.

---

## 14. Authentication System

### Registration

The registration form at `/register/` collects exactly four fields:

1. Username — must be unique across the entire site
2. Email — validated for format and uniqueness across the site; used for login and future notifications
3. Password — subject to Django's four built-in validators
4. Confirm Password — must match the password field exactly

On successful submission, a UserProfile record is created automatically and the user is logged in immediately and redirected to the homepage.

### Login

The login form at `/login/` accepts either a username or an email address in a single combined field. The resolution logic works as follows:

First, Django's `authenticate()` is called with the submitted value as the username. This succeeds immediately if the user typed their actual username.

If that returns None, the code queries `User.objects.get(email__iexact=identifier)` to find the real username associated with that email address, then calls `authenticate()` again with the resolved username.

If both attempts fail, a non-field error is added to the form and the login page is re-rendered.

The Remember Me checkbox controls session lifetime. If unchecked, `request.session.set_expiry(0)` is called, which makes the session expire when the browser is closed rather than persisting for 30 days.

### Logout

Logout requires an HTTP POST request submitted via a form with a CSRF token. This prevents CSRF-based forced logout attacks. The logout button in both the navbar and the account sidebar submits this form correctly.

### Password Change

Authenticated users can change their password at `/account/change-password/`. After a successful change, `update_session_auth_hash(request, user)` is called to keep the current session valid so the user is not logged out.

---

## 15. Shopping Cart Behaviour

### Guest Carts

Adding an item to the cart does not require being logged in. When an anonymous user first adds a product, `request.session.create()` is called if no session exists. A `Cart` record is then created keyed by the `session_key`. The session cookie keeps this cart alive across page loads and browser restarts (subject to session cookie age settings).

### Authenticated Carts

Each logged-in user has at most one Cart record linked via a OneToOneField. `get_or_create_cart()` is called on every cart interaction to ensure this.

### Cart Merging on Login

When a user logs in after browsing as a guest, `get_or_create_cart()` detects an existing session-keyed cart and merges its items into the user's personal cart. If the same product and variant already exists in the user's cart, the quantities are summed up to the available stock limit. After merging, the guest cart record is deleted. This means users can add items before registering and never lose them.

### AJAX Add-to-Cart

Product cards and the product detail page use a form with the class `add-to-cart-form`. The JavaScript in `main.js` intercepts the form submit event, posts to the server via `fetch()` with the `X-Requested-With: XMLHttpRequest` header, and on a successful JSON response updates all `.cart-count-badge` elements and shows a toast notification — all without any page reload.

---

## 16. Checkout and Order Flow

The complete flow from cart to confirmed order follows these steps:

1. User reviews cart at `/cart/` and optionally applies a coupon code.
2. User clicks Proceed to Checkout and is taken to `/checkout/`.
3. The CheckoutForm collects contact information, shipping address, shipping method selection, and optional order notes.
4. On a valid POST, `CheckoutView.post()` executes inside a `transaction.atomic()` block. It creates the Order record, creates all OrderItem records with denormalised price snapshots, decrements stock for each product, and increments the coupon use counter.
5. The cart items are deleted and the session coupon key is cleared.
6. The user is redirected to `/payment/initiate/order_number/`.
7. You add your payment provider integration in `PaymentInitiateView` (see Section 17).
8. On successful payment, update the order: set `payment_status` to paid, `status` to confirmed, and `paid_at` to the current timestamp.
9. Redirect the user to `/checkout/success/order_number/`.

### Shipping cost options

```python
SHIPPING_RATES = {
    'standard':  0,   # Free shipping
    'express':   15,  # $15
    'overnight': 35,  # $35
}
```

These are defined at the top of `store/views.py` and can be edited directly.

---

## 17. Payment Integration Guide

The checkout creates the order before any payment occurs. The order sits in `status=pending` and `payment_status=unpaid` until your payment provider confirms success. You implement this by editing `store/views.py`.

### Stripe Integration

Install the Stripe library:
```bash
pip install stripe
```

Add to `.env`:
```
STRIPE_PUBLIC_KEY=pk_test_YOUR_KEY
STRIPE_SECRET_KEY=sk_test_YOUR_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET
```

Replace the body of `PaymentInitiateView.get()` with:
```python
import stripe
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': f'BikeShop Order #{order.order_number}'},
            'unit_amount': int(order.total * 100),
        },
        'quantity': 1,
    }],
    mode='payment',
    metadata={'order_number': order.order_number},
    success_url=request.build_absolute_uri(
        reverse('store:payment_callback')) + '?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=request.build_absolute_uri(
        reverse('store:order_detail', args=[order.order_number])),
)
return redirect(session.url)
```

Replace `PaymentCallbackView.get()` with:
```python
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
order = Order.objects.get(order_number=session.metadata['order_number'])

if session.payment_status == 'paid':
    order.payment_status = 'paid'
    order.status = 'confirmed'
    order.paid_at = timezone.now()
    order.payment_reference = session.payment_intent
    order.save()
    OrderStatusHistory.objects.create(order=order, status='confirmed')
    return redirect('store:order_success', order_number=order.order_number)

return redirect('store:order_detail', order_number=order.order_number)
```

For the webhook (reliable server-to-server confirmation), decorate `PaymentWebhookView` with `@method_decorator(csrf_exempt, name='dispatch')` and verify the Stripe signature:
```python
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class PaymentWebhookView(View):
    def post(self, request):
        payload = request.body
        sig = request.headers.get('Stripe-Signature', '')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return JsonResponse({'error': 'Invalid signature'}, status=400)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order = Order.objects.get(order_number=session['metadata']['order_number'])
            order.payment_status = 'paid'
            order.status = 'confirmed'
            order.paid_at = timezone.now()
            order.save()
        return JsonResponse({'status': 'ok'})
```

Register `https://yourdomain.com/payment/webhook/` in your Stripe dashboard under Developers then Webhooks.

### Razorpay Integration

```bash
pip install razorpay
```

In `PaymentInitiateView.get()`:
```python
import razorpay
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
rz_order = client.order.create({
    'amount': int(order.total * 100),
    'currency': 'INR',
    'receipt': order.order_number,
    'payment_capture': 1,
})
return render(request, self.template_name, {
    'order': order,
    'razorpay_order_id': rz_order['id'],
    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
})
```

In `payment/initiate.html`, add the Razorpay checkout widget:
```html
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<button onclick="openRazorpay()" class="btn btn-accent w-100 btn-lg">Pay Now</button>
<script>
function openRazorpay() {
  var rzp = new Razorpay({
    key: '{{ razorpay_key_id }}',
    amount: {{ order.total|floatformat:0 }}00,
    currency: 'INR',
    order_id: '{{ razorpay_order_id }}',
    name: 'BikeShop',
    description: 'Order #{{ order.order_number }}',
    handler: function(response) {
      window.location = '/payment/callback/?payment_id=' 
        + response.razorpay_payment_id + '&order={{ order.order_number }}';
    }
  });
  rzp.open();
}
</script>
```

### M-Pesa Integration (Safaricom Daraja — Kenya)

```bash
pip install daraja-py
```

Use the STK Push (Lipa Na M-Pesa Online) API to initiate payment from `PaymentInitiateView`. Register your callback URL at `/payment/webhook/` in the Safaricom Daraja portal. Obtain your Consumer Key, Consumer Secret, Shortcode, and Passkey from the Safaricom developer portal at `developer.safaricom.co.ke`.

### PayPal Integration

```bash
pip install paypalrestsdk
```

Create a PayPal order in `PaymentInitiateView`, redirect the user to the PayPal approval URL, then confirm and capture the payment in `PaymentCallbackView`. Refer to the official PayPal REST SDK documentation for complete code samples.

---

## 18. Static and Media Files

### Development

Django's development server automatically serves static files from the `static/` directory. Media files (user uploads and seed images) are served via the `static()` URL helper added to `config/urls.py`.

### Collecting Static Files for Production

```bash
python manage.py collectstatic --noinput
```

This copies all static files from `static/` and all installed app static directories into `staticfiles/`. WhiteNoise serves these files with compression and cache-busting headers directly from the Django process.

### Media Files in Production

Django does not serve media files in production. You have two options:

**Nginx approach** — Add a location block to your Nginx configuration:
```nginx
location /media/ {
    alias /home/ubuntu/bikeshop/media/;
    expires 7d;
}
```

**Cloud storage approach** — For platforms like Heroku, Railway, or Render where the filesystem is ephemeral, install `django-storages` and configure an S3-compatible bucket or Cloudinary to store media files persistently across deployments.

---

## 19. Deployment to Production

Before deploying to any environment, complete this checklist:

- Set `DEBUG=False` in `.env`
- Set `ALLOWED_HOSTS` to your actual domain or IP address
- Generate a fresh `SECRET_KEY` — never reuse the development key
- Configure PostgreSQL as the database backend
- Run `python manage.py collectstatic`
- Set real SMTP credentials for email sending
- Add payment provider API keys
- Ensure the `media/` directory is writable by the web server process

---

## 20. Deployment: PythonAnywhere

PythonAnywhere offers a free tier suitable for hobby projects and a paid tier for production traffic.

### Upload code

Upload the zip via the PythonAnywhere Files tab, or clone from GitHub in a Bash console:
```bash
git clone https://github.com/your-username/bikeshop.git ~/bikeshop
```

### Create virtual environment and install dependencies

```bash
cd ~/bikeshop
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary
```

### Configure the WSGI file

In the PythonAnywhere Web tab, set the WSGI configuration file path, then edit it to contain:
```python
import os, sys
path = '/home/yourusername/bikeshop'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Set environment variables

In the Web tab under Environment Variables, add each key-value pair from your `.env` file.

### Configure static and media file serving

In the Web tab under Static Files, add two mappings:

| URL | Directory |
|---|---|
| /static/ | /home/yourusername/bikeshop/staticfiles/ |
| /media/ | /home/yourusername/bikeshop/media/ |

Then run:
```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

Click Reload in the Web tab. Your site is live.

---

## 21. Deployment: Railway and Render

Both platforms support Django with minimal configuration files.

### Procfile

Create a file named `Procfile` in the project root:
```
web: gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2
```

Install Gunicorn and save it to requirements:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### runtime.txt

Create a file named `runtime.txt` in the project root:
```
python-3.11.0
```

### Environment Variables

Set these in the Railway or Render dashboard:
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
DATABASE_URL=postgresql://...
```

Railway automatically injects `DATABASE_URL` if you add a PostgreSQL plugin to your project. Update `settings.py` to parse it using `dj-database-url`.

### Build Command for Render

In the Render dashboard under Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

---

## 22. Deployment: VPS with Ubuntu Nginx and Gunicorn

This is the most flexible production setup.

### System dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.10 python3.10-venv python3-pip nginx postgresql postgresql-contrib -y
```

### PostgreSQL setup

```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE bikeshop_db;
CREATE USER bikeshop_user WITH PASSWORD 'strong_unique_password';
ALTER ROLE bikeshop_user SET client_encoding TO 'utf8';
ALTER ROLE bikeshop_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE bikeshop_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE bikeshop_db TO bikeshop_user;
\q
```

### Deploy application code

```bash
git clone https://github.com/your-username/bikeshop.git /home/ubuntu/bikeshop
cd /home/ubuntu/bikeshop
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
cp .env.example .env
nano .env  # Fill in all production values
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Gunicorn systemd service

Create `/etc/systemd/system/bikeshop.service`:
```ini
[Unit]
Description=BikeShop Gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/bikeshop
ExecStart=/home/ubuntu/bikeshop/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/bikeshop.sock \
          config.wsgi:application
EnvironmentFile=/home/ubuntu/bikeshop/.env
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start bikeshop
sudo systemctl enable bikeshop
sudo systemctl status bikeshop
```

### Nginx configuration

Create `/etc/nginx/sites-available/bikeshop`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ubuntu/bikeshop/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/ubuntu/bikeshop/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/bikeshop.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/bikeshop /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot updates your Nginx config automatically and sets up certificate auto-renewal via a systemd timer.

---

## 23. Security Hardening Checklist

All items in the table below are automatically applied when `DEBUG=False` in `config/settings.py`.

| Setting | Value Applied | Effect |
|---|---|---|
| SECURE_BROWSER_XSS_FILTER | True | Sets the X-XSS-Protection response header |
| SECURE_CONTENT_TYPE_NOSNIFF | True | Sets X-Content-Type-Options: nosniff header |
| X_FRAME_OPTIONS | DENY | Prevents the site from being embedded in iframes |
| SECURE_HSTS_SECONDS | 31536000 | Tells browsers to only use HTTPS for one year |
| SECURE_HSTS_INCLUDE_SUBDOMAINS | True | Extends HSTS policy to all subdomains |
| SECURE_SSL_REDIRECT | True | Redirects all HTTP requests to HTTPS |
| SESSION_COOKIE_SECURE | True | Session cookie is only sent over HTTPS |
| CSRF_COOKIE_SECURE | True | CSRF cookie is only sent over HTTPS |

Additional recommendations:

- Rotate SECRET_KEY if it was ever accidentally committed to version control.
- Set ALLOWED_HOSTS to your exact list of domains — never use a wildcard asterisk.
- Use a strong, unique PostgreSQL user password that is not reused elsewhere.
- Run Gunicorn as a non-root OS user.
- Keep all pip dependencies updated regularly with `pip list --outdated`.
- Enable Fail2ban on your VPS to block brute-force login attempts at the firewall level.
- Store all payment provider keys only in environment variables — never hardcode them in source files.
- Consider adding `django-axes` to your installed apps for Django-level login attempt throttling.

---

## 24. Customisation Guide

### Changing the brand colour

The entire colour scheme is driven by CSS variables. Open `static/css/main.css` and change these values at the top of the file:

```css
--bs-primary: #e63946;
--accent:     #e63946;
--accent-dark:#c1121f;
```

The accent colour cascades to buttons, badges, price tags, hover states, and the navbar brand name automatically.

### Adding a new bike type

Add a new tuple to `Product.BIKE_TYPE_CHOICES` in `store/models.py`. Run `makemigrations` and `migrate`. The new type will automatically appear in the filter sidebar on the product catalog page.

### Adding a new product field

Add the field to the `Product` model in `models.py`. Run `makemigrations` and `migrate`. Add the field to the appropriate `fieldsets` section in `ProductAdmin` inside `admin.py`. Then render it in `product_detail.html` where you want it to appear.

### Changing products per page

In `config/settings.py`:
```python
PRODUCTS_PER_PAGE = 12  # Change to any integer you prefer
```

### Adding a new page

Create a view in `store/views.py` as a subclass of `TemplateView` or `View`. Add a URL pattern in `store/urls.py`. Create the corresponding template in `store/templates/store/`. Add a link in `base.html` if it should appear in the navigation.

### Changing shipping rates and options

Edit the `SHIPPING_RATES` dictionary near the top of `store/views.py`:
```python
SHIPPING_RATES = {
    'standard':  0,
    'express':   15,
    'overnight': 35,
}
```

Also update the matching `SHIPPING_CHOICES` list in the `CheckoutForm` inside `store/forms.py` to keep the labels and values consistent.

### Customising the admin site header

In `config/urls.py`:
```python
admin.site.site_header = "BikeShop Admin"
admin.site.site_title = "BikeShop"
admin.site.index_title = "Store Management"
```

---

## 25. Management Commands

### seed_data

```bash
python manage.py seed_data
python manage.py seed_data --no-images
```

Seeds the database with sample categories, brands, products, banners, and coupon codes. Downloads Unsplash images unless `--no-images` is passed. Safe to run multiple times.

### Standard Django commands

| Command | Purpose |
|---|---|
| python manage.py makemigrations | Generate migration files after changing models |
| python manage.py migrate | Apply all pending migrations |
| python manage.py createsuperuser | Create a new admin user interactively |
| python manage.py collectstatic | Copy static files to staticfiles/ for production |
| python manage.py shell | Open a Django-aware interactive Python shell |
| python manage.py dbshell | Open a direct database shell |
| python manage.py check | Run Django system checks without starting the server |
| python manage.py test store | Run the test suite for the store application |
| python manage.py showmigrations | List all migrations and their applied status |
| python manage.py sqlmigrate store 0001 | Print the SQL for a specific migration |

---

## 26. Troubleshooting

### ModuleNotFoundError: No module named 'decouple'

Your virtual environment is not activated or dependencies were not installed inside it.
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### ImproperlyConfigured: The SECRET_KEY setting must not be empty

Your `.env` file is missing or `SECRET_KEY` is not set in it.
```bash
cp .env.example .env
# Edit .env and add a SECRET_KEY value
```

### Product images do not appear after running seed_data

The seed command saves images to `media/products/`. Confirm the `media/` directory exists and is writable:
```bash
mkdir -p media
chmod 755 media
```
In development, confirm DEBUG is True so that `config/urls.py` serves media files. In production, confirm Nginx has a `location /media/` block pointing to the correct directory.

### OperationalError: no such table: store_product

Migrations have not been applied to the database.
```bash
python manage.py migrate
```

### Cart items disappear between sessions

Guest cart items are tied to the Django session. Confirm your SESSION_ENGINE is configured correctly. In development with SQLite, run `python manage.py migrate` to ensure the `django_session` table exists.

### Static files return 404 in production

Run `python manage.py collectstatic` and verify that your Nginx `location /static/` alias points to the `staticfiles/` directory (with an s), not the source `static/` directory.

### CSRF verification failed on login or forms

Confirm `ALLOWED_HOSTS` includes the exact domain making the request. If running behind a reverse proxy, ensure Nginx passes the `Host` header correctly. Only set `CSRF_COOKIE_SECURE=True` when HTTPS is fully configured.

### Email is printed to the terminal instead of being sent

In development, `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` is the default. This is intentional — it prints email content to the terminal. For production, set a real SMTP backend and credentials in `.env`.

---

## 27. Contributing

Contributions are welcome and appreciated.

1. Fork the repository on GitHub.
2. Create a descriptively named feature branch: `git checkout -b feature/add-product-comparison`.
3. Make your changes following the existing code conventions.
4. Run the test suite to confirm nothing is broken: `python manage.py test store`.
5. Commit with a clear and specific message: `git commit -m "Add: product comparison feature with side-by-side spec table"`.
6. Push your branch to your fork: `git push origin feature/add-product-comparison`.
7. Open a Pull Request against the `main` branch of this repository.

### Code conventions

- Follow PEP 8 for all Python code.
- Use class-based views for all new views — no function-based views.
- Business logic belongs in model methods and `@property` decorators, not in views or templates.
- Templates must contain no business logic. Pass all pre-computed values from the view context.
- Every new model must define `__str__`, `Meta.ordering`, and appropriate `db_index` hints on frequently filtered fields.
- All new URL patterns must use descriptive names within the `store` namespace.

---

## 28. License

This project is released under the MIT License.

```
MIT License

Copyright (c) 2025 BikeShop

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">
Built with Django · Bootstrap 5 · Pillow · WhiteNoise<br>
Ready to ride 🚴
</div>