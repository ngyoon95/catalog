from functools import wraps
from flask import session as login_session


# User Login Decorator
def login_required(func):
    """
    A decorator to confirm a user is logged in or redirect as needed.
    """
    @wraps(func)
    def login(*args, **kwargs):
        # Redirect to login if user not logged in, else execute func.
        if 'username' not in login_session:
            return redirect('/login')
        return func(*args, **kwargs)
    return login