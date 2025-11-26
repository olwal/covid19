set SCRIPTS_FOLDER=%cd%
set DATA_FOLDER=..\data

cd %DATA_FOLDER%

cd datasets

REM get population data
REM ----------------------------------
cd population
git fetch
git checkout origin/master --  data/population.csv
cd ..

REM get CSSE John Hopkins data from datasets
REM ----------------------------------
cd covid-19
REM git checkout HEAD data/time-series-19-covid-combined.csv
git fetch
git checkout origin/master -- data/time-series-19-covid-combined.csv
cd ..

cd %SCRIPTS_FOLDER%

REM (not used anymore)

REM cd CSSEGISandData

REM get CSSE John Hopkins data
REM ----------------------------------
REM cd COVID-19
REM git checkout HEAD csse_covid_19_data/csse_covid_19_daily_reports/*.csv
REM cd ..

REM cd ..