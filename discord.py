import os
import requests
from flask import session


def requires_authorization(f):
    def wrapper(*args, **kwargs):
        if 'access_token' in session:
            return f(*args, **kwargs)
        else:
            body = """
            <h1>Unauthorized</h1>
            <p>You must be logged in to access this page.</p>
            <button onclick="window.location.href='/login'">Login</button>
            """
            return body

    wrapper.__name__ = f.__name__
    return wrapper


def is_animated(image):
    ext = image[:2]
    if ext == "a_":
        return ".gif"
    else:
        return ".png"


def gen_avatar_url():
    return (f"https://cdn.discordapp.com/avatars/{session['user_id']}/{session['user_avatar']}"
            f"{is_animated(session['user_avatar'])}")


def gen_banner_url():
    return (f"https://cdn.discordapp.com/banners/{session['user_id']}/{session['user_banner']}"
            f"{is_animated(session['user_banner'])}")


class DiscordOAuth:
    client_id = os.getenv('CLIENT_ID')
    secret_id = os.getenv('CLIENT_SECRET')
    scopes = "identify+email"  # Scopes separated by + sign
    redirect_url = "http://localhost:5000/callback"  # Redirect URL must match the one in the Discord Developer Portal

    @staticmethod
    def gen_state():
        state = os.urandom(12).hex()
        session['state'] = state
        return state

    def generate_authorization_url(self):
        return (f"https://discord.com/oauth2/authorize?response_type=code&client_id={DiscordOAuth.client_id}"
                f"&redirect_uri={DiscordOAuth.redirect_url}&scope={DiscordOAuth.scopes}&state={self.gen_state()}")

    @staticmethod
    def init(code, state):
        if state == session.get('state'):
            auth_url = "https://discord.com/api/oauth2/token"
            data = {
                "client_id": DiscordOAuth.client_id,
                "client_secret": DiscordOAuth.secret_id,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": DiscordOAuth.redirect_url
            }
            response = requests.post(auth_url, data=data)
            results = response.json()
            session['access_token'] = results['access_token']
            return True
        else:
            return False

    @staticmethod
    def get_user():
        if 'access_token' in session:
            get_user_url = "https://discord.com/api/users/@me"
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Authorization': f"Bearer {session['access_token']}"}
            response = requests.get(get_user_url, headers=headers)
            results = response.json()
            print(results)
            user_info = {
                'username': results['username'],
                'user_id': results['id'],
                'user_avatar': results['avatar'],
                'user_flags': results['public_flags'],
                'user_premium': results['premium_type'],
                'flags': results['flags'],
                'user_banner': results['banner'],
                'email': results['email'],
                'accent_color': results['accent_color']
            }
            for k, v in user_info.items():
                session[k] = v
            return user_info
        else:
            return None

    @staticmethod
    def check_state(state):
        return state == session.get('state', '')

    @staticmethod
    def get_user_flags():
        user_flags = session.get('user_flags', 0)
        badges = []
        for i in range(20):
            if user_flags & (1 << i):
                badges.append(str(i))
        return badges
