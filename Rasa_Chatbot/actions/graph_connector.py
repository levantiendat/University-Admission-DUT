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
        MATCH (method:Method {id: c.method})
        WHERE m.id = $major
            AND c.method CONTAINS $method
        RETURN m.name AS major, 
        method.name AS method, 
        c.method AS methodId, 
        c.year AS year, 
        c.score AS score
        ORDER BY c.year DESC
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword, "method": method_keyword})
            return list(result)

    def get_all_cutoffs_by_major(self, major_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_CUTOFF]->(c:Cutoff)
        MATCH (method:Method {id: c.method})
        WHERE m.id = $major
        RETURN m.name AS major, 
        method.name AS method, 
        c.method AS methodId, 
        c.year AS year, 
        c.score AS score
        ORDER BY c.year DESC
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword})
            return list(result)

    def get_all_cutoffs_by_method(self, method_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_CUTOFF]->(c:Cutoff)
        MATCH (method:Method {id: c.method})
        WHERE c.method CONTAINS $method
        RETURN m.name AS major, 
        method.name AS method, 
        c.method AS methodId, 
        c.year AS year, 
        c.score AS score
        ORDER BY c.year DESC
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
        WHERE m.id = $major
        MATCH (m)-[:USES_COMBINATION]->(sc:SubjectCombination)
        RETURN sc.name AS subject_combination , m.name AS major
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword})
            return list(result)
        
    def get_method_by_major(self, major_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_METHOD_2025]->(c:Method)
        WHERE m.id = $major
        RETURN DISTINCT m.name as major, c.name AS method
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword})
            return list(result)
        
    def check_major_has_method(self, major_id: str, method_id: str):
        """
    Kiểm tra xem ngành học có sử dụng phương thức tuyển sinh cụ thể không
    và trả về thông tin chi tiết về ngành và phương thức
    
    Args:
        major_id (str): ID của ngành học
        method_id (str): ID của phương thức tuyển sinh
        
    Returns:
        dict: Dictionary chứa thông tin về kết quả kiểm tra và chi tiết ngành/phương thức
            {
                "exists": boolean,           # True nếu ngành có phương thức này
                "major_id": str,             # ID của ngành
                "major_name": str,           # Tên ngành (nếu tìm thấy)
                "method_id": str,            # ID của phương thức
                "method_name": str,          # Tên phương thức (nếu tìm thấy)
            }
        """
        query = """
        MATCH (m:Major)
        WHERE m.id = $major
    OPTIONAL MATCH (mt:Method)
    WHERE mt.id = $method
    OPTIONAL MATCH (m)-[r:HAS_METHOD_2025]->(mt)
    RETURN 
        m.id AS major_id, 
        m.name AS major_name,
        mt.id AS method_id,
        mt.name AS method_name,
        CASE WHEN r IS NULL THEN false ELSE true END AS exists
    """
    
        with self.driver.session() as session:
            result = session.run(query, {"major": major_id, "method": method_id})
            record = result.single()
        
            if record:
                return {
                    "exists": record["exists"],
                    "major_id": record["major_id"],
                    "major_name": record["major_name"],
                    "method_id": record["method_id"],
                    "method_name": record["method_name"]
                }
        
        # Nếu không tìm thấy record, có thể ID không tồn tại
            return {
                "exists": False,
                "major_id": major_id,
                "major_name": None,
                "method_id": method_id,
                "method_name": None
            }
        
    def get_major_quota_and_name(self, major_id: str) -> dict:
        """
        Lấy thông tin về chỉ tiêu (quota) và tên của ngành học

        Args:
            major_id (str): ID của ngành học cần truy vấn

        Returns:
            dict: Dictionary chứa thông tin của ngành học
                {
                    "major_id": str,     # ID của ngành
                    "name": str,         # Tên ngành 
                    "quota": int,        # Chỉ tiêu tuyển sinh của ngành
                    "found": bool        # True nếu tìm thấy ngành, False nếu không
                }
        """
        query = """
        MATCH (m:Major)
        WHERE m.id = $major
        RETURN m.id AS major_id, m.name AS name, m.quota AS quota
        """
    
        with self.driver.session() as session:
            result = session.run(query, {"major": major_id})
            record = result.single()
        
            if record:
                return {
                    "major_id": record["major_id"],
                    "name": record["name"],
                    "quota": record["quota"],
                    "found": True
                }
        
            # Trả về giá trị mặc định nếu không tìm thấy ngành
            return {
                "major_id": major_id,
                "name": None,
                "quota": None,
                "found": False
            }
