# canopto

canopto is a tool to sync course files and videos from the Canvas LMS hosted by the National
University of Singapore (NUS). Files are downloaded using the Canvas LMS Rest APIs, while videos are
obtained from Panopto, which NUS uses to store course videos.
**Credentials are only used for authenticating with NUS Canvas servers.**

Contributions and suggestions are welcome!

## Usage

- Open a terminal window (Linux/MacOS)
- For windows, open a command prompt (search for `cmd` in the search bar)
- Enter the following command

```commandline
canopto
```

If using the executable for windows, simply double click to launch it.

## Installation

### Install using Python/pipx

- If you have python3 on your computer, are using an OS that has it by default (MacOS, Linux)
- pipx is recommended over directly using pip to install canopto, to run it in an isolated environment.
- For the commands below, use `python3` or `python` if one does not work.
- Similarly, `pip3` or `pip`
- You can easily upgrade using `pipx upgrade canopto`

#### Windows and Linux

```commandline
python -m pip install --user pipx
python -m pipx ensurepath
pipx install canopto
pipx upgrade canopto 
```

- You might need to close the current cmd window and open a new one after running `python -m pipx ensure path`

#### MacOS

  ```commandline
  brew install pipx
  pipx ensurepath
  pipx install canopto
  pipx upgrade canopto
  ```

### Download from executable

TODO

## Running from the source

```commandline
git clone https://github.com/theresurgence/canopto
cd canopto
python -m venv venv
source venv/bin/activate  # Linux or MacOS
source venv/Scripts/activate # Windows
pip install -r requirements.txt
python src/canopto/
```

## FAQ

**1. How are my login credentials stored?**

- Your username and password is stored locally and securely on your computer using the python keyring library.
  For more information please check out [keyring]('https://pypi.org/project/keyring/').
- **Credentials are only used for authenticating with NUS Canvas servers.**

**2. Video downloads seem to take very long!**

- Videos can be large, and can easily be a few hundred MBs each. Please wait patiently.

**3. If my download is interrupted, can I continue from where I left off?**

- Yes, you can end downloads abruptly and resume them at any time.
  Partially downloaded files have a `.part` file extension, which will be removed
  once the download is fully complete.

**4. Will my annotated files be overwritten?**

- No, if the file has been full downloaded to your computer (no more `.part` extension), it will be ignored.

