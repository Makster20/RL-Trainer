from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import pychasing
import os
from requests.exceptions import SSLError
from pprint import pprint

app = Flask(__name__)
app.secret_key = 'liverpool'

db = SQL("sqlite:///trainer.db")

TOKEN              = "sdH539LBF3NZThPb0UdyxtrHKNvRINzO4PtvxMYc"
STEAM_ID           = ""
REPLAY_PATH        = "replays/3A942E6446522E06A44F5AB7EE8989C4.replay"
GROUP_NAME         = "__pychasing_test_group__"
REPLAY_NAME        = "__pychasing_test_replay__"

pychasing_client = pychasing.Client(
    TOKEN,
    True,
    pychasing.PatreonTier.none,
    True
)



@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == 'POST':
        # Error checks
        if 'replay' not in request.files:
            return apology("must provide replay", 403)

        replay = request.files['replay']

        if not replay.filename.endswith('.replay'):
            return apology('must be a replay file', 403)

        # Specify the directory where you want to save the file
        upload_dir = 'replays'

        # Create the directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save the file with its original filename
        replay_path = os.path.join(upload_dir, replay.filename)
        replay_path = replay_path.replace('\\', '/')
        replay.save(replay_path)
        print(f'file saved {replay_path}')

        # Read file content and upload
        with open(replay_path, 'rb') as replay_file:
            res0 = pychasing_client.upload_replay(replay_file, pychasing.Visibility.unlisted)
            print(f"\033[96mpychasing.client.Client.upload_replay \033[90m: \033[92mGOOD\033[0m\n\nNEW REPLAY ID: {res0.json()['id']}")

        # Get the replay id
        replay_id = res0.json()['id']

        # Store the replay_id in session
        session['uploaded_replay_id'] = replay_id

        # Delete file from replays folder as it has been uploaded
        os.remove(replay_path)

        res0 = pychasing_client.get_replay(replay_id)

        print("\033[96mpychasing.client.Client.get_replay \033[90m: \033[92mGOOD\033[0m")
        pprint(res0.json())


        if len(res0.json()['blue']['players']) == 0 or len(res0.json()['orange']['players']) == 0:
            print(len(res0.json()['blue']['players']))
            print(len(res0.json()['orange']['players']))
            pprint(res0.json())
            return apology('1v1 not supported')


        return redirect('/playstyle')

    else:
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("conpassword"):
            return apology("must confirm password", 403)

        # Ensure passwords match
        if request.form.get("password") != request.form.get("conpassword"):
            return apology("must match passwords", 403)

        # Ensure username is not taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) >= 1:
            return apology("username is taken", 403)


        # Declare username and hash for insertion
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Get the new user's id
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)

        if len(rows) == 0:
            return apology("registration error", 400)

        # Log the user in by storing the user's id in the session
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/playstyle", methods=["GET", "POST"])
@login_required
def playstyle():

    if request.method == 'POST':
        uploaded_replay_id = session.get('uploaded_replay_id')
        file = pychasing_client.get_replay(uploaded_replay_id)

        selected_data = request.form.get('selectedPlayer')

        if selected_data:
            team_color, player_index = selected_data.split('-')
            # Handle the selected team color and player index here

        player_index = int(player_index)

        avgSpeed = int( file.json()[team_color]['players'][player_index]['stats']['movement']['avg_speed'] / 10)

        ballTouches = int( file.json()[team_color]['players'][player_index]['stats']['positioning']['avg_distance_to_ball'] + file.json()[team_color]['players'][player_index]['stats']['positioning']['percent_closest_to_ball'])
        ballTouches = int( ballTouches / 10 )

        bpm = int( file.json()[team_color]['players'][player_index]['stats']['boost']['bpm'] )

        boostEfficiency = int( file.json()[team_color]['players'][player_index]['stats']['boost']['bcpm'] - file.json()[team_color]['players'][player_index]['stats']['boost']['avg_amount'] + file.json()[team_color]['players'][player_index]['stats']['boost']['percent_zero_boost'] - file.json()[team_color]['players'][player_index]['stats']['boost']['percent_full_boost'])

        timeSS = int( file.json()[team_color]['players'][player_index]['stats']['movement']['time_supersonic_speed'] )

        percentInOffHalf = int( file.json()[team_color]['players'][player_index]['stats']['positioning']['percent_offensive_half'] )

        percentInDefHalf = int( file.json()[team_color]['players'][player_index]['stats']['positioning']['percent_defensive_half'] )

        percentInMid = int( file.json()[team_color]['players'][player_index]['stats']['positioning']['percent_neutral_third'] )

        distanceToMates = int( file.json()[team_color]['players'][player_index]['stats']['positioning']['avg_distance_to_mates'] / 10)

        assists = int( file.json()[team_color]['players'][player_index]['stats']['core']['assists'] )

        saves = int( file.json()[team_color]['players'][player_index]['stats']['core']['saves'] )

        assists = int( file.json()[team_color]['players'][player_index]['stats']['core']['assists'] )

        goals = int( file.json()[team_color]['players'][player_index]['stats']['core']['goals'] )

        shots = int( file.json()[team_color]['players'][player_index]['stats']['core']['shots'] )

        print(f"avgspeed: {avgSpeed}, balltocuhes: {ballTouches}, bpm: {bpm}, boosteficeincy: {boostEfficiency}, Time Supersonic{timeSS}, percent in offhalf: {percentInOffHalf}, percentin def half: {percentInDefHalf}, percent in mid: {percentInMid}, Distance to mates: {distanceToMates}, assist: {assists}, sves: {saves}, gols: {goals} shots: {shots}")

        if avgSpeed < 135 and bpm < 310 and timeSS < 25 and percentInDefHalf > 62:
            playstyle = 'anchor'
            print(session['user_id'])

            if db.execute('SELECT * FROM playstyle WHERE user_id = ?', session['user_id']):

                db.execute('DELETE FROM playstyle WHERE user_id = ?', session['user_id'])
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])
            else:
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])

            return render_template('anchor.html')

        elif avgSpeed > 145 and bpm > 400 and timeSS > 52:
            playstyle = 'ballchaser'

            if db.execute('SELECT * FROM playstyle WHERE user_id = ?', session['user_id']):

                db.execute('DELETE FROM playstyle WHERE user_id = ?', session['user_id'])
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])
            else:
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])

            return render_template('ballchaser.html')

        elif percentInMid > 31 and distanceToMates > 290:
            playstyle = 'passer'

            if db.execute('SELECT * FROM playstyle WHERE user_id = ?', session['user_id']):

                db.execute('DELETE FROM playstyle WHERE user_id = ?', session['user_id'])
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])
            else:
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])

            return render_template('passer.html')

        else:
            playstyle = 'allrounder'

            if db.execute('SELECT * FROM playstyle WHERE user_id = ?', session['user_id']):

                db.execute('DELETE FROM playstyle WHERE user_id = ?', session['user_id'])
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])
            else:
                db.execute('INSERT INTO playstyle (playstyle, user_id) VALUES (?, ?)', playstyle, session['user_id'])

            return render_template('allrounder.html')



    else:
        uploaded_replay_id = session.get('uploaded_replay_id')

        file = pychasing_client.get_replay(uploaded_replay_id)
        pprint(file.json())

        try:
            blueplayers = file.json()['blue']['players']
            orangeplayers = file.json()['orange']['players']

        except KeyError:
            return apology('File Error, Refresh and try again')



        return render_template("chooseplayer.html", blueplayers=blueplayers, orangeplayers=orangeplayers)


@app.route("/myplaystyle", methods=["GET"])
@login_required
def myplaystyle():
    result = db.execute('SELECT playstyle FROM playstyle WHERE user_id = ?', session['user_id'])

    # Check if the result is not empty
    if result:
        # Extract the playstyle from the first row (dictionary) in the result list
        playstyle = result[0]['playstyle']

        if playstyle == 'anchor':
            return render_template('anchor.html')

        if playstyle == 'ballchaser':
            return render_template('ballchaser.html')

        if playstyle == 'passer':
            return render_template('passer.html')

        if playstyle == 'allrounder':
            return render_template('allrounder.html')
    else:
        return render_template('noplaystyle.html')
