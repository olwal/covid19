import pandas as pd

class Data(object):

  """
    Member variables:
      population # dataframe for population data set
      covid # dataframe for covid data set  
      dateRange # [startDate, endDate]
      
      # processed data frames with additional columns for {Recovered, Confirmed, Deaths} x {Delta, Delta/M, /M}
      n # dataframe for N_LARGEST countries 
      nordic # dataframe for NORDIC_COUNTRIES
  """
  
  N_LARGEST = 10
  NORDIC_COUNTRIES = ['Denmark', 'Finland', 'Iceland', 'Norway', 'Sweden' ]

  CSV_COVID19 = "covid-19/data/time-series-19-covid-combined.csv"
  CSV_POPULATION = "population/data/population.csv"
  PATH_DATASETS = "../data/datasets/"
      
#  def __init__(self):

  def load(self, pathDatasets = PATH_DATASETS, csvCovid19 = CSV_COVID19, csvPopulation = CSV_POPULATION):
  
    # Load and preprocess datasets
    population = self.loadPopulationData(pathDatasets, csvPopulation)
    covid = self.loadCovidData(pathDatasets, csvCovid19)
    
    # Get the date for most recent data
    endDate = max(covid['Date'])  
    startDate = pd.to_datetime(endDate) - pd.to_timedelta('30 days')
    # Remove the time part and convert back to string
    startDate = str(startDate.date())

    # Convert date column to a pd datetime data type
    covid['Date'] = pd.to_datetime(covid['Date'])
    
    # Get the data for the current date
    latest = covid[covid['Date'] == endDate]

    # Compute daily deltas and add as columns
    covid['RecoveredDelta'] = covid['Recovered'].diff()
    covid['DeathsDelta'] = covid['Deaths'].diff()
    covid['ConfirmedDelta'] = covid['Confirmed'].diff()
    
    # Compute data per column/population
    covid = self.getStatsPerMillion(covid, population)

    # Delete data before Mar 1, 2020 (inconsistencies, etc.)
    covid = covid[covid['Date'] >= '2020-03-01']
        
    # Extract the data for the countries with the N_LARGEST deaths
    countries = latest.nlargest(self.N_LARGEST, 'Deaths')['Country']
    n = covid[covid['Country'].isin(countries)] 
    # Remove all other territories
    n = n[n['Province'].isna()] 
    
    # Extract the data for the nordic countries
    nordic = covid[covid['Country'].isin(self.NORDIC_COUNTRIES)] 
    # Remove all other territories
    nordic = nordic[nordic['Province'].isna()] 

    # Store data with object
    self.population = population
    self.n = n
    self.nordic = nordic
    self.dateRange = [ str(startDate), str(endDate) ]
    self.covid = covid    
    
  def getStatsPerMillion(self, data, population):
    
    # Get a unique list of the countries to iterate over
    countries = data['Country'].unique()
    
    columns = ['Confirmed', 'Recovered', 'Deaths']
    suffix = "/M"
    suffixDelta = "Delta/M"
    
    # Create a copy of the columns, for in-place calculations
    for column in columns:
      data[column + suffix] = data[column]
      data[column + suffixDelta] = data[column + "Delta"]

      
    for country in countries:
      
      # Check there is a population entry for this country
      countryPop = population[population['Country'] == country]
      if (countryPop.empty):
        print ("\n[ Missing the year's population for " + country + " ]")
        continue

      # Get the population number from the data frame
      pop = countryPop.Value.values[0]/1000000

      print('.', end = '', flush = 'True')

      #      print (country, end='')
#      print (" " + str(pop), end='')
      
      for column in columns:
        data.loc[(data['Country'] == country), column + suffix] /= pop
        data.loc[(data['Country'] == country), column + suffixDelta] /= pop
        
    print()
        
    return data
    
  def loadPopulationData(self, pathDatasets=PATH_DATASETS, csvFile=CSV_POPULATION, year=2018):
    
    population = pd.read_csv(pathDatasets + csvFile)

    # Rename columns for more convenient and consistent forms 
    population = population.rename(columns={'Country Name':'Country', 'Country Code':'Code'})
    
    # Adjust country names to match the covid dataset
    population.loc[(population['Country'] == 'Iran, Islamic Rep.'), ['Country']] = 'Iran'
    population.loc[(population['Country'] == 'United States'), ['Country']] = 'US'
    population.loc[(population['Country'] == 'Russian Federation'), ['Country']] = 'Russia'
    population.loc[(population['Country'] == 'Bahamas, The'), ['Country']] = 'Bahamas'
    population.loc[(population['Country'] == 'Brunei Darussalam'), ['Country']] = 'Brunei'
    population.loc[(population['Country'] == 'Myanmar'), ['Country']] = 'Burma'
    population.loc[(population['Country'] == 'Egypt, Arab Rep.'), ['Country']] = 'Egypt'
    population.loc[(population['Country'] == 'Gambia, The'), ['Country']] = 'Gambia'
    population.loc[(population['Country'] == 'Korea, Rep.'), ['Country']] = 'South Korea'
    population.loc[(population['Country'] == 'Korea, Dem. Peopleâ€™s Rep.'), ['Country']] = 'North Korea'
    population.loc[(population['Country'] == 'Kyrgyz Republic'), ['Country']] = 'Kyrgyzstan'
    population.loc[(population['Country'] == 'Lao PDR'), ['Country']] = 'Laos'
    population.loc[(population['Country'] == 'St. Kitts and Nevis'), ['Country']] = 'Saint Kitts and Nevis'
    population.loc[(population['Country'] == 'St. Lucia'), ['Country']] = 'Saint Lucia'
    population.loc[(population['Country'] == 'St. Vincent and the Grenadines'), ['Country']] = 'Saint Vincent and the Grenadines'
    population.loc[(population['Country'] == 'Slovak Republic'), ['Country']] = 'Slovakia'
    population.loc[(population['Country'] == 'Syrian Arab Republic'), ['Country']] = 'Syria'
    population.loc[(population['Country'] == 'Venezuela, RB'), ['Country']] = 'Venezuela'
    population.loc[(population['Country'] == 'Yemen, Rep.'), ['Country']] = 'Yemen'
    population.loc[(population['Country'] == 'Venezuela, RB'), ['Country']] = 'Venezuela'

    
    # Extract for specific year
    yearQuery = population['Year']==year
    population = population[yearQuery]
    
    return population

  def loadCovidData(self, pathDatasets=PATH_DATASETS, csvFile=CSV_COVID19):

    covid = pd.read_csv(pathDatasets + csvFile)
    
    # Use more convenient (shorter) column names
    covid = covid.rename(columns={'Country/Region':'Country', 'Province/State':'Province'})

    # Adjust country names to match the population dataset    
    covid.loc[(covid['Country'] == 'Congo (Brazzaville)'), ['Country']] = 'Congo, Rep.'
    covid.loc[(covid['Country'] == 'Congo (Kinshasa)'), ['Country']] = 'Congo, Dem. Rep.'
    covid.loc[(covid['Country'] == 'Czechia'), ['Country']] = 'Czech Republic'
    covid.loc[(covid['Country'] == 'Korea, South'), ['Country']] = 'South Korea'
    
    return covid

    