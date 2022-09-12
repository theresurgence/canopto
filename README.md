# canopto

canopto is a tool to sync course files and videos from the Canvas LMS hosted by the National
University of Singapore (NUS). Files are downloaded using the Canvas LMS Rest APIs, while videos are
obtained from Panopto, which NUS uses to store course videos.

Contributions and suggestions are welcome.


## Installation

### Install using pipx
- If you have python3 on your computer, are using an OS that has it by default (MacOS, Linux)
    - pipx is recommended over directly using pip to install canopto, to run it in an isolated environment.

#### Windows
    -  If you installed python using the app-store, replace `python` with `python3` in the next line.
    ```sh
    python -m pip install --user pipx
    pipx install canopto
    ```

#### Linux
    ```sh
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    pipx install canopto
    ```

#### MacOS
    ```sh
    brew install pipx
    pipx ensurepath
    pipx install canopto
    ```

### Download from executable
    TODO



## Running from the source
    ```sh
    git clone https://github.com/theresurgence/canopto
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python src/canopto/
    ```



## FAQ

    1. How are my login credentials stored?
    Your username and password is stored locally and securely on your computer using the python keyring library.
    For more information please check out [keyring]('https://pypi.org/project/keyring/')
    **Credentials are only used for authenticating with NUS Canvas servers.**

    2. Video downloads seem to take very long!
    Videos can be large, and can easily be a few hundred MBs each. Please wait patiently.

    3. If my download is interrupted, can I continue from where I left off?
    Yes, you can end downloads abruptly and resume them at any time.
    Partially downloaded files have a `.part` file extension, which will be removed
    once the download is fully complete.

    4. Will my annotated files be overwritten?
    No, if the file has been full downloaded to your computer (no more `.part` extension), it will be ignored.

