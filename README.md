# SR4NLP_Project
FrameNet + UCCA - Open-SESAME = Project

# Motivation
UCCA captures a rich set of semantic distinctions, with formal representations as directed edge labeled graphs. In the graphs, nodes represent semantic concepts such as entities and relations, and edges represent categories such as Participant (A), Process (P), Elaborator (E) and Center (C). Texts are viewed as collections of scenes describing some movement or action, with different scenes being linked, or occurring conditionally or in parallel of one another. 

Frame semantics utilize frames, available in a resource called FrameNet, which describe the conceptual structure needed to understand a word. Frames describe the interactions among semantic roles, called frame elements, of which core and non-core types exist. Frames can be related to one another through inheritance and perspective. 

Both annotations have dedicated parsers. However, while UCCA is able to reach a decent accuracy with (TUPA - 79% F1), frame semantics parsing remains a very difficult task up to this day (OpenSesame - 71% F1 “theoretically”). This prompted the comparison of annotations on the same sentences using both parsers.


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
NLTK is used to access the FrameNet elements through the built in FrameNet API.

## NetworkX
Used to build the graph representations and visualizations as well as traverse the graph structure for the merging operations.

# Our Work - High Level Overview
![proposed_framework](https://github.com/PierreTsr/SR4NLP_Project/blob/main/srnlp_resized.png)

## Workflow Steps
1. Parse a sentence using TUPA to identify its UCCA annotation, focusing on Participant (A), Process (P), Elaborator (E) and Center (C). Visualize as a graph.
2. Refer to the pre-annotated FrameNet annotations for the sentence's FrameNet annotation, focusing on the Target (predicate).
3. Compare the UCCA and FrameNet annotations by focusing on the predicates of the sentence, typically labeled as P (Process) or S (Scene) in UCCA annotations and Target in FrameNet annotations. These elements will be most helpful in successfully merging the annotations. 
4. Using bottom-up graph search, align the UCCA P-edge with FrameNet Target to initiate the merge.
5. Traverse the resulting graph top-down to identify the UCCA scene elements and their relations to FrameNet's frame elements. 
6. Annotate the edges of this merged graph with the most probable frame element labels based on maximum token intersection.
7. To avoid propagating existing errors with the UCCA parser, the produced UCCA graphs are assumed to be correct and serve as a baseline for comparison. Since there are no existing datasets that contain both UCCA and FrameNet annotations, the proposed frame element labeling from the traversal of the merged graph must be compared to a manually-annotated representation.


