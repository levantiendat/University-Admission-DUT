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
        m.major_url AS majorUrl,
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
        m.major_url AS majorUrl,
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
        RETURN DISTINCT m.name AS major , c.name AS method, c.method_url AS methodUrl
        """
        with self.driver.session() as session:
            result = session.run(query, {"method": method_keyword})
            return list(result)
    
    def get_combination_subjects(self, major_keyword: str):
        query = """
        MATCH (m:Major)
        WHERE m.id = $major
        MATCH (m)-[:USES_COMBINATION]->(sc:SubjectCombination)
        RETURN sc.name AS subject_combination , m.name AS major, m.major_url AS majorUrl
        """
        with self.driver.session() as session:
            result = session.run(query, {"major": major_keyword})
            return list(result)
        
    def get_method_by_major(self, major_keyword: str):
        query = """
        MATCH (m:Major)-[r:HAS_METHOD_2025]->(c:Method)
        WHERE m.id = $major
        RETURN DISTINCT m.name as major, m.major_url as majorUrl, c.name AS method
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
        m.major_url AS majorUrl,
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
        RETURN m.id AS major_id, m.name AS name, m.major_url AS majorUrl, m.quota AS quota
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
        
    def get_majors_by_faculty(self, faculty_id: str) -> list:
        """
        Lấy danh sách các ngành học thuộc một khoa dựa trên ID khoa
    
        Args:
            faculty_id (str): ID của khoa cần tìm kiếm
    
        Returns:
            list: Danh sách các ngành học thuộc khoa, bao gồm tên ngành và tên khoa
                Mỗi phần tử có định dạng {"major": tên ngành, "major_id": id ngành, "faculty": tên khoa}
        """
        query = """
        MATCH (f:Faculty)<-[:MajorInFaculty]-(m:Major)
        WHERE f.id = $faculty_id
        RETURN m.name AS major, m.id AS major_id, f.name AS faculty
        ORDER BY m.name
        """
    
        try:
            with self.driver.session() as session:
                result = session.run(query, {"faculty_id": faculty_id})
                results = list(result)
            
                # Log kết quả để debug
                if results:
                    print(f"Found {len(results)} majors in faculty ID: {faculty_id}")
                    if len(results) > 0:
                        print(f"Sample major: {dict(results[0])}")
                else:
                    print(f"No majors found for faculty ID: {faculty_id}")
                
                return results
        except Exception as e:
            print(f"Error querying Neo4j: {str(e)}")
            return []
        
    def get_majors_by_score_and_method(self, score: float, method_id: str) -> list:
        """
        Gợi ý các ngành phù hợp với điểm số của thí sinh dựa trên phương thức xét tuyển
    
        Args:
            score (float): Điểm số của thí sinh
            method_id (str): ID của phương thức xét tuyển (dgnl, hb_thpt, tn_thpt, dgtd, xtr)
    
        Returns:
            list: Danh sách các ngành được phân loại thành 3 nhóm: tỷ lệ đỗ cao, trung bình và thấp
                [{"group": "high|medium|low", "majors": [{"major_name": str, "major_id": str, "cutoff": float, "year": int}]}]
        """
        # Xác định khung điểm dựa trên phương thức
        max_score = 0
        if method_id == "dgnl":  # Đánh giá năng lực
            max_score = 1200
        elif method_id in ["hb_thpt", "tn_thpt"]:  # Học bạ và điểm thi tốt nghiệp
            max_score = 30
        elif method_id == "dgtd":  # Đánh giá tư duy
            max_score = 100
        elif method_id == "xtr":  # Xét tuyển riêng
            max_score = 300
    
        if max_score == 0:
            print(f"Invalid method ID: {method_id}")
            return []
    
        # Tính khoảng điểm gợi ý
        min_suggestion = max(0, score - 0.3 * max_score)
        max_suggestion = min(max_score, score + 0.1 * max_score)
    
        print(f"Suggesting majors with score from {min_suggestion} to {max_suggestion} for method {method_id}")
    
        # Truy vấn để lấy điểm chuẩn các ngành theo khoảng điểm
        query = """
        MATCH (m:Major)-[r:HAS_CUTOFF]->(c:Cutoff)
        WHERE c.method = $method_id 
        AND c.year IN [2023, 2024]
        AND c.score <= $max_suggestion
        RETURN 
            m.id AS major_id, 
            m.name AS major_name, 
            c.score AS cutoff, 
            c.year AS year,
            ABS(c.score - $score) AS score_diff
        ORDER BY score_diff
        LIMIT 30
        """
    
        try:
            with self.driver.session() as session:
                result = session.run(query, {
                    "method_id": method_id,
                    "score": score,
                    "max_suggestion": max_suggestion
                })
                results = list(result)
            
                if not results:
                    print(f"No matching majors found for score {score} with method {method_id}")
                    return []
            
                print(f"Found {len(results)} matching majors")
            
                # Phân loại kết quả thành 3 nhóm
                grouped_results = self._group_majors_by_success_rate(results, score)
            
                return grouped_results
            
        except Exception as e:
            print(f"Error querying Neo4j: {str(e)}")
            return []
    
    def _group_majors_by_success_rate(self, results: list, target_score: float) -> list:
        """
        Phân loại các ngành thành 3 nhóm dựa trên so sánh điểm chuẩn với điểm đầu vào:
        - Tỷ lệ đỗ cao: điểm chuẩn <= điểm đầu vào + 0.05*điểm max
        - Tỷ lệ đỗ trung bình và thấp: phân loại các ngành có điểm cao hơn
    
        Args:
            results (list): Danh sách kết quả từ Neo4j
            target_score (float): Điểm số đầu vào của thí sinh
    
        Returns:
            list: Danh sách các nhóm ngành được phân loại
        """
        if not results:
            return []

        # Xác định điểm tối đa dựa theo phương thức xét tuyển
        # Lấy method từ kết quả đầu tiên nếu có
        max_score = 0
        if results and len(results) > 0:
            method_id = results[0].get("methodId", "")
            if method_id == "dgnl":
                max_score = 1200
            elif method_id in ["hb_thpt", "tn_thpt"]:
                max_score = 30
            elif method_id == "dgtd":
                max_score = 100
            elif method_id == "xtr":
                max_score = 300
            else:
                # Nếu không xác định được, lấy điểm cao nhất trong kết quả
                max_score = max([r["cutoff"] for r in results]) * 1.2
    
        # Tính ngưỡng điểm để xác định tỷ lệ cao
        high_threshold = target_score + 0.05 * max_score
        print(f"Target score: {target_score}, High threshold: {high_threshold}, Max score: {max_score}")
    
        # Phân loại thành 3 nhóm
        high_majors = []    # Tỷ lệ đỗ cao (điểm chuẩn <= threshold)
        remaining_majors = [] # Các ngành có điểm cao hơn threshold
    
        # Phân loại ban đầu thành 2 nhóm: cao và còn lại
        for result in results:
            major_info = {
                "major_name": result["major_name"],
                "major_id": result["major_id"],
                "cutoff": result["cutoff"],
                "year": result["year"]
            }
        
            if result["cutoff"] <= high_threshold:
                high_majors.append(major_info)
            else:
                remaining_majors.append((major_info, result["score_diff"]))
    
        # Giới hạn tổng số ngành ở mức 15
        total_majors = len(high_majors) + len(remaining_majors)
        if total_majors > 15:
            limit_remaining = 15 - min(len(high_majors), 15)
            if limit_remaining > 0 and len(remaining_majors) > limit_remaining:
                # Sắp xếp theo khoảng cách tăng dần và giới hạn số lượng
                remaining_majors.sort(key=lambda x: x[1])
                remaining_majors = remaining_majors[:limit_remaining]
        
            # Nếu high_majors quá nhiều, cũng giới hạn lại
            if len(high_majors) > 15:
                high_majors = high_majors[:15]
    
        # Tiếp tục phân loại các ngành còn lại thành trung bình và thấp
        medium_majors = []  # Tỷ lệ đỗ trung bình
        low_majors = []     # Tỷ lệ đỗ thấp
    
        if remaining_majors:
            # Sắp xếp theo khoảng cách tăng dần
            remaining_majors.sort(key=lambda x: x[1])
        
            split_index = len(remaining_majors) // 2
        
            # Phân nhóm medium và low
            medium_majors = [item[0] for item in remaining_majors[:split_index]]
            low_majors = [item[0] for item in remaining_majors[split_index:]]
    
        # Tạo cấu trúc kết quả
        result = []
    
        if high_majors:
            result.append({
                "group": "high",
                "majors": high_majors
            })
    
        if medium_majors:
            result.append({
                "group": "medium",
                "majors": medium_majors
            })
    
        if low_majors:
            result.append({
                "group": "low",
                "majors": low_majors
            })
    
        return result
    
    def get_majors_by_score_method_and_faculty(self, score: float, method_id: str, faculty_id: str) -> list:
        """
        Gợi ý các ngành thuộc một khoa cụ thể phù hợp với điểm số của thí sinh dựa trên phương thức xét tuyển
    
        Args:
            score (float): Điểm số của thí sinh
            method_id (str): ID của phương thức xét tuyển (dgnl, hb_thpt, tn_thpt, dgtd, xtr)
            faculty_id (str): ID của khoa
    
        Returns:
            list: Danh sách các ngành trong khoa được phân loại thành 3 nhóm: tỷ lệ đỗ cao, trung bình và thấp
                [{"group": "high|medium|low", "majors": [{"major_name": str, "major_id": str, "cutoff": float, "year": int}]}]
        """
        # Truy vấn để lấy các ngành thuộc khoa cụ thể có điểm chuẩn theo phương thức xét tuyển
        query = """
        MATCH (f:Faculty)<-[:MajorInFaculty]-(m:Major)-[r:HAS_CUTOFF]->(c:Cutoff)
        WHERE f.id = $faculty_id
            AND c.method = $method_id 
            AND c.year IN [2023, 2024]
        RETURN 
            m.id AS major_id, 
            m.name AS major_name,
            f.name AS faculty_name,
            c.score AS cutoff, 
            c.year AS year,
            CASE WHEN c.score <= $score THEN true ELSE false END AS is_eligible,
            ABS(c.score - $score) AS score_diff
        ORDER BY is_eligible DESC, score_diff
        """
    
        try:
            with self.driver.session() as session:
                result = session.run(query, {
                    "faculty_id": faculty_id,
                    "method_id": method_id, 
                    "score": score
                })
                results = list(result)
            
                if not results:
                    print(f"No matching majors found in faculty ID {faculty_id} for score {score} with method {method_id}")
                    return []
            
                print(f"Found {len(results)} matching majors in faculty {faculty_id}")
            
                # Sắp xếp kết quả thành các nhóm
                # Tất cả các ngành có điểm chuẩn <= điểm người dùng có sẽ vào nhóm khả năng cao
                # Còn lại phân nhóm dựa trên khoảng cách với điểm người dùng
                grouped_results = self._group_majors_by_eligibility(results, score)
            
                return grouped_results
        
        except Exception as e:
            print(f"Error querying Neo4j: {str(e)}")
            return []

    def _group_majors_by_eligibility(self, results: list, target_score: float) -> list:
        """
        Phân loại các ngành dựa trên khả năng đỗ (điểm chuẩn <= điểm người dùng và khoảng cách với điểm mục tiêu)
    
        Args:
            results (list): Danh sách kết quả từ Neo4j
            target_score (float): Điểm số mục tiêu
        
        Returns:
            list: Danh sách các nhóm ngành được phân loại
        """
        if not results:
            return []
    
        groups = {
            "high": [],    # Tỷ lệ đỗ cao (điểm chuẩn <= điểm người dùng)
            "medium": [],  # Tỷ lệ đỗ trung bình (điểm chuẩn > điểm người dùng nhưng chênh lệch nhỏ)
            "low": []      # Tỷ lệ đỗ thấp (điểm chuẩn > điểm người dùng và chênh lệch lớn)
        }
    
        # Trước hết, xác định ngành nào đủ điểm (điểm >= điểm chuẩn)
        eligible_majors = []
        ineligible_majors = []
    
        for result in results:
            major_info = {
                "major_name": result["major_name"],
                "major_id": result["major_id"],
                "cutoff": result["cutoff"],
                "year": result["year"]
            }
        
            if result["is_eligible"]:
                eligible_majors.append(major_info)
            else:
                ineligible_majors.append((major_info, result["score_diff"]))
    
        # Tất cả các ngành đủ điểm vào nhóm tỷ lệ đỗ cao
        groups["high"] = eligible_majors
    
        # Các ngành không đủ điểm phân nhóm theo khoảng cách với điểm mục tiêu
        if ineligible_majors:
            # Sắp xếp theo khoảng cách tăng dần
            ineligible_majors.sort(key=lambda x: x[1])
        
            total_ineligible = len(ineligible_majors)
            split_index = total_ineligible // 2
        
            # Phân chia các ngành không đủ điểm thành 2 nhóm: medium và low
            groups["medium"] = [item[0] for item in ineligible_majors[:split_index]]
            groups["low"] = [item[0] for item in ineligible_majors[split_index:]]
    
        # Chuyển đổi kết quả để trả về
        result = []
        for group_name, majors in groups.items():
            if majors:  # Chỉ thêm nhóm có dữ liệu
                result.append({
                    "group": group_name,
                    "majors": majors
                })
    
        return result
    
    def get_faculty_name_by_id(self, faculty_id: str) -> str:
        """
        Lấy tên của khoa dựa vào ID
    
        Args:
            faculty_id (str): ID của khoa
        
        Returns:
            str: Tên khoa hoặc None nếu không tìm thấy
        """
        query = """
            MATCH (f:Faculty)
            WHERE f.id = $faculty_id
            RETURN f.name AS faculty_name
        """
    
        try:
            with self.driver.session() as session:
                result = session.run(query, {"faculty_id": faculty_id})
                record = result.single()
            
                if record:
                    return record["faculty_name"]
                return None
        except Exception as e:
            print(f"Error querying Neo4j: {str(e)}")
            return None
    
