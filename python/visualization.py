# Alex Olwal, 2020, olwal.com
# Visualization functions to generate Altair charts

import altair as alt
import pandas as pd

import altair_saver
from altair_saver import save

"""## Multi-plot, comparing countries"""

def getMultiPlotsMatrix(data, dateRange, showVsPlots = True, doExportIntermediate = False):

  print ("MultiPlotsMatrix, Date range: " + str(dateRange[0]) + ":" + str(dateRange[1]))

  WIDTH = 800
  HEIGHT = WIDTH
  N_SUBCHARTS = 3
  WS = WIDTH/N_SUBCHARTS
  HS = HEIGHT/N_SUBCHARTS
  
  dataAverage = data.groupby('Country').rolling(window=7, on='Date').mean()
#  data_country_diff[data_country_diff < 0] = 0
#  data_country_diff[data_country_diff.isna()] = 0
#  data_country_diff = data_country_diff.droplevel(0) # remove duplicate Country index created by groupby
  dataAverage = dataAverage.reset_index()

  # Clip negative values to 0
  dataAverage['Confirmed'] = dataAverage['Confirmed'].clip(lower=0)
  dataAverage['Deaths'] = dataAverage['Deaths'].clip(lower=0)
  dataAverage['Recovered'] = dataAverage['Recovered'].clip(lower=0)
  dataAverage['ConfirmedDelta'] = dataAverage['ConfirmedDelta'].clip(lower=0)
  dataAverage['DeathsDelta'] = dataAverage['DeathsDelta'].clip(lower=0)
  dataAverage['RecoveredDelta'] = dataAverage['RecoveredDelta'].clip(lower=0)
  dataAverage['ConfirmedDelta/M'] = dataAverage['ConfirmedDelta/M'].clip(lower=0)
  dataAverage['DeathsDelta/M'] = dataAverage['DeathsDelta/M'].clip(lower=0)
  dataAverage['RecoveredDelta/M'] = dataAverage['RecoveredDelta/M'].clip(lower=0)
  dataAverage['Confirmed/M'] = dataAverage['Confirmed/M'].clip(lower=0)
  dataAverage['Deaths/M'] = dataAverage['Deaths/M'].clip(lower=0)
  dataAverage['Recovered/M'] = dataAverage['Recovered/M'].clip(lower=0)
  
  dataAverageM = dataAverage[['Date', 'Country', 'ConfirmedDelta/M', 'RecoveredDelta/M', 'DeathsDelta/M']]
  dataAverageM = dataAverageM.rename(columns={'ConfirmedDelta/M':'Confirmed', 'RecoveredDelta/M':'Recovered', 'DeathsDelta/M':'Deaths'})
   
  dataAverage = dataAverage[['Date', 'Country', 'ConfirmedDelta', 'RecoveredDelta', 'DeathsDelta']]
  dataAverage = dataAverage.rename(columns={'ConfirmedDelta':'Confirmed', 'RecoveredDelta':'Recovered', 'DeathsDelta':'Deaths'})
   
  dataM = data[['Date', 'Country', 'Confirmed/M', 'Recovered/M', 'Deaths/M']]
  dataM = dataM.rename(columns={'Confirmed/M':'Confirmed', 'Recovered/M':'Recovered', 'Deaths/M':'Deaths'})
 
#  selection = alt.selection_single(on='mouseover', fields=['Country'], nearest=True)#, bind='legend')
  selection = alt.selection_multi(fields=['Country'], bind='legend')

  multiChart = alt.vconcat()

  dataSources = [ dataAverageM, dataAverage, dataM, data ]
  updated =  "[" + str(dateRange[1]) + "]"
  suffixes = [ "/7-day average/million people\n", "/7-day average", " (total)/million people", " (total)" ]
  types = ['Confirmed', 'Deaths', 'Recovered']

  for i, data in enumerate(dataSources):

    suffix = suffixes[i]

    # Create the base chart
    base = alt.Chart(data).mark_line().encode( 
            color='Country',
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
            tooltip = ['Date', 'Country', 'Confirmed', 'Recovered', 'Deaths'],
            #x = alt.X('Date', axis=alt.Axis(title=''))
            x = alt.X('Date', axis=alt.Axis(title=''), scale=alt.Scale(domain=dateRange))

            ).add_selection(
              selection
            ).interactive(
            )

    row = alt.hconcat()
    
    
    for type in types:
      title = [ type + suffix, updated ]
      chart = base.encode(opacity=alt.condition(selection, alt.value(1), alt.value(0.2)), y=alt.Y(type, axis=alt.Axis(title=''))).properties(title=title, width = WS, height = HS)
      row |= chart
      
      if (doExportIntermediate):
        filename = (type + "_" + str(i) + ".svg").lower()
        print ('Saving: ' + filename)
        chart.save(filename)
    
    multiChart &= row

  if showVsPlots:
    row = alt.hconcat()
    row |= base.encode(y=alt.Y('Recovered', scale = alt.Scale(type='linear')), x='Deaths').properties(title='Recovered vs. Deaths' + suffix, width=WIDTH/2, height=HEIGHT/2)
    row |= base.encode(y='Confirmed', x='Deaths').properties(title='Confirmed vs. Deaths' + suffix, width=WIDTH/2, height=HEIGHT/2)
    multiChart &= row
   
  return multiChart

def getMultiPlotsMatrixDeaths(data, dateRange, width = 800, height = 600, showVsPlots = False, doExportIntermediate = False):

  print ("MultiPlotsMatrix, Date range: " + str(dateRange[0]) + ":" + str(dateRange[1]))

  WIDTH = width
  HEIGHT = height
  N_SUBCHARTS = 3
  WS = WIDTH
  HS = HEIGHT/N_SUBCHARTS
  
  dataAverage = data.groupby('Country').rolling(window=7, on='Date').mean()
#  data_country_diff[data_country_diff < 0] = 0
#  data_country_diff[data_country_diff.isna()] = 0
#  data_country_diff = data_country_diff.droplevel(0) # remove duplicate Country index created by groupby
  dataAverage = dataAverage.reset_index()

  # Clip negative values to 0
  dataAverage['Deaths'] = dataAverage['Deaths'].clip(lower=0)
  dataAverage['DeathsDelta'] = dataAverage['DeathsDelta'].clip(lower=0)
  dataAverage['DeathsDelta/M'] = dataAverage['DeathsDelta/M'].clip(lower=0)
  dataAverage['Deaths/M'] = dataAverage['Deaths/M'].clip(lower=0)
  
  dataAverageM = dataAverage[['Date', 'Country', 'DeathsDelta/M']]
  dataAverageM = dataAverageM.rename(columns={'DeathsDelta/M':'Deaths'})
   
  dataAverage = dataAverage[['Date', 'Country', 'DeathsDelta']]
  dataAverage = dataAverage.rename(columns={'DeathsDelta':'Deaths'})
   
  dataM = data[['Date', 'Country', 'Deaths/M']]
  dataM = dataM.rename(columns={'Deaths/M':'Deaths'})
 
#  selection = alt.selection_single(on='mouseover', fields=['Country'], nearest=True)#, bind='legend')
  selection = alt.selection_multi(fields=['Country'], bind='legend')

  multiChart = alt.vconcat()

  dataSources = [ dataAverageM, dataM ]
  updated =  "[" + str(dateRange[1]) + "]"
  calculations = [ "Deaths | 7-day average/million people", "Deaths | Total/million people", " (total)" ]
  types = ['Deaths']

  for i, data in enumerate(dataSources):

    # Create the base chart
    base = alt.Chart(data).mark_line().encode( 
            color='Country',
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
            tooltip = ['Country', 'Date', 'Deaths'],
            #x = alt.X('Date', axis=alt.Axis(title=''))
            x = alt.X('Date', axis=alt.Axis(title=''), scale=alt.Scale(domain=dateRange))

            ).add_selection(
              selection
            ).interactive(
                bind_y = False
            )

    row = alt.hconcat()
        
    for type in types:     
      dateString = "(" + dateRange[0].replace("-", " ") + " - " + dateRange[1].replace("-", " ") + ")"
      title = [ calculations[i], dateString ]
      chart = base.encode(opacity=alt.condition(selection, alt.value(1), alt.value(0.2)), y=alt.Y(type, axis=alt.Axis(title=''))).properties(title=title, width = WS, height = HS)
      row |= chart
      
      if (doExportIntermediate):
        filename = (type + "_" + str(i) + ".svg").lower()
        print ('Saving: ' + filename)
        chart.save(filename)
    
    multiChart &= row
   
  return multiChart


def getCountryPlotsDual(data, dateRange, index = 0):

  print ("CountryPlotsDual, Date range: " + str(dateRange[0]) + ":" + str(dateRange[1]))

  WIDTH = 800
  HEIGHT = WIDTH
  N_SUBCHARTS = 2
  WS = WIDTH/N_SUBCHARTS
  HS = HEIGHT/N_SUBCHARTS

  updated = "[" + str(dateRange[1]) + "]"
  
  dataDelta = data[['Date', 'Country', 'ConfirmedDelta', 'RecoveredDelta', 'DeathsDelta']]
  dataDelta = dataDelta.rename(columns={'ConfirmedDelta':'Confirmed', 'RecoveredDelta':'Recovered', 'DeathsDelta':'Deaths'})

  dataDeltaAverage = data.groupby('Country').rolling(window=7, on='Date').mean()
#  data_country_diff[data_country_diff < 0] = 0
#  data_country_diff[data_country_diff.isna()] = 0
#  data_country_diff = data_country_diff.droplevel(0) # remove duplicate Country index created by groupby
  dataDeltaAverage = dataDeltaAverage.reset_index()

  dataDeltaAverage = dataDeltaAverage[['Date', 'Country', 'ConfirmedDelta', 'RecoveredDelta', 'DeathsDelta']]
  dataDeltaAverage = dataDeltaAverage.rename(columns={'ConfirmedDelta':'Confirmed', 'RecoveredDelta':'Recovered', 'DeathsDelta':'Deaths'})

  dataTotal = data[['Date', 'Country', 'Confirmed', 'Recovered', 'Deaths']]

  countries = list(data['Country'].unique())

  input_dropdown = alt.binding_select(options=countries)
  selection = alt.selection_single(fields=['Country'], bind=input_dropdown, name='Select', init={'Country': countries[index]})

  chartTotal = alt.Chart(dataTotal).transform_fold(
            ['Recovered', 'Deaths', 'Confirmed'],
            as_= ['Type', 'Count']
          ).mark_line().encode( 
  #        y = alt.Y('Count:Q', axis=alt.Axis(format=',.2d', title=None)),
          y = alt.Y('Count:Q', ),
          tooltip = ['Date', 'Country', 'Confirmed', 'Recovered', 'Deaths'],
          x=alt.X('Date', axis=alt.Axis(format='%b %d'), scale=alt.Scale(domain=dateRange)), #https://github.com/d3/d3-time-format#locale_format
          color='Type:N',
          opacity=alt.value(0.7)
          ).add_selection(
            selection
          ).transform_filter(
            selection          
          ).properties(
              title = [ "Total", updated ]
          ).interactive(
          ).properties(width = WS, height = HS
          )

  chartDelta = alt.Chart(dataDelta).transform_fold(
            ['Recovered', 'Deaths', 'Confirmed'],
            as_= ['Type', 'Count']
          ).mark_line().encode( 
  #        y = alt.Y('Count:Q', axis=alt.Axis(format=',.2d', title=None)),
          y = alt.Y('Count:Q', ),

          x=alt.X('Date', axis=alt.Axis(format='%b %d'), scale=alt.Scale(domain=dateRange)), #https://github.com/d3/d3-time-format#locale_format        

          color='Type:N',
          opacity=alt.value(0.2)
          ).transform_filter(
            selection          
          ).interactive(
          ).properties(width = WS, height = HS
          )

  chartDeltaAverage = alt.Chart(dataDeltaAverage).transform_fold(
            ['Recovered', 'Deaths', 'Confirmed'],
            as_= ['Type', 'Count']
#          ).transform_window(
#          rolling_mean='mean(Count)',
#          frame=[-7, 0]
        ).mark_line().encode(
            color='Type:N',
            x=alt.X('Date', axis=alt.Axis(format='%b %d'), scale=alt.Scale(domain=dateRange)), #https://github.com/d3/d3-time-format#locale_format
            opacity=alt.value(1),
            y = 'Count:Q'
#            y='rolling_mean:Q'
        ).transform_filter(
            selection
        ).interactive(
        ).properties(width = WS, height = HS
        )

  chart7Day = chartDelta + chartDeltaAverage
#  countryDiff_chart.data = data_countryDiff
  chart7Day.title = [ "7-day average (light color: daily values)", updated ]

  chart = chart7Day | chartTotal

  return chart 

  
def getCountryPlot(countries):

  regular = alt.Chart(countries).mark_line().encode( 
          x = alt.X('Date', axis=alt.Axis(title='')),
          y='Deaths',
          color='Country'          
          ).interactive()
          
  data_country = countries.groupby('Country').rolling(window=7, on='Date').mean()
#  data_country[data_country < 0] = 0
#  data_country[data_country.isna()] = 0
  data_country = data_country.reset_index()

  countries = data_country
   
  week = alt.Chart(countries).mark_line().encode( 
          x = alt.X('Date', axis=alt.Axis(title='')),
          y='Deaths',
          color='Country'
          ).interactive().properties(width = WS, height = HS) 
          
  return regular + week
  

def activateTheme(viz):
  alt.themes.register('olwal', viz.olwalTheme)
  alt.themes.enable('olwal')
  
def olwalTheme():

  font = "Roboto Condensed"
    
  return {
    'config': {
      'view': {
        'strokeWidth' : 0
      },
      'axis': {
          'grid': False,
          'ticks': False,
          'domainColor': 'lightgray',
          'labelFont': font,
          'titleFont': font,
          'titleFontWeight': 'normal',
      },
      'axisY': {
        'grid': True,
          'labelBaseline': 'middle',
          'maxExtent': 45,
          'minExtent': 45,
          'tickSize': 2,
          'titleAlign': 'left',
          'titleAngle': 0,
          'titleX': -45,
          'titleY': -11,       
      },
      'title': {
        'font': font,
        'fontWeight': 'normal'
      },
      'legend': {
        'labelFont': font,
        'title': None
      }
    }
  }
