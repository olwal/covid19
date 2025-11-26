set SCRIPTS_FOLDER=%cd%
set DATA_FOLDER=..\data

cd %DATA_FOLDER%

md datasets
cd datasets

REM get population data
REM ----------------------------------
git clone -n https://github.com/datasets/population.git --depth 1
cd population
git checkout HEAD data/population.csv
cd ..

REM get CSSE John Hopkins data from datasets
REM ----------------------------------
git clone -n https://github.com/datasets/covid-19.git --depth 1
cd covid-19
git checkout HEAD data/time-series-19-covid-combined.csv
cd ..

cd %SCRIPTS_FOLDER%

REM (not used anymore)

REM md CSSEGISandData
REM cd CSSEGISandData

REM get CSSE John Hopkins data
REM ----------------------------------
REM git clone -n https://github.com/CSSEGISandData/COVID-19.git --depth 1
REM cd COVID-19
REM git checkout HEAD csse_covid_19_data/csse_covid_19_daily_reports/*.csv
REM cd ..

REM cd ..