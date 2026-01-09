# Contributing to Hackathon Management

Thank you for considering contributing to Django Hackathon Management! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing Your Changes](#testing-your-changes)
- [Submitting Changes](#submitting-changes)
- [Code Standards](#code-standards)
- [Reporting Issues](#reporting-issues)

## Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/OWASP-BLT/BLT-Hackathon.git
cd BLT-Hackathon/plugin/django-hackathon
```

### Step 2: Create a Test Django Project

Create a separate test project to develop and test the plugin:

```bash
# Navigate to a suitable directory
cd /path/to/your/workspace

# Create a test Django project
mkdir testproject
cd testproject
django-admin startproject testproj .

# Create a templates directory
mkdir -p templates
```

### Step 3: Create Base Template

Create `templates/base.html` with the following content:

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Hackathon Management{% endblock %}</title>
    <meta name="description" content="{% block description %}{% endblock %}">
    <meta name="keywords" content="{% block keywords %}{% endblock %}">
    <!-- Font Awesome 6.5.1 -->
    <link rel="stylesheet" 
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" 
          integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" 
          crossorigin="anonymous" 
          referrerpolicy="no-referrer" />
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### Step 4: Configure Test Project Settings

Edit `testproj/settings.py`:

```python
# Add templates directory
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # <---- Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Add blt_hackathon to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blt_hackathon',  # <---- Add this
]
```

### Step 5: Configure URLs

Edit `testproj/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hackathons/', include('blt_hackathon.urls')),
]
```

### Step 6: Install Plugin in Development Mode

```bash
# Install the plugin in editable mode
pip install -e /path/to/BLT-Hackathon/plugin/django-hackathon
```

### Step 7: Run Migrations

```bash
python manage.py migrate
```

### Step 8: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 9: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/hackathons/` to see the plugin in action.

## Making Changes

### Workflow for Plugin Development

1. **Make changes** to the plugin code in `BLT-Hackathon/plugin/django-hackathon/blt_hackathon/`

2. **Reinstall the plugin** to see changes:
   ```bash
   pip install -e /path/to/BLT-Hackathon/plugin/django-hackathon --force-reinstall --no-deps
   ```

3. **Restart the development server**:
   ```bash
   # Stop the current server (Ctrl+C)
   python manage.py runserver
   ```

4. **Test your changes** in the browser at `http://127.0.0.1:8000/hackathons/`

### Common Development Tasks

#### Modifying Views

Edit `blt_hackathon/views.py` and restart the server to see changes.

#### Updating Models

1. Edit `blt_hackathon/models.py`
2. Create migrations:
   ```bash
   python manage.py makemigrations blt_hackathon
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

#### Changing Templates

Edit templates in `blt_hackathon/templates/` and refresh your browser.

#### Adding Static Files

Add files to `blt_hackathon/static/` and collect static files:
```bash
python manage.py collectstatic
```

## Testing Your Changes

### Manual Testing

1. Create a new hackathon via the UI
2. Verify all fields are saved correctly
3. Test GitHub repository integration
4. Verify sponsorship and prize creation
5. Check the public listing page

### Running Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest
```

### Code Quality Checks

```bash
# Install development dependencies
pip install -e ".[dev]"

# Format code with black
black blt_hackathon/

# Sort imports
isort blt_hackathon/

# Run linter
ruff check blt_hackathon/
```

## Submitting Changes

### Before Submitting

1. Ensure your code follows the project's code standards
2. Test your changes thoroughly
3. Update documentation if necessary
4. Write clear commit messages

### Creating a Pull Request

1. **Fork the repository** on GitHub

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Screenshots if UI changes are involved
   - Reference to any related issues

## Code Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Maximum line length: 120 characters
- Use type hints where appropriate

### Django Best Practices

- Use class-based views when appropriate
- Follow Django's naming conventions
- Use Django's built-in features and utilities
- Write secure code (sanitize inputs, use CSRF protection)

### JavaScript Code Style

- Use ES6+ syntax
- Use meaningful variable names
- Add comments for complex logic
- Handle errors appropriately

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions and classes
- Update CONTRIBUTING.md for development process changes

## Reporting Issues

### Bug Reports

When reporting bugs, include:
- Python version
- Django version
- Plugin version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or screenshots

### Feature Requests

When requesting features:
- Describe the feature clearly
- Explain the use case
- Suggest possible implementation approaches
- Consider backward compatibility

## Development Tips

### Quick Reinstall Command

Create an alias for quick reinstallation:

```bash
alias reinstall-plugin="pip install -e /path/to/BLT-Hackathon/plugin/django-hackathon --force-reinstall --no-deps"
```

### Watching for Changes

Use Django's autoreload feature by keeping the development server running. Template and Python file changes will reload automatically.

### Database Reset

If you need to reset the database:

```bash
python manage.py migrate blt_hackathon zero
python manage.py migrate blt_hackathon
```

## Questions?

If you have questions or need help:
- Open an issue on GitHub
- Check existing issues and pull requests
- Review the documentation

Thank you for contributing to Hackathon Management!
