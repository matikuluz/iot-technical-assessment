
# IoT Full Stack Technical Assessment

## Overview

Welcome to the technical assessment for the Full Stack Engineer position at **Loop Services**.

Your objective is to build the "glue" that connects a raw IoT sensor to a real-time dashboard. We have provided the core infrastructure (Backend API & Database) and a Mock Device. Your task is to implement the **Middleware** layer and the **Frontend** data logic.

### Architecture

1.  **Mock Device** (Provided): Simulates an IoT device publishing raw data to an MQTT broker.
2.  **Middleware** (Your Task): A Python script that listens to MQTT, sanitizes data, and POSTs it to the Backend.
3.  **Backend** (Provided): A FastAPI server that stores data in SQLite and streams updates via WebSockets.
4.  **Frontend** (Your Task): A Vue.js dashboard to visualize historical and real-time data.

---

## Prerequisites

* **Python 3.8+**
* **Node.js 16+** (and `npm`)
* **Git**

---

## Project Setup

To make setup easy, we use a single Python environment for the Backend, Middleware, and Device components.

### 1. Global Python Setup
Run these commands from the **root** of the project folder:

```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the environment
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# 3. Install all dependencies (Backend, Middleware, & Device)
pip install -r requirements.txt

```

### 2. Start the Backend (Provided)

The backend handles database storage and WebSocket broadcasting.

Bash

```
cd backend
uvicorn main:app --reload

```

-   **Verify:**  Open  [http://127.0.0.1:8000](http://127.0.0.1:8000/)  in your browser. You should see  `{"status": "running"}`.
    
-   _Leave this terminal running._
    

### 3. Start the Frontend (Skeleton Provided)

The frontend is a Vue 3 application. We have provided the UI components, but the data hooks are missing.

Open a  **new terminal**  (keep the backend running) and run:

Bash

```
cd frontend
npm install
npm run dev

```

-   **Verify:**  Open the local link provided (usually http://localhost:5173). You should see the dashboard UI, but it will say "Offline" and show no data.
    
-   _Leave this terminal running._
    

### 4. Configure & Start the Mock Device

To prevent data collisions on the public MQTT broker, you must set a unique topic.

1.  Open  `device/mock_sensor.py`.
    
2.  Find the  `TOPIC`  variable.
    
3.  Change it to:  `loopservices/{your_first_name}/sensors/raw`  (e.g.,  `loopservices/alex/sensors/raw`).
    
4.  **Run the device**  in a  **new terminal**  (ensure your  `.venv`  is active):
    

Bash

```
cd device
python mock_sensor.py

```

-   You should see logs indicating data is being published.
    

----------

## Your Tasks

Now that the infrastructure is running, your goal is to connect the pieces.

### Task 1: The Middleware

**Location:**  `bridge/middleware.py`  (Skeleton provided)

You need to write the script that bridges the gap between MQTT and our HTTP API.

**Requirements:**

1.  **Subscribe**  to the unique topic you configured in Step 4.
    
2.  **Sanitize**  the incoming data. The device sometimes sends "dirty" data (e.g., negative humidity, temperatures > 100°C, or string errors). You must filter these out.
    
3.  **Normalize**  the data keys. The device sends  `t`  and  `h`, but the API expects  `temperature`  and  `humidity`.
    
4.  **POST**  valid data to the Backend API (`http://127.0.0.1:8000/api/readings`).
    

_Tip: You can verify this is working if you see "200 OK" logs in your Backend terminal._

### Task 2: The Frontend Logic

**Location:**  `frontend/src/App.vue`

You need to bring the dashboard to life by connecting it to the backend.

**Requirements:**

1.  **Historical Data:**  On page load, fetch the last 50 readings from  `GET http://127.0.0.1:8000/api/readings`and populate the chart.
    
2.  **Real-time Data:**  Connect to the WebSocket at  `ws://127.0.0.1:8000/ws`.
    
3.  **Updates:**  When a WebSocket message arrives, parse it and update the Chart and the "Current Status" cards dynamically.
    
4.  **Status Indicator:**  The "System Online/Offline" pill in the header should reflect the actual WebSocket connection state.
    

----------



## Submission

1.  **Fork**  this repository to your own GitHub account.
    
2.  **Commit**  your changes as you work.
    
3.  Once finished, ensure all tests pass and your code is clean.
    
4.  Send us the  **link to your forked repository**.
    
    -   _Note: Please ensure the repository is public so we can review it, or invite us if it is private._
    

----------

## Troubleshooting

-   **Port Conflicts:**  Ensure nothing else is running on port 8000.
    
-   **Connection Refused:**  If  `localhost`  fails in your code, try using  `127.0.0.1`  explicitly.
    
-   **Import Errors:**  Ensure you have activated the virtual environment (`source .venv/bin/activate`) before running Python scripts.