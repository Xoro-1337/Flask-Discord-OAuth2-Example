from flask import Flask, render_template, session, request, redirect
from werkzeug.exceptions import BadRequest

from discord import DiscordOAuth, requires_authorization, gen_avatar_url, gen_banner_url

app = Flask(__name__)
app.secret_key = 'SuP3R53cR3tK3Y'

oauth = DiscordOAuth()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return redirect(oauth.generate_authorization_url())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if not code or not state:
        # Input validation: Ensure code and state parameters are present
        raise BadRequest("Missing required parameters.")

    try:
        oauth.init(code, state)
        oauth.get_user()
    except Exception as e:
        # Log the specific error
        app.logger.error('Error fetching user info: %s', e)
        # Optionally, you can provide a more user-friendly message
        return "An error occurred while fetching user info. Please try again later.", 500

    # Redirect user to home page
    return redirect('/success')


@app.route('/success')
@requires_authorization
def success():
    return render_template('success.html', avatar=gen_avatar_url(),
                           banner=gen_banner_url())


if __name__ == '__main__':
    app.run()
