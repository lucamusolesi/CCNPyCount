import os
import sys
import numpy as np
import scipy
import pylab
import pymorph
import mahotas
from scipy import ndimage


def count_nuclei(filename):
	full = filename #nome immagine da analizzare
	empty = '/home/luca/isac/black-cut.bmp' #immagine vuota di riferimento
	img = '/home/luca/isac/tmp/'+filename+'.jpg'	#nome del file da creare con imagemagick
	imagemagick= "compare -metric AE -fuzz 8% " +empty+" "+full+" "+ " -highlight-color White -lowlight-color Black " + img #good values 5-6-7-8%
	os.system(imagemagick) #esegue il comando di imagemagick creando il file ccnx.jpg per l'immagine corrente

	ccn = mahotas.imread(img) #carica l'immagine creata con imagemagick
	ccnf = ndimage.gaussian_filter(ccn, 10) #applica un filtro gaussiano con SD=10 all'immagine
	rmax = pymorph.regmax(ccnf) #trova i massimi locali nell'immagine
	seeds,nr_nuclei=ndimage.label(rmax) #conta i massimi locali dell'immagine filtrata

	return nr_nuclei

imgdir = raw_input("Cartella delle immagini: \n") #Cartella da analizzare
fileout = raw_input("Nome file dove salvare i dati: \n") #Nome file dove verranno salvati i conteggi


os.chdir(imgdir)

# Lista delle subdirectory della directory corrente
cartelle=os.listdir('.')
cartelle.sort() # Ordina la lista delle cartelle

datigiorno = []
for a in cartelle:
# Change the current directory
	os.chdir(a)

# Save names of the files in the directory in an array
	files = os.listdir('.')
	files.sort()
# Ritaglia le immagini per avere solo il volume desiderato
#imagemagick_crop = "for i in *.bmp; do convert $i -crop 640x150+0+200 $i; done"
#os.system(imagemagick_crop)

	nuclei_per_img = []
	#nuclei_per_img.append(a)
	for i in files:
		nuclei_per_img.append(count_nuclei(i))
	
	#nuclei_per_img.append(np.mean(nuclei_per_img)) ################## media dei nuclei di TUTTE le immagini di una prova
	#nuclei_per_img.append(a) ##################### 
	nuclei_per_img.insert(0, a) #Per inserire a come primo elemento

	datigiorno.append(nuclei_per_img)

	os.chdir('..')
os.chdir('..')
###
#Scrivi su file con funzioni standard
###
#filedati=open("nomefile", "w")
#nomefile.writelines('\n'.join(map(str, nuclei_per_img)+'\n'))
#nomefile.close()

###
#Scrivi su file in colonne con numpy ----> from numpy import *
###
#Creare una lista di colonne
dataout = np.column_stack((datigiorno))
#
#Scrivi colonne o righe su file dataout per scrivere colonne e datigiorno per scrivere righe
np.savetxt(fileout, dataout, fmt=('%s')) # i sta per interi, s sta per stringhe
#
#Se al posto di una column_stack si usa una lista di liste si scrivono le liste in righe sul file



#print cartelle
#print datigiorno
#print files



	# //Find the max or the mean or whatever value of the list and save it in a file
	# //...
	# //...
	# // Day Dir_name CCN_number
	
# Go to the next directory to examinate 


