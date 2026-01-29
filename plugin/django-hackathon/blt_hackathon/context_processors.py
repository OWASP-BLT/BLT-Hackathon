"""
Context processors for blt_hackathon plugin
Provides common context variables for templates
"""

def hackathon_context(request):
    """
    Context processor for hackathon plugin
    Provides common context variables that might be expected by templates
    """
    return {
        'organization_exists': False,  # Disable org features in standalone plugin
        'org': None,
        'user_organizations': [],
        'is_plugin': True,  # Indicate this is the plugin version
    }