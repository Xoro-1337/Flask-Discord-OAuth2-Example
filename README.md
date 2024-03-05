# Discord OAuth2 Example

## Usage
- Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create an application if you haven't already.
- Select OAuth2 on the sidebar. Here you will find your *Client ID* and *Client Secret*.
- Create 2 environmental variables called `CLIENT_ID` and `CLIENT_SECRET` (or load them however you want [here](https://github.com/Xoro-1337/Flask-Discord-OAuth2-Example/blob/master/discord.py#L41)).
- On the same page, create a Redirect to `http://localhost:5000/callback`. This must match the endpoint you create [here](https://github.com/Xoro-1337/Flask-Discord-OAuth2-Example/blob/master/app.py#L29) and define [here](https://github.com/Xoro-1337/Flask-Discord-OAuth2-Example/blob/master/discord.py#L44).
- Run the following commands in your terminal (or CMD Prompt, but change `python3` to `py`):
```
$ git clone https://github.com/Xoro-1337/Flask-Discord-OAuth2-Example.git
$ cd Flask-Discord-OAuth2-Example
$ python3 -m pip install -r requirements.txt
$ python3 main.py
```

<details>
  <summary>Preview</summary>
  
  ![image](https://github.com/Xoro-1337/Flask-Discord-OAuth2-Example/assets/72954614/e44a8590-93a6-494f-8c0e-44517cf7e3c6)
  
  ![image](https://github.com/Xoro-1337/Flask-Discord-OAuth2-Example/assets/72954614/223b8ce6-2051-4f9a-b6f9-baf1f44c71fb)
</details>
