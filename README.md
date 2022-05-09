# SR4NLP_Project
FrameNet + UCCA - Open-SESAME = Project

# Setup
## Running TUPA

I used PipEnv as a (somewhat) reliable compatibility manager for the Python packages of the project. The project runs on Python 3.7 - this is enforced by TUPA. So first one needs to install Python 3.7, then PipEnv for the corresponding version of Python, which on Linux is done by 

```
/usr/bin/python3.7 -m pip install pipenv
```

Then, a new python environment can be easily created by running the following command in the root directory of the project

```
pipenv install
python -m spacy download en_core_web_lg
```

Once that's done, TUPA should be installed and ready to run, please look at the instruction on TUPA's repository to load and run some pre-trained models.

* Note: Depending on your environment setup you may have to do the en_core_web_lg download from the root directory of your python install.

## Open-SESAME
This is included just for general information on the planned methodology. Our attempts to successfully incorporate it failed due to model accuracy issues. Please note that it takes 4+ days to train the models, and they are system specific (non-transferable).

https://github.com/swabhs/open-sesame

We included Open-SESAME with the intention that a user would be able to parse any sentence through TUPA and FrameNet and merge them together using our code into a graph structure. However, despite acheiving a theoretical state of the art score of 71% in the original study for Open-SESAME, we were only ever able to achieve ~40% accuracy which introduced an unacceptable level of errors into our experiment from the very beginning. Future work on successfully implementing Open-SESAME would greatly expand the capabilities of our project by removing the limitation on using pre-annotated FrameNet sentences. However, given the limited timeline of this project we regretfully had to move forward without it.

## NLTK
NLTK is used to access the FrameNet elements through the built in FrameNet API. We 

'''
pipenv install ntlk
'''

## NetworkX
Used to build the graph representations and visualizations as well as traverse the graph structure for the merging operations.

'''
pipenv install networkx
'''

# Our Work - High Level Overview
![proposed_framework](https://github.com/PierreTsr/SR4NLP_Project/blob/main/srnlp_resized.png)

### Insert the actual steps here as a high level overview (1 to 2 sentences per step)
