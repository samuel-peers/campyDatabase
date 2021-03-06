# -*- coding: latin-1 -*-
"""
 create projTriples
"""

import pandas as pd
import re
from .. import cleanCSV as cn
from .campyTM import CAMPY as ctm

def createProjTriples(df, row, isoTitle):

    resultTriple = ""

    projTriple = ""

    isoTriple = ""

    proj = df["Dataset ID_1"][row]

    subproj = df["Dataset ID_2"][row]

    # Whether an isolate is a reference strain or not is stored in the 'Dataset ID_1' column
    # (proj variable), and usually in subsequent columns, but not always.
    if re.search("[Rr]eference[ -_][Ss]train", proj) is None:

        if not pd.isnull(proj) and cn.isGoodVal(proj):

            projTriple += ctm.indTriple(proj, "Project") +\
                          ctm.propTriple(proj, {"hasName":proj}, True)

            isoTriple += ctm.propTriple(isoTitle, {"partOfProject":proj})

            if not pd.isnull(subproj) and cn.isGoodVal(proj):

                for c in " _":

                    # Split by '-',' ', or '_' if it's preceded by at least 2 characters,
                    # we don't want to remove 'C' when the project = C-Enternet for example.
                    toRem = re.split("(?<= ..)[- _]", proj)

                    for r in toRem:

                        subproj = subproj.replace(r, "")
                        subproj = subproj.strip()

                    # Remove all the '-',' ', and '_' if they are NOT preceded by a character
                    subproj = re.sub("(?<!.)[- _]", "", subproj)

                    # Handle the french characters
                    subproj = re.sub("H...pital","Hôpital",subproj)
                    subproj = re.sub("^...t... ","Été ",subproj)

                if subproj:

                    # Some of the subprojects are years
                    subproj = cn.cleanInt(subproj) if cn.isNumber(subproj) else subproj 

                    projTriple += ctm.indTriple(subproj, "Sub_project")
                    projTriple += ctm.propTriple(subproj, {"hasName":subproj}, True)
                    projTriple += ctm.propTriple(proj, {"hasSubproject":subproj})

                    isoTriple += ctm.propTriple(isoTitle, {"partOfSubProject":subproj})

    resultTriple += isoTriple + projTriple

    return resultTriple
