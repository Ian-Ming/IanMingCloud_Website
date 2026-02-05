import azure.functions as func
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    # Hardcoded response to rule out Cosmos DB
    return func.HttpResponse(
        json.dumps({"count": 999, "message": "Cosmos is ruled out!"}),
        mimetype="application/json",
        status_code=200
    )