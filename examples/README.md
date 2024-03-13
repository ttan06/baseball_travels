# Example

## Quickstart

From a local copy of the repository, run:

```commandline
pip install -r requirements.txt
```

## Obtaining the Data

The data used in this project is from the MLB and Consumer Airfare Report. For details on how to refresh the data, please vist the [Data](../data/README.md) section of this repository.

## Running the Application

From the root repository, run:

```commandline
python app.py
```
For an example on how to use the app, please view the demo in the [docs](../docs) folder. 

## Running Functions from make_route

The following section will be a tutorial of how to build a travel schedule from the make_route package.

### Imports

```python
import pandas as pd
from makeRoute.exhaustiveSearch import reduce_routes, reduce_schedule, sort_order, find_all_routes
```
### Files

Below are the files that are needed to run the functions. 

```python
mlb_schedule = pd.read_csv('data/final_mlb_schedule.csv') # data frame
# convert the dates to datetime from string
mlb_schedule['date'] = pd.to_datetime(mlb_schedule['date'])
cost_dfx = pd.read_csv('data/cost_df.csv') # data frame
```

### Finding all the Routes and Subsetting the Schedule

Here we input the specific teams that we want to see and the date range. Due to the methodology of future functions, we cap the max number of teams to 6, to conserve runtime. 

```python
teamlist = ['Seattle Mariners', 'Kansas City Royals', 'Boston Red Sox'] # max is 6
start_dt = '2024-05-06'
end_dt = '2024-08-02'
# reduce the schedule to only include specific teams and dates
short_sched = reduce_schedule(mlb_schedule, teamlist, start_dt, end_dt)
# find all possible route combinations
rts = find_all_routes(teamlist)
```

### Creating the Reduced Schedule

The reduce_routes function will do most of the heavy lifting for this project. It calls upon check_valid_route which takes in a route and checks if it is valid, that is there exist games for each stadium within the time frame in the specific route order. 

If valid, the schedule will be created with the earliest game from the next team on the route. During that process, the function will call calculate_distance and calculate_cost, to obtain the total distance and cost of the route.

This is done for all the routes, so the runtime is O(n!). 

```python
game_log = reduce_routes(rts, short_sched, cost_dfx)
```
The output is a pandas dataframe that is the route, the game schedule, and the total cost, distance, and time.

### Sorting by Desired Method

We can then sort the routes by our desired method. In the below example, we sort by distance using the sort_order function. This will result possible routes being sorted by distance, and we can then take the first entry, which has the lowest distance travelled. 

```python
# can sort on time, distance, or cost
sorted_route = sort_order(game_log, 'distance')
# we take the first entry, which has the smallest total distance
sched = sorted_route['games'][0]
# condense data frame to be desired output
sched = sched[['date', 'time', 'away team', 'home team']]
# change date to be more readable
sched['date'] = sched['date'].dt.strftime('%m-%d-%Y')
```

The final output is "sched", a pandas dataframe that contains each game in order for the user to travel to. This is used in the app.py function to create the data table and for input into the map.

## Testing

### Unit Tests
To run the unit tests for search, distance and app, run the following:

```commandline
python -m tests.test_search
python -m tests.test_distance
python -m tests.test_app
```

### Coverage

To run the coverage tests, run:

```commandline
pip install coverage
python -m coverage run -m unittest discover
python -m coverage report      
```


