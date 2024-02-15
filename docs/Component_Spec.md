## Component Specification
### Software Components

#### Input Handler/UI
* User interface that handles user inputs
* Takes in parameters from UI that are inputted by user
* Applies inputted parameters to schedule/route to check legality (e.g. home games for teams exist during given time period)
* Output parameters to route generator to check legality and passes along user inputs

#### Route Creator
* Program that generates routes based on user-provided and intrinsic parameters
* Takes in inputs from input handler and from data sets and sources
* Uses python-tsp package to create routes ordered by optimal cost or distance, depending on user input.
* Checks legality of package-created routes
* Outputs several legal schedules and routes to route visualizer and UI

#### Route Visualizer
* Program that visualizes routes on a map within the UI
* Takes in different legal routes in the form of directed graph from the route creator
* Displays route on map using coordinates and edges
* Has toggle that can change route, and both map and table are updated
* Outputs visualized map and table displaying each step of the schedule or route to UI

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
