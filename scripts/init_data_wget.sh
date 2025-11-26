#!/bin/bash

mkdir ../data/datasets
mkdir ../data/datasets/covid-19
mkdir ../data/datasets/covid-19/data

wget -O --directory-prefix=../data/datasets/covid-19/data https://raw.githubusercontent.com/datasets/covid-19/main/data/time-series-19-covid-combined.csv

mkdir ../data/datasets/population
mkdir ../data/datasets/population/data

wget -O --directory-prefix=../data/datasets/population/data https://raw.githubusercontent.com/datasets/population/master/data/population.csv

