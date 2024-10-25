
## 1. Install MongoDB (Debian)
install guide: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-debian/

Start mongodb with:
```
sudo systemctl start mongod
```
And check with
```
systemctl status mongod
```
(Optional) You can disable mongod on startup via:
```
sudo systemctl disable mongod
```

# Install MongoDB Python API via virtual environment
1. Setup a virtual environment called `.venv`
    ```
    $ python3 -m venv .venv
    ```
2. Activate the virtual environment
    ```
    $ source .venv/bin/activate
    ```
3. Install dependencies
    ```
    pip install -r python/requirements.txt
    ```
