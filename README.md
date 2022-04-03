# SR4NLP_Project
FrameNet + UUCA = Project


## Running TUPA

I used PipEnv as a (somewhat) reliable compatibility manager for the Python packages of the project. The project runs on Python 3.6 - this is enforced by TUPA. So first one needs to install Python 3.6, then PipEnv for the corresponding version of Python, which on Linux is done by 

```
/usr/bin/python3.6 -m pip install pipenv
```

Then, a new python environment can be easily created by running the following command in the root directory of the project

```
pipenv install
```

Once that's done, TUPA should be installed and ready to run, please look at the instruction on TUPA's repository to load and run some pre-trained models.
