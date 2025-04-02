from .client import Neo4jManager
from kgfc.embedding import CodeEmbedder
from loguru import logger


def retrieve_code(query: str, repo_name: str, top_k: int = 3):
    client = Neo4jManager()
    code_embedder = CodeEmbedder()

    query_embedding = code_embedder.generate_embedding(query)

    match_query = """
        WITH $repoName AS repoName, $queryEmbedding AS queryEmbedding, 3 AS topN
        // Match the repo node dynamically
        MATCH (repo: Repository {repo_name: repoName})
        // Find the distant children with embedding
        MATCH (repo)-[*]->(child)
        WHERE child.embedding IS NOT NULL
        // Compute cosine similarity and return the top 3 matches
        WITH child, gds.similarity.cosine(queryEmbedding, child.embedding) AS similarity
        ORDER BY similarity DESC
        // Use the proper CALL syntax with variable scope
        CALL {
            WITH child, similarity  // Pass variables explicitly in scope clause
            RETURN child AS bestMatch, similarity AS score
            ORDER BY score DESC
            LIMIT 3
        }
        RETURN bestMatch, score
    """

    parameters = {'repoName': repo_name, 'queryEmbedding': query_embedding, 'top_k': top_k}
    class_nodes = client.execute_query(match_query, parameters)
    
    logger.info(f"Retrieved Results: {class_nodes}")
    return class_nodes

    
