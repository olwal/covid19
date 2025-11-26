#!/bin/bash

rm -f ../data/datasets/covid-19/data/*
wget --directory-prefix=../data/datasets/covid-19/data https://raw.githubusercontent.com/datasets/covid-19/main/data/time-series-19-covid-combined.csv

rm -f ../data/datasets/population/data/*
wget --directory-prefix=../data/datasets/population/data https://raw.githubusercontent.com/datasets/population/master/data/population.csv
