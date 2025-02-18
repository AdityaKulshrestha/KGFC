from neo4j import GraphDatabase 


URI = "neo4j://localhost"
AUTH = ("Aditya": "Aditya02")

with GraphDatabase.drive(URI, auth=AUTH) as driver:
    driver.verify_connectivity()