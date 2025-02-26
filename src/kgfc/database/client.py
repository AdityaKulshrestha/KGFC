import os
from contextlib import contextmanager
from typing import Any, Dict, Optional
from neo4j import GraphDatabase, Session, Transaction
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path, override=True)


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.environ['NEO4J_URI'],
            auth=(os.environ['NEO4J_USER'], os.environ['NEO4J_PASSWORD'])
        )

    def close(self):
        self.driver.close()

    def get_session(self):
        return self.driver.session()


class Neo4jConnection:
    """
    New Neo4j client - version2
    Handles connection lifecycle using context manager
    """
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.environ['NEO4J_URI'],
            auth=(os.environ['NEO4J_USER'], os.environ['NEO4J_PASSWORD'])
        )

    def __enter__(self):
        return self
    
    def __exit__(self, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.driver:
            self.driver.close()
 
    @contextmanager
    def session(self, **kwargs) -> Session:
        """Provides a session using a context manager"""
        with self.driver.session(**kwargs) as session:
            yield session


class Neo4jManager:
    """Handles database operations using the connection"""
    def __init__(self):
        self.connection = Neo4jConnection()

    def execute_query(self, query: str, parameters: Optional[Dict] = None, **kwargs) -> Any:
        """Generic method to execute a Cypher query"""
        with self.connection.session(**kwargs) as session:
            result = session.execute_write(self._execute_transaction, query, parameters or {})
            return [dict(record) for record in result] if result else None

    @staticmethod
    def _execute_transaction(tx: Transaction, query: str, parameters: Dict) -> Any:
        result = tx.run(query, parameters)
        try:
            return result.data()
        except Exception as e:
            # Handle or log exception
            raise e

    def create_node(self, label: str, properties: Dict, **kwargs) -> Any:
        """Create a node with given label and properties"""
        query = f"CREATE (n: {label} $props) RETURN n"
        return self.execute_query(query, {"props": properties}, **kwargs)

    def create_relationship(self, from_id: Any, to_id: Any, rel_type: str, properties: Optional[Dict] = None, **kwargs) -> Any:
        """Create relation between two nodes"""
        query = (
            "MATCH (a), (b) "
            "WHERE elementId(a) = $from_id AND elementId(b) = $to_id "
            f"CREATE (a)-[r: {rel_type} $props]->(b) RETURN r"
        )
        params = {"from_id": from_id, "to_id": to_id, "props": properties or {}}
        return self.execute_query(query, params, **kwargs)

    
