from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from ptdatabase import Powertool, Base, PowertoolItem, User
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from login_decorator import login_required
from flask import session as login_session

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Powertool Menu Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///powertool.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (    # noqa
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"

    '''
    Due to the formatting for the result from the server token exchange we
    have to split the token first on commas and select the first index which
    gives us the key : value for the server access token then we split it on
    colons to pull out the actual token value and replace the remaining quotes
    with nothing so that it can be used directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token   # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token   # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;' \
        'border-radius:150px;-webkit-border-radius: 150px;' \
        '-moz-border-radius: 150px;"> ' 
    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)   # noqa
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Gathers data from Google Sign In API and places it inside a session variable.
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
                                 'connected. '), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;' \
        'border-radius:150px;-webkit-border-radius: 150px;' \
        '-moz-border-radius: 150px;"> '   
    flash("You are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one_or_none()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Powertools Information
@app.route('/powertool/<int:powertool_id>/menu/JSON')
def powertoolMenuJSON(powertool_id):
    powertool = session.query(Powertool).filter_by(id=powertool_id).one_or_none()
    items = session.query(PowertoolItem).filter_by(
        powertool_id=powertool_id).all()
    return jsonify(PowertoolItems=[i.serialize for i in items])


@app.route('/powertool/<int:powertool_id>/menu/<int:menu_id>/JSON')
def PowertoolItemJSON(powertool_id, menu_id):
    Powertool_Item = session.query(PowertoolItem).filter_by(id=menu_id).one_or_none()
    return jsonify(Powertool_Item=Powertool_Item.serialize)


@app.route('/powertool/JSON')
def powertoolsJSON():
    powertools = session.query(Powertool).all()
    return jsonify(powertools=[r.serialize for r in powertools])


# Show all Powertools
@app.route('/')
@app.route('/powertool/')
def showPowertools():
    powertools = session.query(Powertool).order_by(asc(Powertool.brand))
    if 'username' not in login_session:
        return render_template('publicpowertools.html', powertools=powertools)
    else:
        return render_template('powertools.html', powertools=powertools)


# Create a new Powertools brand
@app.route('/powertool/new/', methods=['GET', 'POST'])
@login_required
def newPowertool():
    if request.method == 'POST':
        newPowertool = Powertool(
            brand=request.form['brand'], user_id=login_session['user_id'])
        session.add(newPowertool)
        flash('New Powertool %s Successfully Created' % newPowertool.brand)
        session.commit()
        return redirect(url_for('showPowertools'))
    else:
        return render_template('newPowertool.html')


# Edit a Powertool brand
@app.route('/powertool/<int:powertool_id>/edit/', methods=['GET', 'POST'])
@login_required
def editPowertool(powertool_id):
    editedPowertool = session.query(Powertool).filter_by(id=powertool_id).one_or_none()   # noqa
    if editedPowertool.user_id != login_session['user_id']:
        return "<script>" \
               "function myFunction()" \
               "{alert('You are not authorized" \
               "to edit this powertool." \
               " Please create your own powertool in order"\
               " to edit.');}" \
               "</script>" \
               "<body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['brand']:
            editedPowertool.brand = request.form['brand']
            flash('Powertool Successfully Edited %s' % editedPowertool.brand)
            return redirect(url_for('showPowertools'))
    else:
        return render_template('editPowertool.html', powertool=editedPowertool)


# Delete a Powertool brand
@app.route('/powertool/<int:powertool_id>/delete/', methods=['GET', 'POST'])
@login_required
def deletePowertool(powertool_id):
    powertoolToDelete = session.query(Powertool).filter_by(id=powertool_id).one_or_none()   # noqa
    if powertoolToDelete.user_id != login_session['user_id']:
        return "<script>" \
               "function myFunction()" \
               "{alert('You are not authorized" \
               "to delete this powertool." \
               " Please create your own powertool in order"\
               " to delete.');}" \
               "</script>" \
               "<body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(powertoolToDelete)
        flash('%s Successfully Deleted' % powertoolToDelete.brand)
        session.commit()
        return redirect(url_for('showPowertools', powertool_id=powertool_id))
    else:
        return render_template('deletePowertool.html',
                               powertool=powertoolToDelete)


# Show a Powertool items
@app.route('/powertool/<int:powertool_id>/')
@app.route('/powertool/<int:powertool_id>/menu/')
def showPowertoolItem(powertool_id):
    powertool = session.query(Powertool).filter_by(id=powertool_id).one_or_none()
    creator = getUserInfo(powertool.user_id)
    items = session.query(PowertoolItem).filter_by(
        powertool_id=powertool_id).all()
    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        return render_template('publicptmenu.html', items=items,
                               powertool=powertool, creator=creator)
    else:
        return render_template('ptmenu.html', items=items,
                               powertool=powertool, creator=creator)


# Create a new Powertool item
@app.route('/powertool/<int:powertool_id>/menu/new/', methods=['GET', 'POST'])
@login_required
def newPowertoolItem(powertool_id):
    powertool = session.query(Powertool).filter_by(id=powertool_id).one_or_none()
    if request.method == 'POST':
        newPowertoolItem = PowertoolItem(model=request.form['model'],
                                         description=request.form
                                         ['description'],
                                         price=request.form['price'],
                                         category=request.form['category'],
                                         powertool_id=powertool_id,
                                         user_id=powertool.user_id)
        session.add(newPowertoolItem)
        session.commit()
        flash('New Item %s Successfully Created' % (newPowertoolItem.model))
        return redirect(url_for('showPowertoolItem',
                                powertool_id=powertool_id))
    else:
        return render_template('newPowertoolItem.html',
                               powertool_id=powertool_id)


# Edit a Powertool item
@app.route('/powertool/<int:powertool_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editPowertoolItem(powertool_id, menu_id):
    editedPowertoolItem = session.query(PowertoolItem).filter_by(id=menu_id).one_or_none()   # noqa
    powertool = session.query(Powertool).filter_by(id=powertool_id).one_or_none()
    if login_session['user_id'] != powertool.user_id:
        return "<script>" \
               "function myFunction()" \
               "{alert('You are not authorized" \
               "to edit menu items to this powertool." \
               " Please create your own powertool in order"\
               " to edit items.');}" \
               "</script>" \
               "<body onload='myFunction()'>"       
    if request.method == 'POST':
        if request.form['model']:
            editedPowertoolItem.model = request.form['model']
        if request.form['description']:
            editedPowertoolItem.description = request.form['description']
        if request.form['price']:
            editedPowertoolItem.price = request.form['price']
        if request.form['category']:
            editedPowertoolItem.category = request.form['category']
        session.add(editedPowertoolItem)
        session.commit()    
        flash('Powertool Item Successfully Edited')
        return redirect(url_for('showPowertoolItem',
                                powertool_id=powertool_id))
    else:
        return render_template('editPowertoolItem.html',
                               powertool_id=powertool_id, menu_id=menu_id,
                               item=editedPowertoolItem)


# Delete a Powertool item
@app.route('/powertool/<int:powertool_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deletePowertoolItem(powertool_id, menu_id):
    powertool = session.query(Powertool).filter_by(id=powertool_id).one_or_none()
    itemToDelete = session.query(PowertoolItem).filter_by(id=menu_id).one_or_none()
    if login_session['user_id'] != powertool.user_id:
        return "<script>" \
               "function myFunction()" \
               "{alert('You are not authorized" \
               "to delete menu items to this powertool." \
               " Please create your own powertool in order"\
               " to delete items.');}" \
               "</script>" \
               "<body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showPowertoolItem',
                                powertool_id=powertool_id))
    else:
        return render_template('deletePowertoolItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            # del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showPowertools'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showPowertools'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
