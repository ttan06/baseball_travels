# Data

## MLB Schedule

For more details and to refresh the schedule for a future season, visit the notebook 'Schedule Scraping.ipynb' in the notebooks section of this repository.

The MLB schedule dataset used by the app is 'final_mlb_schedule.csv' which contains nearly 3000 rows, each with the details of a game, including the teams, date, time, and coordinates of the stadium.

## Cost Matrix

The cost matrix is a csv 'cost_df.csv', which is created by running the following:

```commandline
python -m data.create_cost_matrix
```

### Description
It is 900 rows, with a from and to location, the cost of the trip, and the locations. 
The intended usage is to pull the route of from and to locations, and the "fare" column, which is based on cost and time. 

### Acquisition
The script uses the file 'team_airport_key.csv', which is a mapping of the team stadium to the closest major airport.

It also uses the file 'Consumer_Airfare_Report__Table_6_-_Contiguous_State_City-Pair_Markets_That_Average_At_Least_10_Passengers_Per_Day_20240309.csv'

This file is obtained from the [Consumer Airfare Report](https://data.transportation.gov/Aviation/Consumer-Airfare-Report-Table-6-Contiguous-State-C/yj5y-b2ir/data). Since this downloaded csv is quite large, it is not included in the repository and must be downloaded prior to running the 'create_cost_matrix.py' file.

### Other Details
Since not every path between two teams has a flight, we fill in the missing cost data with a driving estimate. We use the average cost of a gallon of gas in 2023, which is $3.29 as of March 2024 [(Source)](https://www.finder.com/economics/gas-prices#:~:text=National%20average%3A%20The%20current%20national%20average%20cost,for%20gas%20is%20%243.23%20%28Feb.%2022%2C%202024%29%20%281%29).
We also use the average miles per gallon, which was 36mpg [(Source)](https://www.caranddriver.com/research/a31518112/what-is-good-gas-milage/).
