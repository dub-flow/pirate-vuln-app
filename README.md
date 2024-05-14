# Pirate-themed Vulnerable App

This app is intentionally vulnerable!

# Setup

### Docker Compose (Only 1 Command!)

* Simply run `docker-compose up` and visit `http://localhost:80`

### Manually

* Install the Python dependencies: 
    - `pipenv shell`
    - `pipenv install`
* Run the Python API via `python3 app.py`
* Run Nginx via `docker run --name my-nginx -p 80:80 -v ./nginx.conf:/etc/nginx/nginx.conf:ro -d nginx`

# Vulnerabilities

### Vulnerability 1: Exposed Files

* We run `gobuster dir -u http://localhost -w ./wordlists/1.txt` 
* Looking at the output, we find `/pirates` exposed
* We visit `http://localhost/pirates` and find `http://localhost/pirates/treasure.txt`

### Vulnerability 2: Host Header Injection in Password Reset

* Send a `POST` request like:

```
POST /reset-password HTTP/1.1
Host: attacker.com
Content-Length: 25

{"email":"test@test.com"}
```

### Vulnerability 3: IDOR in the Loot Function

* Check out the 'Loot' functionality and realize that you can access, without authentication, any loot if you know the `id`
* Check out the `production.log` again and find the `id` of the `admin` user

### Vulnerability 4: Admins can Execute OS Commands

* This is of course only like god-level bad if we can take over an admin account... So that's what we're gonna do here
* First, we find the admin's `sessionId` in the `production.log` and then run commands

### Vulnerability 5: XSLT Injection

* Use the `Transform XML with XSLT` functionality
* Upload a file and take the `./resources/injection-read-file.xslt`, and observe that the `/etc/passwd` file was returned

# Vulnerability 6: BAC in Change Password

* Realize that you can change another user's password if you provide their email address
* This means you can change any users' password