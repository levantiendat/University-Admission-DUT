from neo4j import GraphDatabase

class GraphConnector:
    def __init__(self):
        self.uri = "neo4j+s://159fcaec.databases.neo4j.io"
        self.username = "neo4j"
        self.password = "crlyf1jA-cjW1LNZ00jQv-t1Y-xYr_BqS8fsWXQNRFk"
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def get_cutoff_by_major_and_method(self, major_keyword: str, method_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_CUTOFF]->(c:Cutoff)
        WHERE m.id CONTAINS $major
          AND r.method CONTAINS $method
        RETURN m.name AS major, r.method AS method, c.year AS year, c.score AS score
        ORDER BY c.year DESC
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword, "method": method_keyword})
            return list(result)

    def get_all_cutoffs_by_major(self, major_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_CUTOFF]->(c:Cutoff)
        WHERE m.id CONTAINS $major
        RETURN r.method AS method, c.year AS year, c.score AS score, m.name AS major
        ORDER BY r.method, c.year DESC
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword})
            return list(result)

    def get_all_cutoffs_by_method(self, method_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_CUTOFF]->(c:Cutoff)
        WHERE r.method CONTAINS $method
        RETURN m.name AS major, c.year AS year, c.score AS score
        ORDER BY m.name, c.year DESC
        """
        with self.driver.session() as session:
            result = session.run(query, {"method": method_keyword})
            return list(result)
    
    def get_major_by_method(self, method_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_METHOD_2025]->(c:Method)
        WHERE c.id CONTAINS $method
        RETURN DISTINCT m.name AS major
        """
        with self.driver.session() as session:
            result = session.run(query, {"method": method_keyword})
            return list(result)
    
    def get_combination_subjects(self, major_keyword: str):
        query = """
        MATCH (m:Major)
        WHERE toLower(m.name) = toLower($major)
        MATCH (m)-[:USES_COMBINATION]->(sc:SubjectCombination)
        RETURN sc.name AS subject_combination
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword})
            return list(result)
