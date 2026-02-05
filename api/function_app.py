import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # 1. Check for the connection string first
        conn_str = os.environ.get("CosmosDBConnectionString")
        if not conn_str:
            return func.HttpResponse("Error: CosmosDBConnectionString is missing in Portal settings.", status_code=500)

        # 2. Connect
        client = CosmosClient.from_connection_string(conn_str)
        database = client.get_database_client("AzureResume")
        container = database.get_container_client("Counter")
        
        # 3. Read and Update
        item = container.read_item(item="1", partition_key="1")
        item["count"] += 1
        container.replace_item(item="1", body=item)
        
        return func.HttpResponse(json.dumps({"count": item["count"]}), mimetype="application/json", status_code=200)

    except Exception as e:
        # This will return the actual error message to your browser instead of a 404!
        return func.HttpResponse(f"Crash details: {str(e)}", status_code=500)