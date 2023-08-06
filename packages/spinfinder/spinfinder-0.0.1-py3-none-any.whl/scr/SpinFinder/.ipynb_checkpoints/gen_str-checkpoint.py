#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import os.path
import glob
import tempfile
from itertools import combinations
import pandas as pd
import numpy as np
from openbabel import pybel
from rdkit import Chem
from rdkit.Chem import AllChem
from chemml.chem import Molecule
pybel.ob.obErrorLog.StopLogging()


# In[2]:


def xyz_to_smiles(file_xyz: str) -> str:
    mol = next(pybel.readfile("xyz", file_xyz))
    smi = mol.write(format="smi")
    return smi.split()[0].strip()


# In[3]:


def GANNA (inp_dir=None, out_dir=None,hetero_nr=1,iters=100):
    import os
    import os.path
    import glob
    import tempfile
    from itertools import combinations
    import pandas as pd
    import numpy as np
    from openbabel import pybel
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from chemml.chem import Molecule
    pybel.ob.obErrorLog.StopLogging()
    for o in glob.glob(inp_dir):
        frame=open(o)
        framework=frame.readlines()
        Nr_heteroatom=hetero_nr
# Generating structures

        xyz=[]
        smiles=[]
        canon_smiles=[]
        canon_smiles_tab=[]
        final_smiles=[]
        for element1 in framework:
            xyz.append(element1.split())
        df=pd.DataFrame(xyz[2:])
        t=[]
        for framework in range(len(df)):
            if df.loc[framework][0]=='H':
                t.append(framework)
        asd=df.drop(t)
        y = df[df[0]=='H']
        for index in list(combinations(asd.index,Nr_heteroatom)):
            asd.loc[index,0]='N'
            qas=[]
            for n in index:
                q=[]
                for i in t:
                    q.append(np.linalg.norm(np.array(asd.loc[n][1:]).astype('float') - np.array(y.loc[i][1:]).astype('float')))
                qas.append(pd.DataFrame(q,columns=['A']).astype('float').nsmallest(Nr_heteroatom,columns='A').index.array[0])
            Q=pd.DataFrame(y).reset_index()
            Q.drop(qas, axis=0, inplace=True)
            u=Q.pop('index')
            asd=pd.concat([asd,Q],axis=0)
    
# Generating SMILES
    
            with tempfile.TemporaryDirectory() as td:
                f_name = os.path.join(td, 'test.txt')
                with open(f_name, 'w') as fh:
                    fh.write(str(len(asd))+' \n\n'+asd.to_string(index=False,index_names=False,header=False))    
                smiles.append(xyz_to_smiles(fh.name))
            asd=df.drop(t)
        for i in range(30):
            for s in smiles:
                for ele in s:
                    if ele.isupper()==True:
                        smiles.remove(s)
                        break
                
# Rendering compounds according to the symetry

        for i in smiles:
            canon_smiles.append(Chem.CanonSmiles(i))
        C=pd.concat([pd.DataFrame(canon_smiles,columns=['canon']),pd.DataFrame(smiles,columns=['smiles'])],axis=1)
        for u in list(set(canon_smiles)):
            canon_smiles_tab.append(C.loc[C['canon'] == u].reset_index().iloc[[0]]['smiles'])

# Generating SMILES of unique compounds

        for t in canon_smiles_tab:
            final_smiles.append(t[0])
        for file in final_smiles:
            mol = Molecule(file, input_type='smiles')
            mol.hydrogens('add')
            mol.to_xyz(optimizer='MMFF', mmffVariant='MMFF94s', maxIters=iters

    return ('DONE!')


# In[ ]:




