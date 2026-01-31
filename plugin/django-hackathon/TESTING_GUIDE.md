# Quick Testing Guide for BLT Hackathon Plugin

This guide will help you quickly test the Django Hackathon plugin in under 5 minutes.

## Prerequisites

- Python 3.11+
- Django knowledge (basic)

## Step 1: Create a Test Django Project

```bash
# Create a new directory for testing
mkdir hackathon-test && cd hackathon-test

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Django
pip install django

# Create Django project
django-admin startproject testproject
cd testproject
```

## Step 2: Install the Hackathon Plugin

```bash
# Install from TestPyPI
pip install -i https://test.pypi.org/simple/ blt-hackathon==0.1.1
```

**Latest Version**: Check [https://test.pypi.org/project/blt-hackathon](https://test.pypi.org/project/blt-hackathon) for the newest version.

## Step 3: Configure Django Settings

Edit `testproject/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Add the hackathon plugin
    'blt_hackathon',
]
```

## Step 4: Configure URLs

Edit `testproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hackathons/', include('blt_hackathon.urls')),
]
```

## Step 5: Create Base Template (Required for Charts)

Create directory and file: `testproject/templates/base.html`

```bash
mkdir templates
```

Create `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Hackathon Test{% endblock %}</title>
    
    <!-- Required: Chart.js for charts -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Required: Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" 
          integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" 
          crossorigin="anonymous" referrerpolicy="no-referrer" />
    
    <!-- Optional: Basic styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-100">
    <div class="container mx-auto py-8">
        {% block content %}{% endblock %}
    </div>
    
    <!-- Required: Scripts block for Chart.js initialization -->
    {% block scripts %}{% endblock %}
</body>
</html>
```

Update `testproject/settings.py` to include templates directory:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            # ... rest of the config
        },
    },
]
```

## Step 6: Run Migrations and Create Superuser

```bash
# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
# Enter: username=admin, email=admin@test.com, password=admin123
```

## Step 7: Start Server and Test

```bash
# Start development server
python manage.py runserver
```

## Step 8: Access and Test Features

### 🎯 **Quick Test Checklist:**

1. **Visit Hackathon List**: http://127.0.0.1:8000/hackathons/
   - Should show empty list with "Create Hackathon" button

2. **Create Test Hackathon**:
   - Click "Create Hackathon"
   - Fill in:
     - Name: "Test Hackathon 2024"
     - Description: "A test hackathon for plugin testing"
     - Start Date: Today's date
     - End Date: Tomorrow's date
   - Click "Create"

3. **Test Detail Page**:
   - Click on your created hackathon
   - ** Charts should display**: You should see:
     - Pull Request Activity chart (bar chart)
     - Page Views sparkline (small chart)
   - ** Icons should display**: Font Awesome icons should be visible

4. **Test Admin Interface**: http://127.0.0.1:8000/admin/
   - Login with superuser credentials
   - Navigate to "BLT_HACKATHON" → "Hackathons"
   - Should see your created hackathon

##  Success Indicators

-  **Charts render properly** (no console errors)
-  **Font Awesome icons display**
-  **Responsive design works**
-  **Admin interface accessible**
-  **CRUD operations work** (Create, Read, Update, Delete hackathons)

## 🐛 Troubleshooting

### Charts Not Displaying?
- Check browser console for JavaScript errors
- Ensure Chart.js is loaded: `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`
- Ensure base template has `{% block scripts %}{% endblock %}`

### Icons Not Displaying?
- Check network tab for Font Awesome CSS load errors
- Ensure Font Awesome CSS is in `<head>` section

### 500 Server Errors?
- Check Django debug output
- Ensure all migrations are applied: `python manage.py migrate`
- Ensure `blt_hackathon` is in `INSTALLED_APPS`

##  Next Steps

- Add GitHub repositories to track real pull requests
- Configure sponsors and prizes
- Customize the styling to match your project
- Deploy to production

**Total setup time: ~5 minutes** ⚡️