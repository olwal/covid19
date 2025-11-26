#!/bin/bash

SCRIPT_FOLDER=$(pwd)
DATA_FOLDER=../data

cd ${DATA_FOLDER}

cd datasets

# get population data
# ----------------------------------
git clone -n https://github.com/datasets/population.git --depth 1
cd population
git fetch
git checkout HEAD data/population.csv
cd ..

# get CSSE John Hopkins data from datasets
# ----------------------------------
git clone -n https://github.com/datasets/covid-19.git --depth 1
cd covid-19
# git checkout HEAD data/time-series-19-covid-combined.csv
git fetch
git checkout HEAD data/time-series-19-covid-combined.csv
cd ..

cd ${SCRIPTS_FOLDER}