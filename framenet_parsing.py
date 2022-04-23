#!/usr/bin/env python
# coding: utf-8


# ## Step 1
# ### Ingest TUPA annotation and extract P, S, A, D, E and C elements


#################################
# ## Step 2:
# ### Collect all the frame names and their frame elements from the lemma
# transform verb from ucca to lemma form


## Function 1- for a given word, convert to lemma, then get all frames and frame elements for it
def get_frames(word):
   
    from nltk.corpus import framenet as fn
    from nltk.stem.wordnet import WordNetLemmatizer
    import pandas as pd
    
    lemma = WordNetLemmatizer().lemmatize(word,'v')

    fr_names = []
    fr_elements = []
    
    for i in fn.frames_by_lemma(lemma): 
        fr_name = i.name
        fr_e = i.FE.keys() # does not seem to be a away to extract only the core frame elements in a frame but might be most efficient...?
        fr_names.append(fr_name)
        fr_elements.append(fr_e)
    
    names_df = pd.DataFrame(fr_names)    
    names_df.columns = ['frame_name']
    elements_df = pd.DataFrame(fr_elements)
    
    # Store as a dataframe, but maybe should be in a dictionary?
    fr_df = pd.concat([names_df, elements_df], axis = 1)

    return fr_df



# ## Step 2
# function to map ucca and frame/frame elements in progress



# dictionary
# key = sentence
# for every verb, has the position, 
# frame element, position
# output a graph with p swapped out in favor of the frame element on frame elements

