from neo4j import GraphDatabase
import os

class Neo4jConnection:
    def __init__(self, server, password):
        self.driver = GraphDatabase.driver(f"bolt://{server}:7687", auth=("neo4j", password))
    
    def close(self):
        self.driver.close()
    
    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters)
        
    def get_session(self):
        return self.driver.session()
    
def local_neo4j():
    action_password = os.environ.get("LOCAL_ACTION_PASSWORD")
    action_server = os.environ.get("LOCAL_ACTION_SERVER")
    return Neo4jConnection(action_server, action_password)

def global_neo4j():
    action_password = os.environ.get("GLOBAL_ACTION_PASSWORD")
    action_server = os.environ.get("GLOBAL_ACTION_SERVER")
    return Neo4jConnection(action_server, action_password)