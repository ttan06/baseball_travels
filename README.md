[![Coverage Status](https://coveralls.io/repos/github/ttan06/baseball_travels/badge.svg?branch=main)](https://coveralls.io/github/ttan06/baseball_travels?branch=main)

# Baseball Stadium Travels

## Project Description
Known as America’s pastime, going to baseball games is a common summertime activity. One popular way is to go on a stadium tour and travel across the country, watching a game at each stadium.

Our application creates an optimal schedule for fans of all types to attending games at MLB stadiums in 2024, given user inputted parameters.

Users are able to optimize for cost, time, or distance, choosing either the cheapest route, quickest route, or the route with the least travel, and can view the journey on a map. 


## How to run app

The following packages need to be installed before running the app :

* plotly : pip3 install plotly
* pandas : pip3 install pandas
* dash : pip3 install dash


To start the app just run the command below in your terminal at baseball_travels : 

```
python3 app.py
```

After running the app, open the link provided from the terminal in your browser. Then select the teams from the drop down list you would like to visit then view the paths to take. 

## Future Work
* Optimize search algorithm to remove team entry limit and reduce runtime and loading time.

* Introduce method to choose specific games, especially for more advanced fans. These can be based on the away teams, home team promotions, or even specific player appearances.

* Incorporate live flight costs and stadium ticket prices and add to the total cost. 

## Data

Schedule Data: 
* https://www.baseball-reference.com/leagues/majors/2024-schedule.shtml 

US Stadium locations
* https://docs.google.com/spreadsheets/d/1p0R5qqR7XjoRG2mR5E1D_trlygHSqMOUdMgMpzq0gjU/htmlview

Map/Distance Data:
* https://www.openstreetmap.org/#map=4/38.01/-95.84 

Flight Data: 
* https://data.transportation.gov/Aviation/Consumer-Airfare-Report-Table-6-Contiguous-State-C/yj5y-b2ir/data



