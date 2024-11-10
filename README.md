# DijkstraRoadAlignment

## Introduction
Python code to implement Dijkstra's Algorithm on Raster DEM to find the shortest (least cost) path.

## Workflow
- Raster.py is a class that creates a 2D matrix from a QGIS Raster DEM Layer.
- Grid.py is a class that stores the 2D matrix and has methods to provide information of a matrix cell like its values and neighbours.
- First, Network.py generates the Cost Network.
- Then, Dijkstra.py implements the Dijkstra's algorithm.
- Finally, Path.py converts the resulting shortest path to a QGIS vector line layer.

```mermaid
flowchart LR
    A([Network.py]) --> B([Dijkstra.py])
    B --> C([Path.py])
```
