from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
import boto3
import json

logger = Logger(service="APP")

app = APIGatewayRestResolver()

@app.get("/hello/<name>")
def hello_name(name):
    logger.info(f"Request from {name} received")
    return {"message": f"hello {name}!"}

# @app.post("/db_init")
# def db_init():
#     logger.info("db initialized")


@app.get("/hello")
def hello():
    logger.info("Request from unknown received")
    # f = open('teams.json')
    # request_items = json.loads(f.read())
    # dynamodb = boto3.resource('dynamodb', region_name = 'eu-central-1')
    # client = boto3.client('dynamodb')
    # response = client.batch_write_item(RequestItems=request_items) 

    dynamodb = boto3.client('dynamodb', region_name = 'eu-central-1')

    with open('teams.json', 'r') as json_file:
        data = json.load(json_file)
    requests = [item["PutRequest"] for item in data]

    # response = dynamodb.batch_write_item(
    # RequestItems={
    #     'teams': requests
    # }
    # )

    return requests

@app.get("/team/<team>")
def get_team(team):
    logger.info("Request for one team received")

    dynamodb = boto3.resource('dynamodb', region_name = 'eu-central-1')
    table = dynamodb.Table('teams')
    key = { 'name': team }

    response = table.get_item(Key=key)

    item = response["Item"]

    return item

@app.get("/teams")
def get_teams():
    logger.info("Request from unknown received")

    dynamodb = boto3.resource('dynamodb', region_name = 'eu-central-1')
    table = dynamodb.Table('teams')
    key = { 'name': 'Ferrari' }

    response = table.get_item(Key=key)

    item = response["Item"]

    return item

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
def lambda_handler(event, context):
    return app.resolve(event, context)