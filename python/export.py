# Alex Olwal, 2020, olwal.com
# Downloads data, generates charts and saves to disk in different formats

import altair as alt
import sys

import altair_saver
from altair_saver import save

import datasets
import visualization as viz

import os

CSV_COVID19 = "covid-19\\data\\time-series-19-covid-combined.csv"
CSV_POPULATION = "population\\data\\population.csv"

def loadDataAndExportVisualizations(path):

  d = datasets.Data()

  if (path == ""):
    d.load() #csvCovid19 = CSV_COVID19, csvPopulation = CSV_POPULATION)
  else:
    d.load(path) #, csvCovid19 = CSV_COVID19, csvPopulation = CSV_POPULATION)
    
  print("Exporting plots")
  exportPlots(d)

def exportPlots(d):

  print("Activating theme")
  viz.activateTheme(viz)
    
  nordicCountry = []

  for i in range(0, 5):
    nordicCountry.append(viz.getCountryPlotsDual(d.nordic, d.dateRange, i))

  nLargestCountry = viz.getCountryPlotsDual(d.n, d.dateRange)

  nordicMultiMatrix = viz.getMultiPlotsMatrix(d.nordic, d.dateRange)
  nLargestMultiMatrix = viz.getMultiPlotsMatrix(d.n, d.dateRange)
  
  types = [ 'json', 'svg', 'html' ]

#  !rm *.json *.svg *.png *.html

  for suffix in types:
    print("Exporting " + suffix)

    nordicMultiMatrix.save('nordic_multi_matrix.' + suffix)
    nLargestMultiMatrix.save('nlargest_multi_matrix.' + suffix)

    for i, c in enumerate(nordicCountry):
      c.save(d.NORDIC_COUNTRIES[i].lower() + '_country_plots.' + suffix)

    nLargestCountry.save('nlargest_country_plots.' + suffix)

  print("[OK]")
    
nArgs = len(sys.argv)

path = "" if nArgs < 2 else sys.argv[1] 

#os.getcwd() + "\\" + 

loadDataAndExportVisualizations(path)