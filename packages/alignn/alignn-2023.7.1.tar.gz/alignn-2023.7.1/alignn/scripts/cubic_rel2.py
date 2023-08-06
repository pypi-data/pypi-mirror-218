from jarvis.core.atoms import Atoms
import pandas as pd
# from jarvis.core.graphs import Graph
from alignn.ff.ff import (
    default_path,
    ev_curve,
    surface_energy,
    vacancy_formation,
    ForceField,
    fd_path,
    get_interface_energy,
)
from jarvis.db.jsonutils import loadjson
from jarvis.db.figshare import data
d=loadjson('data_1.json')

model_path = "/wrk/knc6/ALINN_FC/FD_mult/temp_new"
model_path=fd_path() #default_path()
model_path=default_path()
def relax(model_path=[]):
    for i in d:
        atoms=Atoms.from_dict(i['atoms'])
        material=i['material']
        crys=i["Crystal structure"]
        a=i['a']
        print(material,crys,a) 
        ff = ForceField(
            jarvis_atoms=atoms,
            model_path=model_path,
            stress_wt=0.2,
            force_multiplier=1,
            force_mult_natoms=False,
        )
        opt, en, fs = ff.optimize_atoms()#logfile=None)

relax(model_path=model_path) 
