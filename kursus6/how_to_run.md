# Install dependencies in an virtual Python env

1. Setup a virtual environment called `.venv`
    ```
    $ python3 -m venv .venv
    ```
2. Activate the virtual environment
    ```
    $ source .venv/bin/activate
    ```
    > You can check which Python you are using with `which python3`
3. Install PLY
    ```
    pip install ply
    ```

# How to run it
```bash
python3 main.py schweigi_source_code.txt
```