from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_BASE_URL = "http://127.0.0.1:5000"
API_TIMEOUT_SECONDS = 5


@app.get("/")
def index():
    try:
        response = requests.get(
            f"{API_BASE_URL}/menu",
            timeout=API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        menu = response.json()
        return render_template("index.html", menu=menu, result=None, error=None)
    except requests.RequestException:
        return (
            render_template(
                "index.html",
                menu={},
                result=None,
                error="The canteen API is unavailable. Please start the API server first.",
            ),
            503,
        )


@app.post("/order")
def order():
    item = request.form.get("item", "")
    quantity_text = request.form.get("quantity", "")

    try:
        quantity = int(quantity_text)
        if quantity < 1:
            raise ValueError
    except (TypeError, ValueError):
        return render_page_with_error("Please enter a quantity of at least 1.", 400)

    try:
        response = requests.post(
            f"{API_BASE_URL}/order",
            json={"item": item, "quantity": quantity},
            timeout=API_TIMEOUT_SECONDS,
        )
        data = response.json()

        if not response.ok:
            return render_page_with_error(
                data.get("error", "Your order could not be placed."),
                response.status_code,
            )

        menu_response = requests.get(
            f"{API_BASE_URL}/menu",
            timeout=API_TIMEOUT_SECONDS,
        )
        menu_response.raise_for_status()
        return render_template(
            "index.html",
            menu=menu_response.json(),
            result=data,
            error=None,
        )
    except (requests.RequestException, ValueError):
        return render_page_with_error(
            "Could not contact the canteen API. Please try again.",
            503,
        )


def render_page_with_error(message, status_code):
    """Render the page with a user-friendly error message."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/menu",
            timeout=API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        menu = response.json()
    except requests.RequestException:
        menu = {}

    return (
        render_template("index.html", menu=menu, result=None, error=message),
        status_code,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
