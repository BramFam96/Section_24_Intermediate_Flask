# Goals

- Define hashing
- Implement authentication and authorization in flask with **Bcrypt**
  - _authorization and authentication are different_

Ultimately: build and application with authorization and authentication

## TOC

- [Goals](#goals)
  - [TOC](#toc)
  - [Auth v Auth!](#auth-v-auth)
    - [Horrible no good authentication](#horrible-no-good-authentication)
  - [Hashing](#hashing)
    - [Cryptographic hashing](#cryptographic-hashing)
    - [Bad Implementation](#bad-implementation)
    - [Built-in Hashing](#built-in-hashing)
  - [Salts / Hashing Algos](#salts--hashing-algos)
    - [Problems with hashing algos](#problems-with-hashing-algos)
    - [Salting](#salting)
  - [Bcrypt](#bcrypt)
    - [Intro](#intro)
    - [Work-factor](#work-factor)
  - [Flask-Bcrypt](#flask-bcrypt)
    - [Session storage](#session-storage)
    - [1. Logic in templates:](#1-logic-in-templates)
    - [2. Logic in view functions:](#2-logic-in-view-functions)
    - [User priveleges](#user-priveleges)
    - [Gating a page](#gating-a-page)
  - [### Delete Permissions](#-delete-permissions)
    - [Errors](#errors)

---

## Auth v Auth!

---

Authentication - verifying a user's identity  
Authorization - determining an authenticated users privileges

- create, delete, etc;

---

### Horrible no good authentication

---

```py
class BadUser(db.Model):
    "Site user."

    __tablename__ = "bad_users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.Text,
                         nullable=False,
                         unique=True)

    password = db.Column(db.Text,
                         nullable=False)
```

Saves password directly!

```py
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = BadUser(username=name, password=pwd)
        db.session.add(user)
        db.session.commit()

        # on successful login, redirect to secret page
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)
```

```py
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = BadUser(username=name, password=pwd)
        db.session.add(user)
        db.session.commit()

        # on successful login, redirect to secret page
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)
```

The method above is very easy, but stores pwds as plaintext in the db!

---

## Hashing

---

Hashing functions map inputs, typicaly plain-text, and outputs a fixed length output  
It does this systematically, and is therefor unencryptable

---

### Cryptographic hashing

---

One-way encryption:

- encrypted outputs can **not** be turned back into inputs
  Unpredictable outputs:
- small dif in input (single character) creates big different output
  We'll eventually use this to encrypt passwords!

---

### Bad Implementation

---

DO NOT DO THIS!  
[Badhash demo](demo/badhash.py)

```py
def awful_hash(phrase):
    """Truly terrible hash:
        simply shifts each letter (a->b, etc).

        >>> awful_hash('yay')
        'zbz'
    """

    return ''.join(next_char(c) for c in phrase)
```

Not one-way!

```py
def slightly_better_hash(phrase):
    """Better hash: returns every other letter, shifted, max 4.

        >>> slightly_better_hash('penguin1')
        'qovo'

    Since this is "lossy", multiple inputs return same output:

        >>> slightly_better_hash('penguin1~pretzel7')
        'qovo'

        >>> slightly_better_hash('p?nguinZ')
        'qovo'
    """

    return ''.join(next_char(c) for c in phrase[0:8:2])
```

Problem - different inputs will give us same output  
Cryptographic hash funcs will give us very different outputs, even for similar outputs!

---

### Built-in Hashing

---

Hash is python's built in hashing function  
_We would not use this to store passwords!_

```py
hash('teststring')
returns 64-bit numeric val and has been optimized for speed
```

Meets many of our requirements, but still not good enough!  
Hashing we'll use will use 128-bit outputs, and a slower process.  
Dictionaries:

```py
d = {'name': 'Harry', 'house':'Griffindor'}
# Behind the scenes the keys are hashed. Leads to very fast look up times!
d['house'] -> roughly equal lookup time regardless of dict size!
# This is why we must use immitubale values as dict keys;
ie d = {[]: 123} -> invalid
```

---

## Salts / Hashing Algos

---

Popular hashing algos (_there are only a handful_):
| Cryptographic | PW Hashing |
| :----------- | :----------- |
| MD5 | Argon2 |
| SHA(_family_) | Bcrypt |
| | Scrypt |;

Column 1 - Fast, non-reversible, very different output - not suitable for pwds  
Column 2 - Same, but slow, and hard to optimize

---

### Problems with hashing algos

---

There are only a handful of hashing algos, and their popularity makes them vulnerable

- often pwds are saved as {'hash_value' : 'password'} somewhere in our db;
- bad actors could compile a list of common, hashed pwds, and use them to try and extract pwds
- b/c pwds are often reused and repetitive this method works!

---

### Salting

---

A salt is a random string we add to our data _prior_ to hashing

Once we do this, we have a salted hash;

'''py
salt = 'asd321asd4312'
pw = 'example'
hash(f'{pw}{salt}')
When comparing to db we pass in salt
'''

---

## Bcrypt

---

### Intro

Use Bcrypt to generate a new salt each time we hash a string

```py
import bcrypt   # pip install bcrypt
# We'll actually be using flask-bcrypt
salt = bcrypt.gensalt()
# Creating a new salt for each pwd safe-guards against duplicated pwds
salt -> b'$2b$12$uYNRTDE7RrMvwDcF9f1Yyu'
# b signifies that we are looking at a binary string
bcrypt.hashpw(b'secret', salt) ->
# We also pass the pwd in as binary!
b'$2b$12$uYNRTDE7RrMvwDcF9f1Yyuvuu48PzANrWy88Iz3z1tRTfdXi6DlNW'
```

We will store this string -> no need to store the salt seperately  
Bcrypt will:

1. **Compare** a non-hashed pwd to the hashed pwd
2. **Extract** the salt from the hashed pwd
3. **Rehash** the pwd w/ the extracted salt
4. **Compare** the results

---

### Work-factor

---

Bcrypt is designed to be slow, but computer get _faster_ all the time!  
To compensate for this bcrypt includes a work factor, aka a cost factor  
The work factor tells becrypt how many times it should run its algo.

```py
Our hashed string looked like this:
b'$2b$12$uYNRTDE7RrMvwDcF9f1Yyuvuu48PzANrWy88Iz3z1tRTfdXi6DlNW'
Split up:
b'$2b$12$' -> bcrypt w/ workfactor of 12
b'uYNRTDE7RrMvwDcF9f1Yyu' -> salt itself
b'vuu48PzANrWy88Iz3z1tRTfdXi6DlNW' -> salted pwd
#$2b$12 signifies we are using b crypt with a work-factor of 12!
```

- for each round the time to crack the algo with brute force, or work, increases exponentially
- this number is steadily increased over time to compensate for better processing speeds
- Currently we should use a work-factor of 14

---

## Flask-Bcrypt

---

A much nicer API:

```py
>> from flask_bcrypt import Bcrypt

>> bcrypt = Bcrypt()
# We would get plain-text pw from form;
>> hash = bcrypt.generate_password_hash('user-pw')
>> hash
b'$2b$12$s....'
# We'd store this hash in our db.
>> bcrypt.check_password_hash(hash, 'user-pw')
True
```

In practice we register and authenticate with model methods:
[good-password-demo](flask-hashing-login-demo/goodpassword/models.py)

---

### Session storage

---

How can we make user data persist between pages?  
Browser session rears its head again!

```py
@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)
      ############ Ze' Magic ##############
        if user:
            session["user_id"] = user.id  # keep user logged in
            return redirect("/secret")
      ######################################
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login
```

We can check that a user is logged in a couple places:

### 1. Logic in [templates](flask-hashing-login-demo/goodpassword/templates/index.html):

```HTML
<ul>
  {% if 'user_id' not in session %}
    <li><a href="/register">Register</a></li>
    <li><a href="/login">Login</a></li>
  {% endif %}

  {% if 'user_id' in session %}
    <li><a href="/logout">Logout</a></li>
    <li><a href="/secret">Secret</a></li>
  {% endif %}
</ul>
NOTE We use this template logic to check for user priveleges
```

### 2. Logic in [view functions](flask-hashing-login-demo/goodpassword/app.py):

```py
@app.route("/secret")
def secret():
    """Example hidden page for logged-in users only."""

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:

        from werkzeug.exceptions import Unauthorized
        raise Unauthorized()

    else:
        return render_template("secret.html")
    # NOTE The template for secret does not check session
```

---

### User priveleges

---

We'll move onto the dummy twitter clone example  
Order-of-operations:

1. [Model](/flask-hashing-login-demo/VideoCode/auth_demo/models.py)  
   _The user model is identical to [good-password-demo](flask-hashing-login-demo/goodpassword/models.py)_

```py
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False,  unique=True)

    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

```

Registration test:

```py
u = User.register('big_dawg', 'random_pwd')
update_db(u)
```

Auth test:

```py
User.authenticate('big_dawg', 'random_pwd')
returns <User {id}>
```

2. [Form](/flask-hashing-login-demo/VideoCode/auth_demo/forms.py)  
   Super straightforward
3. [App](/flask-hashing-login-demo/VideoCode/auth_demo/app.py)
4. Template files

---

### Gating a page

---

First, make sure register and login BOTH add user_id to the session:  
[App](/flask-hashing-login-demo/VideoCode/auth_demo/app.py)

- Line 59, and 80 respectively

```py
@app.route('/tweets', methods=['GET', 'POST'])
def show_tweets():
  #  first check, blocks unlogged users
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    form = TweetForm()
    all_tweets = Tweet.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_tweet = Tweet(text=text, user_id=session['user_id'])

        update_db(new_tweet)

        flash('Tweet Created!', 'success')
        return redirect('/tweets')

    return render_template("tweets.html", form=form, tweets=all_tweets)
```

Logout is very simple. Remove user_id from session:

```py
@app.route('/logout', methods=['POST'])
def logout_user():
  session.pop('user_id')
  flash('Logged out')
  return redirect('/')
```

To send a post route ww hide a button in the nav-link:

```html
{% if session['user_id'] %}
<li class="nav-item">
	<form method="POST" action="/logout">
		<button class="btn btn-link nav-link pr-3 text-light" type="submit">
			Logout
		</button>
	</form>
</li>
```  
---
### Delete Permissions
---
Two parter:  
1. Render delete button based on user id - [tweets](flask-hashing-login-demo/VideoCode/auth_demo/templates/tweets.html)
```html
  <h5 class="card-title text-info">
        {{tweet.user.username}}
        {% if session['user_id'] == tweet.user_id %}
        <form style="display:inline;" action="/tweets/{{tweet.id}}" method="POST">
          <button class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></button>
        </form>
        {% endif %}
      </h5>
      <h6 class="card-subtitle mb-2 text-muted">Date goes here</h6>
      <p class="card-text">
        {{tweet.text}}
      </p>
```
2. Gate the delete route to protect against unauth reqs

```py
@app.route('/tweets/<int:id>', methods=["POST"])
def delete_tweet(id):
    """Delete tweet"""
    if 'user_id' not in session:
        flash("Please login first!", "info")
        return redirect('/login')
    tweet = Tweet.query.get_or_404(id)
    if tweet.user_id == session['user_id']:
        db.session.delete(tweet)
        db.session.commit()
        flash("Tweet deleted!", "success")
    else:
        flash("You don't have permission to do that!", "danger")
    return redirect('/tweets')
```
### Errors
If we pass a username in that has been taken we get:  
```py
sqlalchemy.exc.IntegrityError
```
To handle this we can import it, and raise an exception!
```py
from sqlalchemy.exc import IntegrityError

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
########################################################
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
########################################################
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/tweets')
```