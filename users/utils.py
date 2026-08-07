from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    """
    Allow access only to:
    - superusers
    - users in the 'Administrator' group
    """
    return user_passes_test(
        lambda u: u.is_authenticated and (
            u.is_superuser or u.groups.filter(name="Administrator").exists()
        )
    )(view_func)
