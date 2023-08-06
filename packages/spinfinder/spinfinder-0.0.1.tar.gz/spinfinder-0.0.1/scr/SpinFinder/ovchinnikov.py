#!/usr/bin/env python
# coding: utf-8

# In[1]:


def spin_finder(PATH):
    from rdkit import Chem
    from openbabel import pybel
    import pandas as pd
    m = Chem.MolFromSmiles(next(pybel.readfile("xyz",PATH)).write(format="smi").split()[0].strip())
    A=Chem.rdmolops.GetAdjacencyMatrix(m)
    q=pd.DataFrame(A)
    q=q.rename(columns={0:'↑'},index={0:'↑'})
    for r in range(len(q)):
        for u in range(len(q.iloc[r])):
            try:
                if q.iloc[r][u]==1 and q.index[r]=='↑':
                    q=q.rename(index={u:'↓'},columns={u:'↓'})
                elif q.iloc[r][u]==1 and q.index[r]=='↓':
                    q=q.rename(index={u:'↑'},columns={u:'↑'})
            except:
                q
    count = {}
    for i in list(q.columns):
        if not i in count:
            count[i] = 1
        else:
            count[i] +=1
    return(abs(count['↑']-count['↓'])+1)


