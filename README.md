# Readify: Library Management System

A comprehensive web-based library management system built with Django that automates borrowing processes, tracks fines, and provides an intuitive interface for both librarians and borrowers.

## 🚀 Features

### Core Functionality
- **User Management**: Complete user registration and authentication system
- **Book Inventory Management**: Add, edit, and organize books with categories and authors
- **Automated Borrowing System**: Borrow and return books with automatic availability tracking
- **Fine Calculation**: Automatic calculation of overdue fines based on configurable rates
- **Reservation System**: Reserve books when they're not available
- **Reports & Analytics**: Comprehensive dashboard with library statistics

### User Roles
- **Borrowers**: Can browse books, borrow, return, and reserve books
- **Librarians/Staff**: Full access to all features including user management and reports
- **Administrators**: Complete system control including fine management

### Technical Features
- **Modern UI**: Responsive design with Bootstrap 5
- **Real-time Updates**: Automatic status updates and notifications
- **Search & Filter**: Advanced book search with multiple criteria
- **Data Export**: Export reports in various formats
- **Mobile Responsive**: Works seamlessly on all devices

## 📋 Requirements

- Python 3.8 or higher
- Django 4.2 or higher
- Pillow (for image handling)
- Modern web browser

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Python2/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
python manage.py loaddata sample_data.json
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 📁 Project Structure

```
backend/
├── readify/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main settings file
│   ├── urls.py            # URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── library/                # Main library app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin interface
│   └── urls.py            # App URLs
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── library/           # Library-specific templates
│   └── registration/      # Authentication templates
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images
├── media/                  # User-uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🎯 Usage

### For Borrowers

1. **Registration**: Create an account with your details
2. **Browse Books**: Search and filter the library catalog
3. **Borrow Books**: Borrow available books (up to your limit)
4. **Track Borrowings**: View your current and past borrowings
5. **Reserve Books**: Reserve books when they're unavailable
6. **Pay Fines**: View and pay any overdue fines

### For Librarians

1. **Dashboard**: View library statistics and recent activity
2. **Manage Books**: Add, edit, and organize book inventory
3. **User Management**: Manage borrower accounts
4. **Process Returns**: Handle book returns and fine collection
5. **Generate Reports**: Create various library reports
6. **Fine Management**: Waive or collect overdue fines

## ⚙️ Configuration

### Fine Settings
Edit `settings.py` to configure fine calculation:
```python
DAILY_FINE_RATE = 5.0  # $5 per day
MAX_FINE_DAYS = 30     # Maximum days to calculate fine
```

### Borrowing Limits
Set default borrowing limits in the Borrower model or through admin interface.

### Email Configuration
Configure email settings for notifications (optional):
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🗄️ Database Models

### Core Models
- **User**: Extended Django User model
- **Borrower**: Library member profile
- **Book**: Book inventory with metadata
- **Author**: Book authors
- **Category**: Book categories
- **Borrowing**: Borrowing transactions
- **Fine**: Fine records
- **Reservation**: Book reservations

### Key Relationships
- Books have multiple authors (Many-to-Many)
- Borrowers can borrow multiple books (One-to-Many)
- Each borrowing can have one fine (One-to-One)
- Books can have multiple reservations (One-to-Many)

## 🔧 Customization

### Adding New Features
1. Create new models in `models.py`
2. Add corresponding forms in `forms.py`
3. Create views in `views.py`
4. Update URL patterns in `urls.py`
5. Create templates in `templates/library/`
6. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Styling
- Modify `static/css/style.css` for custom styles
- Update `templates/base.html` for layout changes
- Add new JavaScript functionality in `static/js/main.js`

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving with WhiteNoise
4. Configure email settings
5. Set up proper logging
6. Use environment variables for sensitive data

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/readify
EMAIL_HOST=your-smtp-server
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 API Endpoints

The system includes basic API endpoints:
- `/api/search/` - Book search API
- `/api/check-availability/` - Check book availability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- Email notifications for due dates and fines
- Mobile app integration
- Advanced reporting and analytics
- Integration with external library systems
- Multi-language support
- Advanced search with Elasticsearch
- Book recommendation system

## 📈 Performance Optimization

- Database indexing on frequently queried fields
- Caching for search results
- Image optimization for book covers
- Lazy loading for large datasets
- CDN integration for static files

---

**Readify Library Management System** - Simplifying library operations through automation and modern web technology.
