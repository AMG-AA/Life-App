from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from database.db_setup import get_db, close_connection
import requests

def login_required(f):
    """Decorator to require user to be logged in"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
