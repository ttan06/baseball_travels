## Functional Specification

### Background
The goal for this project is to create schedules for visiting MLB stadiums given the 2024 MLB schedule, given user inputted parameters. The shortest or cheapest route may not always be possible, since there may be schedule constraints (e.g. there might not be a home game for a team within a certain time frame between home games for other teams). This project serves to create legal schedules for a user to travel to all desired stadiums within a time frame. 

### User Profiles
Baseball fans with domain knowledge of baseball, players, teams, stadiums can use the system to create some schedules to choose from. They interact with the system through the web application interface by inputting the teams or stadiums they want to visit, as well as a time frame. They can either prioritize cost or travel distance and time, and with their domain knowledge, can select which schedules they prefer based on other details as well, including away teams or pitching matchups.

The technician maintaining the application will mainly work on keeping the dataset updated with the most recent schedule changes, including weather delays, as well as updating the flight prices. They will interact with the system through the repository and work with the code. They should also have skills in Python programming and UI development. 

### Data Sources:

[2024 MLB Schedule](https://www.baseball-reference.com/leagues/majors/2024-schedule.shtml)

This data source is from Baseball Reference. It is in the form of text on a webpage, and will need to be scraped into a table. It provides the teams playing, the date of the game, and the time of the game.  

[World Cities Database](https://simplemaps.com/data/world-cities)

This data source is from simple maps, and is a table that can be exported into a csv that contains over 30,000 rows. It provides each city and several details, and will mainly be used to grab the coordinates of each city, for distance calculation usage. 

[Consumer Airfare Report](https://data.transportation.gov/Aviation/Consumer-Airfare-Report-Table-1-Top-1-000-Contiguo/4f3n-jbg2/data)

This data source is from the US Department of Transportation. It is in the form of a table that can be exported into a csv and contains over 100,000 rows. It will mainly be used to provide the prices of flights between two cities.

### Use Cases

#### Use Case: Generate Schedules
The objective of the user interaction is to use the system to generate and view legal schedules for a baseball-focused trip. 

The expected interactions are that the user inputs parameters for desired stadium visitations and dates, the system uses those parameters to generate potential legal schedules, and outputs them in the form of a table for users to look through, with details such as travel time, distance, or cost. 

#### Use Case: View Routes and Costs on Map
The objective of the user interaction is to view the outputted schedules and routes on a map alongside costs and distances

The expected interactions are that after the user generates schedules, they can view and interact with the map portion of the UI and hover over cities and routes with their map. The system will display the map and other information depending on what the user chooses to view on the UI. 

#### Use Case: Understanding Distance and Cost of Traveling in the US
The objective of this user interaction is to be able to see how much it costs to travel in the US and how far it may be. 

The expected interactions are for the user to view the table on the bottom left of the dashboard that summarizes the trip.
