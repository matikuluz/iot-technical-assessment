# iot-technical-assessment Submission 

## Submission Overview

This submission connects a mock IoT sensor feed to a FastAPI backend via a Python middleware layer, and provides a Vue dashboard to monitor temperature and humidity in both historical and real time. The middleware is responsible for validation and normalization before forwarding readings to the backend API, and the frontend renders the latest values and a live-updating chart. 

The following deliverables have been met: 

## Task 1: Middleware

- Subscribe to the unique topic configured for the device.
- Sanitize incoming data and filter dirty payloads (invalid JSON, non-numeric values, NaN/inf, out-of-range readings).
- Normalize keys from `t`/`h` to `temperature`/`humidity`.
- POST valid data to the backend API (`http://127.0.0.1:8000/api/readings`).

## Task 2: Frontend Logic

- Historical Data: fetch last 50 readings from `GET http://127.0.0.1:8000/api/readings` and populate the chart (chart retains the most recent 20 points).
- Real-time Data: connect to the WebSocket at `ws://127.0.0.1:8000/ws`.
- Updates: parse WebSocket messages and update the chart and current status cards dynamically.
- Status Indicator: “System Online/Offline” reflects the WebSocket connection state.

