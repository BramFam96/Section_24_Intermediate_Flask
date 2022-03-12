# External API requests

Two ways to talk with an api:

- Client-side (AJAX)
- Server-side (Python)
  Either method simply makes http requests

## Client-side Model

---

<-> Resp/Req relationship  
_db_ <-> _Flask Server_ <-> **Browser** <AJAX RES/REQ> _External Api_  
Ajax can also make res/req to the flask server, but we'll cover this later  
We can easily handle client side requests without involving Flask  
storing our results on the other hand will require more steps!

## Server Side Model

---

**Browser** <-> _Flask Server_ <-> _External Api_ / _db_  
Server-side handles comms with Apis and db from flask itself  
Browser makes ajax requests from our server

### Why use Server side requests?

---

- Same-Origin Policy may prevent browser requests
- Easy to store/process data without ajax
- Need to hide access key for api
  - client-side requests are visible in dev tools

## Making requests via Python

---

We'll be using the iTunes API and a Py library called _requests_.

```SQL
pip install requests
```

### Get requests

```py
res = request.get('url', params= {})
print(res.json())
```
Both *.get()* and *.post()* return res instances  
.text, .status_code, .json

### Post requests
---
```py
requests.post(url,data/json); 
```
Some api require json, but most now support data obj as well
```py
requests.post(dummy_url, data = {'username': 'user', 'password': 'nonsense', 'msg':'Yowww'})
The raw data for this req looks like:
username=user&msg=Yowww%str len
```
To send **json** instead, we simply change kw *data* to *json*  
We should do this by default  

## API Keys / Secrets
Most API's require keys, some even require an additional 'secrets' obj  
Some apis expect this key in the url params, but this is **not** guarenteed;
Check documentation, keyed apis typically have very good docs!  
## Keeping Keys / Secrets a secret!
---
The simplest method of keeping keys secret:  
add key to seperate file, import it, and add it to git ignore!

## Mapquest demo
---
We'll be using mapquest's free api to get geocoding information 