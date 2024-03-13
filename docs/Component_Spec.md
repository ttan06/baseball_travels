## Component Specification
### Software Components

#### Input Handler/UI
* User interface that handles user inputs. This is built with Dash. 
* Takes in parameters from UI that are inputted by user.
  * Dates - Strings converted to datetime objects - desired date range.
  * Teams - Strings - desired teams to visit (up to 6)
  * Optimization - String - how to optimize the schedule
* Applies inputted parameters to schedule/route to check legality (e.g. home games for teams exist during given time period)
* Output parameters to route generator to check legality and passes along user inputs
  * Sends the above parameters to the next stage.

#### Route Creator
* Program that generates routes based on user-provided and intrinsic parameters
* Takes in inputs from input handler and from data sets and sources
  * Dates - Strings converted to datetime objects - desired date range.
  * Teams - Strings - desired teams to visit (up to 6)
  * Optimization - String - how to optimize the schedule
  * Schedule - Pandas DataFrame - the MLB schedule where game details are acquired from.
  * Cost Matrix - Pandas DataFrame - cost it takes to travel from one place to another.
* Uses custom package to create routes ordered by optimal cost, time or distance, depending on user input.
* Checks legality of package-created routes
* Outputs several legal schedules and routes to route visualizer and UI
  * Route - list - list of teams, ordered by visit
  * Schedule - Pandas DataFrame - MLB schedule, but one game per each team in the route, optimized by user choice.
  * Metrics - strings/float - The metrics (total cost, distance, time) from the optimized schedule.

#### Route Visualizer
* Program that visualizes routes on a map within the UI
* Takes in different legal routes in the form of directed graph from the route creator
  * Route - list - list of teams, ordered by visit
  * Schedule - Pandas DataFrame - MLB schedule, but one game per each team in the route, optimized by user choice.
  * Metrics - strings/float - The metrics (total cost, distance, time) from the optimized schedule.
* Displays route on map using coordinates and edges
* Has toggle that can change route, and both map and table are updated
* Outputs visualized map and table displaying each step of the schedule or route to UI
  * Map - Dash Graph Object - map of the US displaying the traveling route
  * Schedule Table - Dash data table - tables of the inputted schedule
  * Metrics Table - Dash data table - tables of the metrics from the optimized schedule. 

### Interactions
#### Use Case: Generate Schedules
* This use case mainly uses the route creator and input handler/UI components.
* The user inputs desired stadiums and dates to the Input Handler/UI, which checks legality of stadium and date combination
* The Input Handler/UI then sends the parameters to the Route Creator that creates the routes and schedule
* The Route Creator then creates the routes and schedules and outputs them in the form of a table to back to the UI which displays the table to the user.

![](images/Generate%20Schedule.png)

#### Use Case: View Routes and Costs on Map
* This use case mainly uses the route creator and route visualizer, but also the UI.
* The Route Creator sends the route information to the Route Visualizer
* The Route Visualizer visualizes each route on a map and sends it to the UI. 
* The user hovers over a point on the map on the UI, the UI tracks the movement and retrieves the information from that point from the Route Visualizer and displays the data to the user. 

![](images/View%20Routes%20and%20Costs%20on%20Map.png)

#### Route Creation Pipeline
* This is a more detailed view of how the routes are created in the route creator. 

![](images/schedule_builder_pipeline.png)
