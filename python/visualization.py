# Alex Olwal, 2020, olwal.com
# Visualization functions to generate Altair charts

import altair as alt
import pandas as pd

import altair_saver
from altair_saver import save

"""## Multi-plot, comparing countries"""

def getMultiPlotsMatrix(data, dateRange, showVsPlots = True):

  WIDTH = 800
  HEIGHT = WIDTH
  N_SUBCHARTS = 3
  WS = WIDTH/N_SUBCHARTS
  HS = HEIGHT/N_SUBCHARTS

  doExportIntermediate = False
  
  dataAverage = data.groupby('Country').rolling(window=7, on='Date').mean()
#  data_country_diff[data_country_diff < 0] = 0
#  data_country_diff[data_country_diff.isna()] = 0
#  data_country_diff = data_country_diff.droplevel(0) # remove duplicate Country index created by groupby
  dataAverage = dataAverage.reset_index()
  
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
  suffixes = [ "/7-day average/million people", "/7-day average", " (total)/million people", " (total)" ]

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
    
    chartConfirmed = base.encode(opacity=alt.condition(selection, alt.value(1), alt.value(0.2)), y=alt.Y('Confirmed', axis=alt.Axis(title=''))).properties(title='Confirmed' + suffix, width = WS, height = HS)
  #  row |= base.encode(opacity=alt.condition(selection, alt.value(1), alt.value(0.2)), y=alt.Y('Active', axis=alt.Axis(title='')), x=alt.X('Date', axis=alt.Axis(title=''))).properties(title='Active')
    chartDeaths = base.encode(y=alt.Y('Deaths', axis=alt.Axis(title=''))).properties(title='Deaths' + suffix, width = WS, height = HS)
    chartRecovered = base.encode(y=alt.Y('Recovered', axis=alt.Axis(title=''))).properties(title='Recovered' + suffix, width = WS, height = HS)
    
    row |= chartConfirmed
    row |= chartDeaths
    row |= chartRecovered

    if (doExportIntermediate):
      chartConfirmed.save('Confirmed' + str(i) + ".svg")
      chartDeaths.save('Deaths' + str(i) + ".svg")
      chartRecovered.save('Recovered' + str(i) + ".svg")
    
    multiChart &= row

  if showVsPlots:
    row = alt.hconcat()
    row |= base.encode(y=alt.Y('Recovered', scale = alt.Scale(type='linear')), x='Deaths').properties(title='Recovered vs. Deaths' + suffix, width=WIDTH/2, height=HEIGHT/2)
    row |= base.encode(y='Confirmed', x='Deaths').properties(title='Confirmed vs. Deaths' + suffix, width=WIDTH/2, height=HEIGHT/2)
    multiChart &= row
   
  return multiChart

def getCountryPlotsDual(data, dateRange, index = 0):

  WIDTH = 800
  HEIGHT = WIDTH
  N_SUBCHARTS = 2
  WS = WIDTH/N_SUBCHARTS
  HS = HEIGHT/N_SUBCHARTS

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
              title = "Total"
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
  chart7Day.title = "7-day average (Daily values in light color)"

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
  return {
    'config': {
      'view': {
        'strokeWidth' : 0
      },
      'axis': {
          'grid': False,
          'ticks': False,
          'domainColor': 'lightgray',
          'labelFont': 'Roboto Condensed',
          'titleFont': 'Roboto Condensed',
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
        'font': 'Roboto Condensed',
        'fontWeight': 'normal'
      },
      'legend': {
        'labelFont': 'Roboto Condensed',
        'title': None
      }
    }
  }
