# Campus Canteen API

A beginner-friendly Python project demonstrating how a web application communicates with a REST API. The project has two Flask applications:

- **API server** (`canteen_api/server.py`) — returns the menu and processes orders as JSON.
- **Website client** (`canteen_website/website.py`) — displays the menu and sends order requests to the API using Python's `requests` library.

## Features

- View the canteen menu and prices.
- Place an order with a chosen quantity.
- Receive a JSON response with order ID, unit price, total, and status.
- Validate menu items and quantities.
- Handle API connection errors.
- Responsive HTML/CSS interface.

> This is an educational demo. Menu data and order IDs are stored in memory, so they reset when the API server restarts. It does not use a database or payment processing.

## Project structure

```text
campus_canteen_api/
├── canteen_api/
│   └── server.py
├── canteen_website/
│   ├── website.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- pip

## Run locally

### 1. Open a terminal in the project folder

Create and activate a virtual environment (recommended).

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the API server

Open **Terminal 1** in the project folder:

```bash
python canteen_api/server.py
```

The API will run at `http://127.0.0.1:5000`.

### 4. Start the website

Open **Terminal 2** in the same project folder, activate the same virtual environment if needed, and run:

```bash
python canteen_website/website.py
```

Open `http://127.0.0.1:5001` in your browser.

**Both servers must be running** for the website to retrieve the menu and submit orders.

## API endpoints

### `GET /menu`

Returns the menu as JSON.

Example response:

```json
{
  "Water bottle": 20,
  "Pizza": 199,
  "Salad": 120
}
```

Actual response includes all menu items configured in `server.py`.

### `POST /order`

Accepts a JSON request body:

```json
{
  "item": "Pizza",
  "quantity": 2
}
```

Successful response (HTTP `201 Created`):

```json
{
  "order_id": 101,
  "item": "Pizza",
  "quantity": 2,
  "unit_price": 199,
  "total": 398,
  "status": "Order Placed"
}
```

Invalid requests return an error message with an appropriate HTTP status code.

## How the API works in this project

1. The browser sends a form submission to the website Flask app on port `5001`.
2. The website reads the selected item and quantity.
3. The website uses `requests.post()` to send a JSON request to the API server on port `5000`.
4. The API validates the input and calculates the total price.
5. The API returns JSON with the order details.
6. The website reads the JSON response and renders the confirmation page.

**Flow:** Browser → Website Flask app → HTTP/JSON request → API Flask app → JSON response → Website → Browser.

## Test the API directly

With the API server running, open another terminal and run:

```bash
curl http://127.0.0.1:5000/menu
```

To submit an order:

```bash
curl -X POST http://127.0.0.1:5000/order \
  -H "Content-Type: application/json" \
  -d '{"item":"Pizza","quantity":2}'
```

## Viva quick notes

- **API:** An interface that lets software components communicate.
- **REST API:** An API commonly using HTTP methods and resource URLs.
- **Endpoint:** A URL path that exposes an operation or resource.
- **GET:** Retrieves data.
- **POST:** Sends data to the server, often to create a resource.
- **JSON:** A data format used to exchange structured information.
- **`request.get_json()`:** Reads and parses JSON sent to a Flask endpoint.
- **`jsonify()`:** Converts Python data into an HTTP JSON response.
- **`requests.get()` / `requests.post()`:** Sends HTTP requests from the website app to the API.
- **HTTP 200:** Request succeeded.
- **HTTP 201:** A resource/order was created successfully.
- **HTTP 400:** The request contains invalid input.
- **HTTP 503:** The website could not reach the API service.

## Upload to GitHub

From the project folder:

```bash
git init
git add .
git commit -m "Build campus canteen REST API"
```

Create an empty repository on GitHub, then follow GitHub's instructions to connect it as a remote and push the commit. Do not commit virtual environments, passwords, tokens, or other secrets.
