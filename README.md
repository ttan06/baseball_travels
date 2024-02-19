# Baseball Stadium Travels

## Project Type

The plan for this project is to be a Web Application that takes in user inputs of Teams and Dates and provides potential routes and schedules for users to choose from.

## Questions

* How many teams can the app handle on a schedule without providing too many options?
* Can we optimize for distance and maybe cost?
* Can we take lineup and potential starters into account to maximize enjoyment for fans?


## Goals

Create an interface that allows users to select parameters such as weeks available and stadiums to visit, in order to create an optimal route that satisfies all constraints. 

Stretch Goals:
* Create visualization of route on map
* Look at ticket price to see differences in price per away team
* Build in home-team promotions
* Use projected lineups to maximize "fun" (maybe day with max team WAR or Ace pitchers)


## Data

Schedule Data: 
* https://www.baseball-reference.com/leagues/majors/2024-schedule.shtml 
* https://www.mlbschedulegrid.com/downloads

Map/Distance Data:
* https://www.openstreetmap.org/#map=4/38.01/-95.84 

Ticket Data: 
* https://www.mlb.com/tickets

Flight Data: 
* https://www.flightconnections.com/airlines

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



