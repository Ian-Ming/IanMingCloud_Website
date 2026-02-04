import azure.functions as func
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    # For now, we will return a hardcoded number. 
    # Once the DB is connected, we will change this logic.
    mock_count = 124 
    
    return func.HttpResponse(
        body=json.dumps({"count": mock_count}),
        status_code=200,
        mimetype="application/json"
    )