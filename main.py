#COMCOP

import glob
import argparse
import csv
import numpy
from searcher import Searcher

#Toma todos los archivos cvs de la carpeta dateset y los resume en uno solo
#Ejemlo:
#python3 main.py -d dataset/agricola -i base.csv -a objetivo.csv

"""
Para la evaluación del riesgo, se comparará la empresa objetivo
con algunas empresas del sector, es por ello que se van a generar bases
de datos por cada rengión económico.
 
"""

def norm_sig(sig):#Funcion para normalizar un conjunto de datos nxm

    vector=[]
    normsigSTR=[]
    Reader=csv.reader(sig)
    for row in Reader:
        for j in row:
            vector.append(float(j))
    maximo=max(j)
        #vector.extend(float(row))  
    #print (vector)
    #Escalar valores de amplitud entre -1 y 1
    for i in vector:
        normsigSTR.append(str(float(i)/float(maximo)))
    return normsigSTR

ap= argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="Carpeta que contiene historiales de referencia")
ap.add_argument("-i", "--index", required=True, help="donde se entregaran los indicadores de riesgo")
ap.add_argument("-a", "--analisis", required=True, help="Empresa u organizacion objetivo")

args=vars(ap.parse_args())
output=open("Resultados/"+args["index"],"w") #Conjjunto de datos de topdas las empresas sintetizado en una sola matriz

vectorM=[]#Vector generado a partir de los datos de la empresa a relacionar.
with open("objetivo.csv") as nueva:
    Reader=csv.reader(nueva)
    for row in Reader:
        dimnueva=len(row)
        vectorM =norm_sig(nueva)
        

for i in glob.glob(args["dataset"]+"/*.csv"):
    csvid=i[i.rfind("/"+args["dataset"])+1:]
    vectorH=[]
    with open(csvid) as empresa: 
        empresanormalizada=norm_sig(empresa)
        output.write("%s,%s\n" % (csvid, ",".join((empresanormalizada))))

output.close()
features=[]
for i in vectorM:
    features.append(float(i))


searcher = Searcher("Resultados/"+args["index"])
results = searcher.search(features)

output=open("Resultados/Resultados.csv","w") #Aqui se va a almacenar la empresa con mayor correlacion 
correlacionada=results[1][1]
Conclusion=[]
with open(correlacionada) as empresa:
    for row in empresa:
        Conclusion.append(row)
    output.write("%s\n" % ("".join((Conclusion))))

