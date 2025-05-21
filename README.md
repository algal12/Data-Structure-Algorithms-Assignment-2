# Data Structure & Algorithms – Assignment 2
A simple program that uses graph data structures to model the Singapore MRT system and find optimal routes between stations.

## Overview

This Python program simulates the routing system of Singapore's MRT network. It loads real-world MRT station data and builds a graph to represent the metro system. The graph supports:

- Finding the **shortest route (fewest stops)**
- Finding the **fastest route (least travel time)**

The graph is built using the NetworkX library, with real station names and coordinates loaded from a CSV file.

---

## Features

- **Graph Representation**: Each MRT station is a node; connections and transfers are edges.
- **Transfer Penalties**: Switching lines incurs a fixed transfer time (5 minutes).
- **Variable Travel Times**: Travel time between adjacent stations is randomly set between 2–8 minutes.
- **Shortest Path Finder**: Find the path with the fewest stops.
- **Fastest Route Calculator**: Find the path with the least total travel time.

---

## Installation

1. Clone the repository or download the files:

```bash
git clone https://github.com/algal12/Data-Structure-Algorithms-Assignment-2


To run the simulation, simply execute the Python script:


python Galatis Data Structure and Algorithms Assignment 2.py
