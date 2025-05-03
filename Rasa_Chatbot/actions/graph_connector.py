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
        RETURN DISTINCT m.name AS major , c.name AS method
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
        
    def get_major_by_achievement(self, achievement_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_ACHIEVEMENT]->(a:AchievementField)
        WHERE tolower(a.name) CONTAINS tolower($achievement)
        RETURN m.name AS major, a.name AS achievement
        """
        with self.driver.session() as session:
            result = session.run(query, {"achievement": achievement_keyword})
            return list(result)
    
    def get_majors_by_subjects(self, subject_list: list) -> list:
        """
        Lấy danh sách các ngành học dựa trên danh sách các môn học với logic cải tiến:
        - Pick 2 môn: phù hợp cả 2 môn HOẶC (1 trong 2 môn + toán + ngữ văn)
        - Pick 3 môn: nếu có cả toán và ngữ văn thì cần cả 3, 
                 nếu thiếu 1 trong 2 môn thì yêu cầu toán + ngữ văn + 1 trong 2 môn còn lại
        - Pick 4 môn: cần có 3 trong 4 môn đó trong tổ hợp
    
        Args:
            subject_list (list): Danh sách các môn học (1-4 môn)
    
        Returns:
            list: Danh sách các ngành học phù hợp với các môn học đã cho
        """
        if not subject_list:
            return []
    
        # Chuẩn hóa danh sách môn học để tránh lỗi
        subject_list = subject_list[:4]  # Giới hạn tối đa 4 môn
    
        # Log môn học đầu vào để debug
        print(f"Processing subjects: {subject_list}")
    
        # Trường hợp 1 môn học - giữ nguyên logic cũ
        if len(subject_list) == 1:
            query = """
            MATCH (m:Major)-[:USES_COMBINATION]->(sc:SubjectCombination)
            WHERE toLower(sc.name) CONTAINS toLower($subject1)
            WITH m, collect(sc.name) AS subject_combinations
            RETURN m.id AS major_id, m.name AS major, subject_combinations
            """
            params = {"subject1": subject_list[0]}
    
        # Trường hợp 2 môn học - phù hợp cả 2 môn HOẶC (1 trong 2 môn + toán + ngữ văn)
        elif len(subject_list) == 2:
            query = """
            MATCH (m:Major)-[:USES_COMBINATION]->(sc:SubjectCombination)
            WHERE 
            // Trường hợp 1: Chứa cả 2 môn
            (toLower(sc.name) CONTAINS toLower($subject1) AND toLower(sc.name) CONTAINS toLower($subject2))
            OR 
            // Trường hợp 2: Chứa môn 1 + toán + ngữ văn
            (toLower(sc.name) CONTAINS toLower($subject1) AND toLower(sc.name) CONTAINS toLower('toán') AND toLower(sc.name) CONTAINS toLower('ngữ văn'))
            OR
            // Trường hợp 3: Chứa môn 2 + toán + ngữ văn
            (toLower(sc.name) CONTAINS toLower($subject2) AND toLower(sc.name) CONTAINS toLower('toán') AND toLower(sc.name) CONTAINS toLower('ngữ văn'))
            WITH m, collect(sc.name) AS subject_combinations
            RETURN m.id AS major_id, m.name AS major, subject_combinations
            """
            params = {"subject1": subject_list[0], "subject2": subject_list[1]}
    
        # Trường hợp 3 môn học - logic phức tạp hơn dựa trên có toán và ngữ văn không
        elif len(subject_list) == 3:
            # Kiểm tra xem trong các môn học có toán và/hoặc ngữ văn không
            has_toan = any(subject.lower() == "toán" for subject in subject_list)
            has_nguvan = any(subject.lower() in ["ngữ văn", "văn"] for subject in subject_list)
    
            # Case 1: Nếu có cả toán và ngữ văn trong danh sách
            if has_toan and has_nguvan:
                # Tìm môn còn lại không phải toán và văn
                other_subjects = [s for s in subject_list if s.lower() != "toán" and s.lower() not in ["ngữ văn", "văn"]]
                if other_subjects:
                    other_subject = other_subjects[0]
                    query = """
                        MATCH (m:Major)-[:USES_COMBINATION]->(sc:SubjectCombination)
                        WHERE 
                        toLower(sc.name) CONTAINS toLower('toán') 
                        AND toLower(sc.name) CONTAINS toLower('ngữ văn')
                        AND toLower(sc.name) CONTAINS toLower($other_subject)
                    WITH m, collect(sc.name) AS subject_combinations
                    RETURN m.id AS major_id, m.name AS major, subject_combinations
                    """
                    params = {"other_subject": other_subject}
                else:
                    # Trường hợp chỉ có toán và văn (và có thể có môn trùng), tìm tổ hợp có cả 2
                    query = """
                    MATCH (m:Major)-[:USES_COMBINATION]->(sc:SubjectCombination)
                    WHERE 
                    toLower(sc.name) CONTAINS toLower('toán') 
                    AND toLower(sc.name) CONTAINS toLower('ngữ văn')
                    WITH m, collect(sc.name) AS subject_combinations
                    RETURN m.id AS major_id, m.name AS major, subject_combinations
                    """
                    params = {}
    
                # Case 2: Nếu chỉ có toán (không có ngữ văn)
            elif has_toan:
                # Lấy các môn không phải toán
                other_subjects = [s for s in subject_list if s.lower() != "toán"]
                query = """
                MATCH (m:Major)-[:USES_COMBINATION]->(sc:SubjectCombination)
                WHERE 
                // Trường hợp 1: Toán + ngữ văn + môn 1
                (
                    toLower(sc.name) CONTAINS toLower('toán') 
                    AND toLower(sc.name) CONTAINS toLower('ngữ văn')
                    AND toLower(sc.name) CONTAINS toLower($subject1)
                )
                OR
                // Trường hợp 2: Toán + ngữ văn + môn 2
                (
                    toLower(sc.name) CONTAINS toLower('toán') 
                    AND toLower(sc.name) CONTAINS toLower('ngữ văn')
                    AND toLower(sc.name) CONTAINS toLower($subject2)
                )
                OR
                // Trường hợp 3: Cả 3 môn đã chọn
                (
                    toLower(sc.name) CONTAINS toLower($subject1) 
                    AND toLower(sc.name) CONTAINS toLower($subject2) 
                    AND toLower(sc.name) CONTAINS toLower($subject3)
                )
                WITH m, collect(sc.name) AS subject_combinations
                RETURN m.id AS major_id, m.name AS major, subject_combinations
                """
                params = {
                    "subject1": other_subjects[0] if len(other_subjects) > 0 else subject_list[0],
                    "subject2": other_subjects[1] if len(other_subjects) > 1 else subject_list[1],
                    "subject3": subject_list[2]
                }
    
                # Case 3: Nếu chỉ có ngữ văn (không có toán)
            elif has_nguvan:
                # Lấy các môn không phải ngữ văn
                other_subjects = [s for s in subject_list if s.lower() not in ["ngữ văn", "văn"]]
                query = """
                MATCH (m:Major)-[:USES_COMBINATION]->(sc:SubjectCombination)
                WHERE 
                // Trường hợp 1: Toán + ngữ văn + môn 1
                (
                    toLower(sc.name) CONTAINS toLower('toán') 
                    AND toLower(sc.name) CONTAINS toLower('ngữ văn')
                    AND toLower(sc.name) CONTAINS toLower($subject1)
                )
                OR
                // Trường hợp 2: Toán + ngữ văn + môn 2
                (
                    toLower(sc.name) CONTAINS toLower('toán') 
                    AND toLower(sc.name) CONTAINS toLower('ngữ văn')
                    AND toLower(sc.name) CONTAINS toLower($subject2)
                )
                OR
                // Trường hợp 3: Cả 3 môn đã chọn
                (
                    toLower(sc.name) CONTAINS toLower($subject1) 
                    AND toLower(sc.name) CONTAINS toLower($subject2) 
                    AND toLower(sc.name) CONTAINS toLower($subject3)
                )
                WITH m, collect(sc.name) AS subject_combinations
                RETURN m.id AS major_id, m.name AS major, subject_combinations
            """
                params = {
                    "subject1": other_subjects[0] if len(other_subjects) > 0 else subject_list[0],
                    "subject2": other_subjects[1] if len(other_subjects) > 1 else subject_list[1],
                    "subject3": subject_list[2]
                }
    
            # Trường hợp 4 môn học - cần có ít nhất 3 trong 4 môn
        else:
            query = """
            MATCH (m:Major)-[:USES_COMBINATION]->(sc:SubjectCombination)
            WHERE 
            // Tổ hợp chứa ít nhất 3 trong 4 môn đã chọn
            (
                // Trường hợp 1: Chứa môn 1, 2, 3
                (toLower(sc.name) CONTAINS toLower($subject1) AND toLower(sc.name) CONTAINS toLower($subject2) AND toLower(sc.name) CONTAINS toLower($subject3))
                OR
                // Trường hợp 2: Chứa môn 1, 2, 4
                (toLower(sc.name) CONTAINS toLower($subject1) AND toLower(sc.name) CONTAINS toLower($subject2) AND toLower(sc.name) CONTAINS toLower($subject4))
                OR
                // Trường hợp 3: Chứa môn 1, 3, 4
                (toLower(sc.name) CONTAINS toLower($subject1) AND toLower(sc.name) CONTAINS toLower($subject3) AND toLower(sc.name) CONTAINS toLower($subject4))
                OR
                // Trường hợp 4: Chứa môn 2, 3, 4
                (toLower(sc.name) CONTAINS toLower($subject2) AND toLower(sc.name) CONTAINS toLower($subject3) AND toLower(sc.name) CONTAINS toLower($subject4))
            )
            WITH m, collect(sc.name) AS subject_combinations
            RETURN m.id AS major_id, m.name AS major, subject_combinations
            """
            params = {
                "subject1": subject_list[0], 
                "subject2": subject_list[1], 
                "subject3": subject_list[2], 
                "subject4": subject_list[3]
            }
    
            # Thực thi truy vấn
        with self.driver.session() as session:
            result = session.run(query, params)
            results = list(result)
        
            # Log kết quả để debug
            if results:
                print(f"Found {len(results)} matching majors")
                if len(results) > 0:
                    print(f"Sample Neo4j result: {dict(results[0])}")
                    print(f"subject_combinations type: {type(results[0]['subject_combinations'])}")
                    print(f"subject_combinations value: {results[0]['subject_combinations']}")
            else:
                print(f"No matching majors found for subjects: {subject_list}")
            
            return results
