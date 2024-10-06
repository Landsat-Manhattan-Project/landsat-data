# LANDSAT
## Table of Contents

- [LANDSAT](#landsat)
  - [Table of Contents](#table-of-contents)
  - [Endpoints](#endpoints)
    - [GET `/metadata`](#get-metadata)
    - [POST `/evaluate-data`](#post-evaluate-data)
  - [Example Requests](#example-requests)
    - [1. Location: **Amazonia** (Latitude: 6.0, Longitude: -74.0)](#1-location-amazonia-latitude-60-longitude--740)
    - [2. Location: **Desierto del Sahara** (Approximate Coordinates: Latitude: 24.0, Longitude: 25.0)](#2-location-desierto-del-sahara-approximate-coordinates-latitude-240-longitude-250)
    - [3. Location: **Australia** (Approximate Coordinates: Latitude: 70.0, Longitude: -55.0)](#3-location-australia-approximate-coordinates-latitude-700-longitude--550)
    - [4. Location: **Amazonia** (Latitude: 1.0, Longitude: -70.0)](#4-location-amazonia-latitude-10-longitude--700)
    - [5. Location: **Islandia** (Latitude: 65.0, Longitude: -18.0)](#5-location-islandia-latitude-650-longitude--180)
  - [Setup and Installation](#setup-and-installation)
  - [Troubleshooting](#troubleshooting)

## Endpoints

### GET `/metadata`

Retrieve metadata for a Landsat satellite image based on latitude and longitude.

**Parameters:**

- `latitude` (float): Latitude of the target location.
- `longitude` (float): Longitude of the target location.

**Example:**

```bash
curl -X GET "http://localhost:8000/metadata?latitude=6.0&longitude=-74.0"
```

### POST `/evaluate-data`

Evaluate data based on provided context and role.

**Headers:**

- `Content-Type: application/json`

**Body Parameters:**

- `latitude` (float): Latitude of the target location.
- `longitude` (float): Longitude of the target location.
- `context` (string): Contextual information for the evaluation.
- `role` (string): Role of the user (e.g., farmer, researcher).

**Example:**

```bash
curl -X POST "http://localhost:8000/evaluate-data"   -H "Content-Type: application/json"   -d '{
        "latitude": 6.0,
        "longitude": -74.0,
        "context": "I am studying the impact of cloud coverage on agricultural yield.",
        "role": "farmer"
      }'
```

## Example Requests

Below are example requests demonstrating how to use the API for different geographic locations.

### 1. Location: **Amazonia** (Latitude: 6.0, Longitude: -74.0)

**GET Metadata:**

```bash
curl -X GET "http://localhost:8000/metadata?latitude=6.0&longitude=-74.0"
```

**POST Evaluate Data:**

```bash
curl -X POST "http://localhost:8000/evaluate-data"   -H "Content-Type: application/json"   -d '{
        "latitude": 6.0,
        "longitude": -74.0,
        "context": "I am studying the impact of cloud coverage on agricultural yield.",
        "role": "farmer"
      }'
```

---

### 2. Location: **Desierto del Sahara** (Approximate Coordinates: Latitude: 24.0, Longitude: 25.0)

**GET Metadata:**

```bash
curl -X GET "http://localhost:8000/metadata?latitude=24.0&longitude=25.0"
```

**POST Evaluate Data:**

```bash
curl -X POST "http://localhost:8000/evaluate-data"   -H "Content-Type: application/json"   -d '{
        "latitude": 24.0,
        "longitude": 25.0,
        "context": "I am assessing the impact of water vapor on local climate conditions.",
        "role": "researcher"
      }'
```

---

### 3. Location: **Australia** (Approximate Coordinates: Latitude: 70.0, Longitude: -55.0)

**GET Metadata:**

```bash
curl -X GET "http://localhost:8000/metadata?latitude=70.0&longitude=-55.0"
```

**POST Evaluate Data:**

```bash
curl -X POST "http://localhost:8000/evaluate-data"   -H "Content-Type: application/json"   -d '{
        "latitude": 70.0,
        "longitude": -55.0,
        "context": "I am analyzing how high cloud coverage affects agricultural production.",
        "role": "farmer"
      }'
```

---

### 4. Location: **Amazonia** (Latitude: 1.0, Longitude: -70.0)

**GET Metadata:**

```bash
curl -X GET "http://localhost:8000/metadata?latitude=1.0&longitude=-70.0"
```

**POST Evaluate Data:**

```bash
curl -X POST "http://localhost:8000/evaluate-data"   -H "Content-Type: application/json"   -d '{
        "latitude": 1.0,
        "longitude": -70.0,
        "context": "I am analyzing how high cloud coverage affects agricultural production.",
        "role": "farmer"
      }'
```

---

### 5. Location: **Islandia** (Latitude: 65.0, Longitude: -18.0)

**GET Metadata:**

```bash
curl -X GET "http://localhost:8000/metadata?latitude=65.0&longitude=-18.0"
```

**POST Evaluate Data:**

```bash
curl -X POST "http://localhost:8000/evaluate-data"   -H "Content-Type: application/json"   -d '{
        "latitude": 65.0,
        "longitude": -18.0,
        "context": "I am analyzing how high cloud coverage affects agricultural production.",
        "role": "farmer"
      }'
```

---

## Setup and Installation

To get started with the Universidad de la Sabana API, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/universidad-de-la-sabana-api.git
   cd universidad-de-la-sabana-api
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI Server:**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the Interactive API Documentation:**

   Open your browser and navigate to `http://localhost:8000/docs` to explore and test the API endpoints interactively.

## Troubleshooting

If you encounter any issues while using the API, consider the following troubleshooting steps:

1. **Check Server Logs:**

   Ensure that the FastAPI server is running without errors. Server logs can provide insights into any issues.

   ```bash
   # If running the server in a terminal, observe the logs directly.
   ```

2. **Validate JSON Files:**

   Ensure that all JSON files in the `app/data/` directory are correctly formatted. You can use `jq` to validate JSON syntax.

   ```bash
   jq . app/data/LC09_L2SP_218015_20241002_20241003_02_T1.json
   ```

3. **Verify File Permissions:**

   Ensure that the FastAPI application has read permissions for all JSON files.

   ```bash
   chmod 644 app/data/*.json
   ```

4. **Coordinate Validation:**

   Make sure the latitude and longitude provided in the requests fall within the regions covered by your metadata JSON files.

5. **API Documentation:**

   Utilize FastAPI's interactive documentation at `http://localhost:8000/docs` to test endpoints and understand expected inputs and outputs.

6. **Restart the Server:**

   After making changes to JSON files or configurations, restart the FastAPI server to apply the updates.

   ```bash
   uvicorn app.main:app --reload
   ```

If problems persist, please reach out to the project maintainer or consult the documentation for further assistance.

---