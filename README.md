# Jaka to melodia - What melody is it
The aim of this project is gather in one place all song used in popular polish show "Jaka to melodia" ("What melody is it"). 

Before running or changing code please read [Confluence documentation](https://adlm.nielsen.com/confluence/display/NPI/Denmark)

## Getting started
```

## Requirements
The required version of Python for the current release is 3.7.

### Prerequisities
Run the code below:

```
pip install -r \path_to\requirements.txt
```
Remember that if you add any library to your project scripts you MUST add them to **requirements.txt**

## Authors
Sebastian Konicz - sebastian.konicz@gmail.com

## Project Organization <a id="project"></a>
------------

    ├── data              				<- Place whre the data is stored
    │   │
    │   ├── interim        					<- Intermediate data that has been transformed.
    │   │
    │   ├── processed      					<- The final, canonical datasets for modeling.
    │   │
    │   └── raw            					<- The original, immutable data dump.
    │
    ├── README.md					<- The top-level README for developers using this project.
    │
    ├── src                				<- Source code for use in this project.
    │   │
    │   ├── __init__.py    					<- Makes src a Python module
    │   │
    │   ├── JTM_cleaning          			        <- Script cleaning the data scrapped from the Internet
    │   │
    │   ├── JTM_scrapy          			        <- Script scrapping the data from the Internet
    │   │
    │   ├── JTM_deezer_API           		                <- Script updating information about artist and song
    │   │	
    │   │
    │   └──  								<-  │   
    │
    └── xxxxx            					<- ?


--------
