import azure.functions as func
import json
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # 1. We import INSIDE the function so the 404 goes away
        from azure.cosmos import CosmosClient
        
        # 2. Get the connection string from your Portal environment variables
        conn_str = os.environ.get("CosmosDBConnectionString")
        if not conn_str:
            return func.HttpResponse("Error: CosmosDBConnectionString not found in Azure settings.", status_code=500)

        # 3. Connect to the client
        client = CosmosClient.from_connection_string(conn_str)
        database = client.get_database_client("AzureResume")
        container = database.get_container_client("Counter")
        
        # 4. Read the item (ensure id="1" and partition_key="1" match your Data Explorer)
        item = container.read_item(item="1", partition_key="1")
        item["count"] += 1
        
        # 5. Save it back
        container.replace_item(item="1", body=item)
        
        return func.HttpResponse(
            json.dumps({"count": item["count"]}),
            mimetype="application/json",
            status_code=200
        )

    except ImportError:
        return func.HttpResponse("Import Error: azure-cosmos library is still not installed on the server.", status_code=500)
    except Exception as e:
        return func.HttpResponse(f"Database/Logic Error: {str(e)}", status_code=500)