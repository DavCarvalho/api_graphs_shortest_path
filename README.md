# Shortest Way 🗺️

A web platform designed to find the shortest paths to reach people and tourist attractions in Salvador, Bahia, Brazil, using graph theory techniques it as made by the graph subject in college




## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [UML Diagrams](#uml-diagrams)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Introduction

The **Shortest Way** platform is designed to help users find optimal routes to connect with friends and discover tourist attractions in Salvador, Bahia. The system leverages graph algorithms to calculate the shortest path between two geographic points, providing both visual map representations and detailed route information.

## ✨ Features

### User Interface (Front-End)
- Input latitude and longitude coordinates
- Select destinations from a list of friends or tourist attractions
- Interactive map displaying the shortest route
- Display route details including distance and estimated travel time
- Responsive design compatible with multiple devices and browsers

### Route Processing (Back-End)
- Calculate shortest routes using Dijkstra's algorithm
- Use real road network data from Salvador, Bahia
- Incorporate road speeds for accurate travel time calculations
- Return routes in appropriate format for map visualization
- Efficient error handling with clear user messages

## 🏗️ Architecture

The system follows a client-server web application architecture:

- **Frontend**: Built with HTMX for seamless HTML/API integration
- **Backend**: FastAPI framework for RESTful API development
- **Communication**: RESTful APIs handle all client-server interactions
- **Data Processing**: OSMnx for road network manipulation and route calculations
- **Visualization**: Folium for interactive map generation

### System Architecture Diagram


## 🛠️ Technologies

### Frontend
- **HTMX**: Simplifies HTML/API integration and interactive page creation
- **Folium**: Generates interactive maps for route visualization
- **JavaScript (Fetch API)**: Handles asynchronous API calls

### Backend
- **FastAPI**: Modern, fast Python framework for building APIs
- **OSMnx**: Obtains and manipulates OpenStreetMap road network data
- **NetworkX**: Implements graph algorithms (Dijkstra, A*) for shortest path calculation
- **Geopandas**: Manipulates geospatial data for route analysis
- **Shapely**: Handles geometric objects (points, lines, polygons)

### Visualization
- **Matplotlib**: Creates static route visualizations
- **Contextily**: Adds detailed background maps to visualizations
- **Folium**: Generates interactive HTML maps

## 📦 Requirements

### Python Dependencies

```text
fastapi
uvicorn
osmnx
networkx
geopandas
shapely
folium
matplotlib
contextily
pydantic
python-multipart
jinja2
```

### System Requirements
- Python 3.8+
- Virtual environment (recommended)
- Modern web browser

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/DavCarvalho/api_graphs_shortest_path.git
cd api_graphs_shortest_path
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create the database**
```bash
python create_database.py
```

5. **Run the application**
```bash
uvicorn app:app --reload
```

6. **Access the application**
Open your browser and navigate to: `http://localhost:8000`

## 💻 Usage

### Basic Workflow



1. **Enter Your Location**
   - Input your latitude and longitude coordinates

2. **Select Destination**
   - Choose a friend or tourist attraction from the dropdown menu

3. **Calculate Route**
   - Click "Find Route" button to calculate the shortest path

4. **View Results**
   - Interactive map showing the route
   - Static image with detailed visualization
   - Distance and estimated travel time

### Example Usage

## 📡 API Documentation

### Endpoints

#### GET `/friends`
Returns the list of available friends.

**Response:**
```json
{
  "John Doe": {
    "latitude": -12.9777,
    "longitude": -38.5016
  }
}
```

#### GET `/places_salvador`
Returns the list of tourist attractions in Salvador.

**Response:**
```json
{
  "Mercado Modelo": {
    "latitude": -12.9714,
    "longitude": -38.5124
  }
}
```

#### POST `/shortest_path`
Calculates the shortest path between origin and destination.

**Request Body:**
```javascript
{
  "latitude": -13.0086948,
  "longitude": -38.5375255,
  "destination": "Mercado Modelo"
}
```

**Response:**
```json
{
  "html_path": "/static/route.html",
  "png_path": "/static/route.png"
}
```

### Frontend-API Integration Example

```javascript
// Fetch friends list
fetch(`${apiUrl}/friends`)
  .then(response => response.json())
  .then(data => {
    const select = document.getElementById("destination");
    for (const friend in data) {
      const option = document.createElement("option");
      option.value = friend;
      option.text = friend;
      select.add(option);
    }
  })
  .catch(error => {
    console.error("Error fetching friends:", error);
  });
```

## 📊 Algorithm Details

### Route Calculation Process

1. **Area Optimization**: Instead of loading the entire city's road network, the system calculates a bounding box that includes only the origin and destination points, optimizing resource usage.

2. **Graph Construction**: Uses OSMnx to download the road network as a directed graph where:
   - Nodes represent intersections or geographic points
   - Edges represent streets or paths

3. **Speed Integration**: Adds speed data to edges using `ox.routing.add_edge_speeds()`

4. **Travel Time Calculation**: Computes travel time for each edge:
   ```
   travel_time = edge_length / edge_speed
   ```

5. **Shortest Path**: Applies Dijkstra's algorithm using travel time as the weight metric

6. **Visualization**: Generates both interactive (Folium) and static (Matplotlib) visualizations

### Code Example: Route Calculation

```python
# Calculate center point and maximum distance
center_lat = (origin_lat + dest_lat) / 2
center_lon = (origin_lon + dest_lon) / 2
max_dist = max(abs(origin_lat - dest_lat), 
               abs(origin_lon - dest_lon)) * 111320  # Convert to meters

# Download road network
G = ox.graph_from_point((center_lat, center_lon), 
                        dist=max_dist, 
                        network_type='drive')

# Add speeds and travel times
G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

# Find nearest nodes
orig_node = ox.distance.nearest_nodes(G, origin_lon, origin_lat)
dest_node = ox.distance.nearest_nodes(G, dest_lon, dest_lat)

# Calculate shortest path
shortest_path = nx.shortest_path(G, orig_node, dest_node, 
                                 weight='travel_time')
```

## 📈 UML Diagrams

### Sequence Diagram
The sequence diagram illustrates the interaction flow between User, Interface, API, and Map components:

<img width="1136" height="449" alt="image" src="https://github.com/user-attachments/assets/7c98aad7-cbc9-40dd-af29-1a35865cd952" />


1. User enters coordinates
2. Interface calls the API route
3. API calculates the route
4. Map stores the information
5. API returns the map with route
6. Interface displays the map with route

### Use Case Diagram
The use case diagram shows the main user interactions with the system:

<img width="951" height="587" alt="image" src="https://github.com/user-attachments/assets/cb8d0d85-4719-412f-b8fa-bc7f3cecb582" />


## 🖼️ Screenshots

### Application Interface
<img width="951" height="587" alt="image" src="https://github.com/user-attachments/assets/616983c1-1e0d-4d5e-9469-420e26c6ffd1" />

The interface shows:
- Input fields for latitude and longitude
- Destination selection dropdown
- "Find Route" button
- Results section with both static and interactive maps
- Route visualization with markers for origin (green) and destination (blue)

## 📅 Project Timeline

| Project Phase | Date | Context |
|--------------|------|---------|
| Project Start, Idea Construction and Initial Requirements | Early May 09/05 | In Class |
| System Functionality Planning | Mid-May 16/05 | In-class Meeting |
| Technology Definition | 16/05 to 30/05 | Teams and Notion Meetings |
| Backend Construction | 05/06 to 14/06 | VS Code |
| Frontend Construction | 15/06 to 20/06 | VS Code |



## 👥 Authors

- **David Carvalho** - [@DavCarvalho](https://github.com/DavCarvalho)

## 🙏 Acknowledgments

- OpenStreetMap for providing road network data
- OSMnx library for simplifying geospatial network analysis
- FastAPI community for excellent documentation
- Salvador, Bahia tourism board for inspiration

---

**Project Link**: [https://github.com/DavCarvalho/api_graphs_shortest_path](https://github.com/DavCarvalho/api_graphs_shortest_path)
