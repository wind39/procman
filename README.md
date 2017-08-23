# procman

Run several process on multiple machines

# 1. Introduction

`procman` stands for **Process Manager**. It allows you to run Python scripts on
any computer that:

- You have access to;
- Has Python >= 3.5 installed;
- Has `procman` installed;
- Has `procman listener` running;
- Has the Python script of interest in the folder `procman/run`.

# 2. Installation

```
sudo apt install git make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv install 3.5.2

git clone https://github.com/wind39/procman
cd procman

pyenv local 3.5.2

pip install pip --upgrade
pip install -r requirements.txt
```

# 3. Basic setup

# 4. Running a Python script remotely

# 5. Scheduling a Python script to be run every X seconds
