from typing import List, Dict, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.graph_connector import GraphConnector
from actions.mapping_utils import normalize_major, normalize_method, normalize_achievement_field, normalize_subject, normalize_faculty  # Import các hàm tiện ích
import logging
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction

# Cấu hình logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ActionCutoffScore(Action):
    def name(self) -> str:
        return "action_cutoff_score"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
            
        # Lấy dữ liệu từ tracker
        major_input = tracker.get_slot("major")
        method_input = tracker.get_slot("method")
        
        # Chuẩn hóa dữ liệu sử dụng các hàm từ mapping_utils
        major_keyword = normalize_major(major_input)
        method_keyword = normalize_method(method_input)

        print(f"Normalized major: {major_keyword}, Normalized method: {method_keyword}")
        logging.debug(f"Normalized major: {major_keyword}, Normalized method: {method_keyword}")
        
        # Truy vấn và xử lý kết quả
        if major_keyword and method_keyword:
            rows = self.db.get_cutoff_by_major_and_method(major_keyword, method_keyword)
            if rows:
                message = f"**Điểm chuẩn phương thức {rows[0]['method']} của ngành {rows[0]['major']}**:\n"
                for row in rows:
                    message += f"- Năm {row['year']}: {row['score']}\n"
                message += f"Thí sinh có thể tham khảo thêm thông tin chi tiết về ngành ở {rows[0]['majorUrl']} "
            else:
                message = "❌ Không có dữ liệu cho ngành và phương thức bạn yêu cầu."

        elif major_keyword:
            rows = self.db.get_all_cutoffs_by_major(major_keyword)
            if rows:
                message = f"📌 **Điểm chuẩn của ngành {rows[0]['major']}**:\n"
                grouped = {}
                for row in rows:
                    grouped.setdefault(row["method"], []).append(f"  - Năm {row['year']}: {row['score']}")
                for method, scores in grouped.items():
                    message += f"\n👉 {method}:\n" + "\n".join(scores)
                message += f"Bạn có thể tham khảo thêm thông tin chi tiết về ngành ở {rows[0]['majorUrl']}"
            else:
                message = "❌ Không tìm thấy điểm chuẩn cho ngành bạn hỏi."

        elif method_keyword:
            rows = self.db.get_all_cutoffs_by_method(method_keyword)
            if rows:
                message = f"📊 **Điểm chuẩn theo phương thức {method_keyword}**:\n"
                current_major = ""
                for row in rows:
                    if row['major'] != current_major:
                        current_major = row['major']
                        message += f"\n📌 {current_major}:\n"
                    message += f"- Năm {row['year']}: {row['score']}\n"
                message += f"Bạn có thể tham khảo thêm thông tin điểm chuẩn các phương thức khác /statistics/previous-admission"
            else:
                message = "❌ Không tìm thấy ngành nào có phương thức tuyển sinh này."
        else:
            message = "❗ Vui lòng cung cấp tên ngành hoặc phương thức xét tuyển."

        dispatcher.utter_message(text=message)
        return []

class ActionMajorByMethod(Action):
    def name(self) -> str:
        return "action_major_by_method"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
            
        # Sử dụng hàm normalize_method từ mapping_utils
        method_keyword = normalize_method(tracker.get_slot("method"))

        if method_keyword:
            rows = self.db.get_major_by_method(method_keyword)
            if rows:
                message = f"📌 **Các ngành có xét tuyển bằng phương thức {rows[0]['method']}**:\n"
                for row in rows:
                    message += f"- {row['major']}\n"
                message += f"\n💡 Bạn có thể tham khảo thêm thông tin chi tiết về phương thức xét tuyển ở {rows[0]['methodUrl']}"
            else:
                message = "❌ Không tìm thấy ngành nào có phương thức tuyển sinh này."
        else:
            message = "❗ Vui lòng cung cấp tên phương thức xét tuyển."

        dispatcher.utter_message(text=message)
        return []
    
class ActionCombinationMajor(Action):
    def name(self) -> str:
        return "action_combination_major"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:

        # Lấy thông tin từ entity major trong message
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        
        # Chuẩn hóa tên ngành sử dụng hàm từ mapping_utils
        major_keyword = normalize_major(major_entity)
        
        if major_keyword:
            # Truy vấn dữ liệu tổ hợp môn từ Neo4j
            combinations = self.db.get_combination_subjects(major_keyword)
            
            if combinations and len(combinations) > 0:
                message = f"📚 **Tổ hợp môn xét tuyển của ngành {combinations[0]['major']}**:\n\n"
                for idx, combo in enumerate(combinations, 1):
                    message += f"{idx}. {combo['subject_combination']}\n"
                message += f"\n💡 *Bạn có thể tham khảo thêm thông tin của ngành này ở {combinations[0]['majorUrl']} .*"
            else:
                message = f"❗ Không tìm thấy thông tin về tổ hợp môn xét tuyển cho ngành **{major_keyword}**.\n\nVui lòng kiểm tra lại tên ngành hoặc liên hệ với nhà trường để biết thêm thông tin."
        else:
            message = "❓ Vui lòng cho biết tên ngành cụ thể bạn muốn tìm hiểu về tổ hợp môn xét tuyển.\n\nVí dụ: *\"Tổ hợp môn xét tuyển ngành Công nghệ thông tin là gì?\"*"

        dispatcher.utter_message(text=message)
        return []
    
class ActionAskMethodsForMajor(Action):
    def name(self) -> str:
        return "action_ask_methods_for_major"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:

        # Lấy dữ liệu từ tracker
        major_input = tracker.get_slot("major")
        
        # Chuẩn hóa dữ liệu sử dụng hàm từ mapping_utils
        major_keyword = normalize_major(major_input)
        
        print(f"Normalized major for methods: {major_keyword}")
        
        if major_keyword:
            # Truy vấn phương thức xét tuyển cho ngành
            results = self.db.get_method_by_major(major_keyword)
            
            if results:
                # Tạo thông báo với danh sách các phương thức xét tuyển
                major_name = results[0]["major"]
                methods = [result["method"] for result in results]
                
                message = f"📝 **Ngành {major_name} xét tuyển bằng các phương thức sau:**\n\n"
                
                for i, method in enumerate(methods, 1):
                    message += f"{i}. {method}\n"
                
                if len(methods) == 0:
                    message = f"❌ Không tìm thấy thông tin về phương thức xét tuyển cho ngành {major_input}."
                message += f"💡 Bạn có thể xem thêm thông tin của ngành {results[0]['majorUrl']}"
            else:
                message = f"❌ Không tìm thấy thông tin về phương thức xét tuyển cho ngành {major_input}."
        else:
            message = "❓ Vui lòng cung cấp tên ngành cụ thể để tôi có thể tìm kiếm thông tin về phương thức xét tuyển."
            
        dispatcher.utter_message(text=message)
        return []
    
class ActionAskIfMajorAcceptsMethod(Action):
    def name(self) -> str:
        return "action_ask_if_major_accepts_method"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:

        # Lấy dữ liệu từ tracker
        major_input = tracker.get_slot("major")
        method_input = tracker.get_slot("method")
        
        # Chuẩn hóa dữ liệu sử dụng các hàm từ mapping_utils
        major_keyword = normalize_major(major_input)
        method_keyword = normalize_method(method_input)
        
        print(f"Normalized major: {major_keyword}, Normalized method: {method_keyword}")
        
        if major_keyword and method_keyword:
            # Kiểm tra xem ngành có xét tuyển bằng phương thức này không
            result = self.db.check_major_has_method(major_keyword, method_keyword)
            
            if result["exists"]:
                message = f"✅ **Có, ngành {result['major_name']} có xét tuyển bằng phương thức {result['method_name']}.**"
                message += f"\n\n💡 Bạn có thể xem thêm thông tin chi tiết về ngành ở {result['majorUrl']}"
            else:
                if result["major_name"] and result["method_name"]:
                    message = f"❌ **Không, ngành {result['major_name']} không xét tuyển bằng phương thức {result['method_name']}.**"
                    message += f"\n\n💡 Bạn có thể xem thêm các phương thức xét tuyển về ngành ở {result['majorUrl']}"
                elif result["major_name"]:
                    message = f"❌ **Không tìm thấy phương thức xét tuyển \"{method_input}\" cho ngành {result['major_name']}.**"
                    message += f"\n\n💡 Bạn có thể xem thêm thông tin chi tiết về ngành ở {result['majorUrl']}"
                elif result["method_name"]:
                    message = f"❌ **Không tìm thấy ngành \"{major_input}\" có xét tuyển bằng phương thức {result['method_name']}.**"
                else:
                    message = f"❌ **Không tìm thấy thông tin về ngành \"{major_input}\" và phương thức \"{method_input}\".**"
        else:
            if not major_keyword and not method_keyword:
                message = "❓ Vui lòng cung cấp cả tên ngành và phương thức xét tuyển để tôi có thể kiểm tra."
            elif not major_keyword:
                message = f"❓ Vui lòng cung cấp tên ngành cụ thể để tôi kiểm tra có xét tuyển bằng phương thức \"{method_input}\" không."
            else:
                message = f"❓ Vui lòng cung cấp phương thức xét tuyển cụ thể để tôi kiểm tra ngành \"{major_input}\" có áp dụng không."
            
        dispatcher.utter_message(text=message)
        return []
    
class ActionGetMajorQuota(Action):
    def name(self) -> str:
        return "action_get_major_quota"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:

        # Lấy thông tin từ entity major trong message
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        
        # Chuẩn hóa tên ngành sử dụng hàm từ mapping_utils
        major_keyword = normalize_major(major_entity)
        
        logging.debug(f"Normalized major for quota: {major_keyword}")
        
        if major_keyword:
            # Lấy thông tin về chỉ tiêu và tên ngành từ Neo4j
            result = self.db.get_major_quota_and_name(major_keyword)
            
            if result["found"]:
                if result["quota"]:
                    message = f"📊 **Chỉ tiêu tuyển sinh ngành {result['name']}**: {result['quota']} sinh viên."
                    message += f"\n\n💡 *Lưu ý: Chỉ tiêu có thể thay đổi theo từng năm, bạn có thể tham khảo thêm chi tiết về ngành ở {result['majorUrl']}.*"
                else:
                    message = f"❗ Ngành {result['name']} hiện chưa có thông tin về chỉ tiêu tuyển sinh."
            else:
                message = f"❌ Không tìm thấy thông tin về ngành \"{major_entity}\"."
        else:
            message = "❓ Vui lòng cho biết tên ngành cụ thể bạn muốn biết về chỉ tiêu tuyển sinh.\n\nVí dụ: *\"Chỉ tiêu ngành Công nghệ thông tin là bao nhiêu?\"*"
            
        dispatcher.utter_message(text=message)
        return []
    
class ActionSuggestMajorByAchievement(Action):
    def name(self) -> str:
        return "action_major_by_achievement"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:

        # Lấy thông tin về thành tích/sở trường từ entity
        achievement = next(tracker.get_latest_entity_values("achievement"), None)
        
        logging.debug(f"Achievement input: {achievement}")
        
        if not achievement:
            message = "❓ Vui lòng cho biết thành tích, sở trường hoặc lĩnh vực bạn giỏi để tôi có thể gợi ý ngành phù hợp."
            dispatcher.utter_message(text=message)
            return []
        
        # Chuẩn hóa và phân loại thành tích/sở trường
        achievement_type = normalize_achievement_field(achievement)
        logging.debug(f"Normalized achievement: {achievement_type}")
        
        # Truy vấn các ngành phù hợp với thành tích/sở trường
        majors = self.db.get_major_by_achievement(achievement_type)
        
        if majors:
            message = f"🎯 **Dựa trên thành tích của bạn về {achievement_type}, những ngành sau bạn có thể xét tuyển:**\n\n"
            
            for i, major_info in enumerate(majors, 1):
                message += f"{i}. {major_info['major']}\n"
            
            message += "\n💡 *Bạn có thể tham khảo phương thức tuyển sinh bằng xét tuyển riêng ở /admission/xettuyenrieng và xét tuyển thẳng ở /admission/xettuyenthang *"
        else:
            message = f"❗ Thành tích '{achievement_type} không tìm thấy ngành phù hợp'.\n\nVui lòng chia sẻ thêm về thành tích khác để tôi tư vấn tốt hơn."
        
        dispatcher.utter_message(text=message)
        return []

class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Đếm số lần fallback liên tiếp
        fallback_count = 0
        for event in reversed(tracker.events):
            if event.get("name") == "action_default_fallback":
                fallback_count += 1
            elif event.get("name") not in ["action_listen", None]:
                break
        
        if fallback_count >= 2:
            # Nếu fallback nhiều lần liên tiếp -> đề nghị chuyển người hỗ trợ
            dispatcher.utter_message(
                text="Có vẻ như tôi không thể trả lời câu hỏi của bạn. "
                     "Bạn muốn được kết nối với cán bộ tư vấn tuyển sinh không?")
            
            # Đặt một slot để theo dõi yêu cầu handoff
            return [SlotSet("handoff_requested", True)]
        else:
            # Fallback thông thường với gợi ý
            dispatcher.utter_message(
                text="Xin lỗi, tôi không hiểu ý của bạn. Bạn có thể thử các câu hỏi như:\n"
                     "- Điểm chuẩn ngành Công nghệ thông tin năm 2024?\n"
                     "- Ngành CNTT đặc thù là gì?\n"
                     "- Tổ hợp môn xét tuyển ngành CNTT?\n"
                     "- Các phương thức xét tuyển năm nay là gì?")
            
            return []

# Thêm action handoff đã điều chỉnh
class ActionHandoffToHuman(Action):
    def name(self) -> str:
        return "action_handoff_to_human"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Thông báo hướng dẫn theo yêu cầu
        dispatcher.utter_message(
            text="Để kết nối với cán bộ tư vấn, vui lòng truy cập vào mục tư vấn tuyển sinh trên website.")
        
        # Reset slot handoff_requested
        return [SlotSet("handoff_requested", False)]

# Thêm action trích xuất thông tin từ ngữ cảnh
class ActionExtractFromContext(Action):
    def name(self) -> str:
        return "action_extract_from_context"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy message hiện tại của người dùng
        user_message = tracker.latest_message.get("text", "").lower()
        
        # Trích xuất ngữ cảnh hiện tại
        current_major = tracker.get_slot("current_context_major")
        current_method = tracker.get_slot("current_context_method")
        
        # Các từ khóa xác nhận/phủ định
        affirm_keywords = ["có", "đúng", "vâng", "ok", "được", "muốn", "tất nhiên", "chắc chắn"]
        deny_keywords = ["không", "đừng", "thôi", "khỏi", "chưa", "không cần"]
        
        # Kiểm tra nếu có xác nhận/phủ định trong tin nhắn
        is_affirm = any(keyword in user_message for keyword in affirm_keywords)
        is_deny = any(keyword in user_message for keyword in deny_keywords)
        
        # Nếu có xác nhận và đang có major trong ngữ cảnh
        if is_affirm and current_major:
            if "tổ hợp" in user_message or "môn" in user_message:
                # Chuyển hướng sang action trả lời về tổ hợp môn
                return [FollowupAction("action_combination_major")]
            
            elif "phương thức" in user_message or "xét tuyển" in user_message:
                # Chuyển sang trả lời về phương thức xét tuyển
                return [FollowupAction("action_ask_methods_for_major")]
        
        # Nếu phủ định hoặc không rõ ý người dùng
        if is_deny or not (is_affirm or is_deny):
            dispatcher.utter_message(
                text="Bạn cần tư vấn thêm thông tin gì về tuyển sinh?")
        
        return []

class ActionSuggestMajorBySubjects(Action):
    def name(self) -> str:
        return "action_suggest_major_by_subjects"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy tất cả các entity subject từ message hiện tại
        subjects = list(tracker.get_latest_entity_values("subject"))
        
        logging.debug(f"Raw subjects from entities: {subjects}")
        
        # Nếu không tìm thấy subject trong entities, thử tìm trong toàn bộ message
        if not subjects:
            user_message = tracker.latest_message.get("text", "")
            from actions.mapping_utils import find_subjects_in_text
            subjects = find_subjects_in_text(user_message)
            logging.debug(f"Subjects extracted from message: {subjects}")
        
        # Chuẩn hóa các môn học
        normalized_subjects = []
        for subject in subjects:
            normalized_subject = normalize_subject(subject)
            if normalized_subject and normalized_subject not in normalized_subjects:
                normalized_subjects.append(normalized_subject)
        
        logging.debug(f"Normalized subjects: {normalized_subjects}")
        
        if not normalized_subjects:
            message = "❓ Vui lòng cho biết các môn học bạn muốn xét tuyển để tôi có thể gợi ý ngành phù hợp.\n\n" \
                      "Ví dụ: \"*Tôi muốn xét tuyển bằng môn Toán, Lý, Hóa thì có thể đăng ký ngành nào?*\""
            dispatcher.utter_message(text=message)
            return []
        
        # Giới hạn số lượng môn học tối đa là 4
        if len(normalized_subjects) > 4:
            normalized_subjects = normalized_subjects[:4]
            logging.debug(f"Limited to max 4 subjects: {normalized_subjects}")
        
        # Truy vấn các ngành phù hợp với các môn học đã chuẩn hóa
        majors = self.db.get_majors_by_subjects(normalized_subjects)
        logging.debug(f"Got {len(majors)} results from Neo4j")
        
        if majors:
            # Danh sách các môn đã chọn
            subjects_str = ", ".join([f"**{subject}**" for subject in normalized_subjects])
            
            message = f"📚 **Các ngành phù hợp với môn {subjects_str}:**\n\n"
            
            # Xử lý kết quả trực tiếp từ Neo4j, không cần gom nhóm lại
            major_count = 0
            for i, record in enumerate(majors, 1):
                # Chuyển Neo4j record thành dict để dễ xử lý
                major_info = dict(record)
                
                # Lấy thông tin cơ bản
                major_name = major_info.get('major')
                major_id = major_info.get('major_id')
                
                if not major_name:
                    continue
                
                major_count += 1
                message += f"{major_count}. **{major_name}**\n"
                
                # Xử lý và hiển thị các tổ hợp môn
                subject_combinations = major_info.get('subject_combinations', [])
                
                if subject_combinations and len(subject_combinations) > 0:
                    message += "   *Tổ hợp môn*:\n"
                    for combo in subject_combinations:
                        message += f"   - {combo}\n"
                else:
                    message += "   *Tổ hợp môn*: Thông tin không có sẵn\n"
                
                message += "\n"
                
            
            # Thêm gợi ý
            message += "\n💡 Bạn có thể xem chi tiết về phương thức xét điểm thi tốt nghiệp trung học phổ thông /admission/totnghiep_thpt"
        else:
            subjects_str = ", ".join(normalized_subjects)
            message = f"❌ Không tìm thấy ngành nào phù hợp với môn **{subjects_str}**.\n\n" \
                      f"Có thể tổ hợp môn này không được sử dụng trong xét tuyển hoặc thông tin chưa được cập nhật trong hệ thống.\n\n" \
                      f"💡 Bạn có thể thử với các môn phổ biến như: **Toán, Lý, Hóa** hoặc **Toán, Văn, Anh**."
        
        dispatcher.utter_message(text=message)
        
        # Lưu lại bối cảnh để xử lý theo dõi
        if "current_subjects" in domain.get("slots", {}):
            return [SlotSet("current_subjects", normalized_subjects)]
        return []
    
class ActionGetMajorsByFaculty(Action):
    def name(self) -> str:
        return "action_get_majors_by_faculty"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy faculty từ entity hoặc slot
        faculty_entity = next(tracker.get_latest_entity_values("faculty"), None)
        faculty_slot = tracker.get_slot("faculty")
        
        # Ưu tiên entity trong message hiện tại, nếu không có thì dùng slot
        faculty = faculty_entity or faculty_slot
        
        logging.debug(f"Faculty input: {faculty}")
        
        if not faculty:
            message = "❓ Vui lòng cho biết tên khoa bạn muốn tìm hiểu về các ngành đào tạo.\n\n" \
                      "Ví dụ: \"*Khoa Công nghệ thông tin có những ngành nào?*\" hoặc \"*Các ngành thuộc khoa Điện?*\""
            dispatcher.utter_message(text=message)
            return []
        
        # Chuẩn hóa faculty để lấy ID
        faculty_id = normalize_faculty(faculty)
        faculty_id = int(faculty_id)
        logging.debug(f"Normalized faculty ID: {faculty_id}")
        
        if not faculty_id:
            message = f"❌ Tôi không tìm thấy thông tin về Khoa \"{faculty}\". Vui lòng kiểm tra lại tên khoa."
            dispatcher.utter_message(text=message)
            return []
            
        # Lấy danh sách ngành từ khoa
        majors = self.db.get_majors_by_faculty(faculty_id)
        
        if not majors or len(majors) == 0:
            message = f"❌ Không tìm thấy thông tin về các ngành thuộc Khoa này. Có thể dữ liệu chưa được cập nhật."
            dispatcher.utter_message(text=message)
            return []
            
        # Tạo message hiển thị danh sách ngành
        faculty_name = majors[0]["faculty"]
        message = f"🏫 **Các ngành đào tạo thuộc khoa {faculty_name}:**\n\n"
        
        for i, major in enumerate(majors, 1):
            message += f"{i}. **{major['major']}**\n"
            
        message += "\n💡 *Bạn có thể hỏi thêm về điểm chuẩn, tổ hợp môn hoặc thông tin chi tiết của từng ngành.*"
        
        dispatcher.utter_message(text=message)
        
        # Lưu thông tin vào slot để sử dụng sau này
        return []
    
class ActionSuggestMajorByScore(Action):
    def name(self) -> str:
        return "action_suggest_major_by_score"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy điểm số từ entity
        score_entity = next(tracker.get_latest_entity_values("score"), None)
        
        # Lấy phương thức từ entity và chuẩn hóa
        method_entity = next(tracker.get_latest_entity_values("method"), None)
        
        if not score_entity:
            dispatcher.utter_message(text="❓ Vui lòng cho biết số điểm bạn đạt được.")
            return []
        
        if not method_entity:
            dispatcher.utter_message(text="❓ Vui lòng cho biết phương thức xét tuyển bạn quan tâm.")
            return []
        
        try:
            # Chuyển đổi điểm sang số
            score = float(score_entity)
            
            # Chuẩn hóa phương thức
            method_id = normalize_method(method_entity)
            
            if not method_id:
                dispatcher.utter_message(text=f"❌ Tôi không nhận ra phương thức '{method_entity}'. "
                                            f"Vui lòng thử lại với các phương thức như: xét điểm thi tốt nghiệp, "
                                            f"xét học bạ, đánh giá năng lực, đánh giá tư duy hoặc xét tuyển riêng.")
                return []
            
            # Lấy kết quả gợi ý ngành
            results = self.db.get_majors_by_score_and_method(score, method_id)
            
            if not results:
                dispatcher.utter_message(text=f"❌ Không tìm thấy ngành nào phù hợp với điểm số {score} "
                                            f"theo phương thức {method_entity}.")
                return []
            
            # Lọc kết quả để chỉ giữ lại các ngành vẫn áp dụng phương thức này trong năm hiện tại
            results = self._filter_valid_majors(results, method_id)
            
            if not results:
                dispatcher.utter_message(text=f"❌ Tôi đã tìm thấy một số ngành phù hợp với điểm số của bạn, "
                                            f"nhưng không có ngành nào còn áp dụng phương thức {method_entity} "
                                            f"trong năm học hiện tại.")
                return []
            
            # Tạo phản hồi
            message = self._create_response_message(results, score, method_entity)
            
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("score", score_entity),
                SlotSet("method", method_entity)
            ]
            
        except ValueError:
            dispatcher.utter_message(text=f"❌ Điểm số '{score_entity}' không hợp lệ. Vui lòng nhập một số.")
            return []
    
    def _filter_valid_majors(self, grouped_results: list, method_id: str) -> list:
        """
        Lọc kết quả để chỉ giữ lại các ngành vẫn áp dụng phương thức này trong năm hiện tại
        """
        if not grouped_results:
            return []
        
        filtered_groups = []
        
        for group in grouped_results:
            valid_majors = []
            for major in group["majors"]:
                # Kiểm tra xem ngành có còn áp dụng phương thức này không
                check_result = self.db.check_major_has_method(major["major_id"], method_id)
                
                # Nếu phương thức vẫn được áp dụng, giữ lại ngành này
                if check_result["exists"]:
                    valid_majors.append(major)
                else:
                    logging.debug(f"Major {major['major_name']} ({major['major_id']}) no longer uses method {method_id}")
            
            # Chỉ thêm nhóm vào kết quả nếu có ngành hợp lệ
            if valid_majors:
                filtered_groups.append({
                    "group": group["group"],
                    "majors": valid_majors
                })
        
        return filtered_groups
    
    def _create_response_message(self, grouped_results: list, score: float, method: str) -> str:
        """
        Tạo thông điệp phản hồi từ kết quả đã nhóm
        """
        message = f"📊 **Các ngành phù hợp với điểm {score} theo phương thức {method}:**\n\n"
        
        # Thông tin về các nhóm
        group_info = {
            "high": "🔥 **Tỷ lệ đỗ cao**",
            "medium": "⚡ **Tỷ lệ đỗ trung bình**",
            "low": "⚠️ **Tỷ lệ đỗ thấp**"
        }
        
        for group in grouped_results:
            group_name = group["group"]
            majors = group["majors"]
            
            if majors:
                message += f"{group_info.get(group_name, 'Khác')}:\n\n"
                
                for i, major in enumerate(majors, 1):
                    message += f"{i}. **{major['major_name']}**\n"
                    message += f"   - Điểm chuẩn: {major['cutoff']} ({major['year']})\n"
                
                message += "\n"
        
        message += "💡 *Ghi chú: Các ngành được hiển thị đều áp dụng phương thức này trong năm học hiện tại. Kết quả dựa trên điểm chuẩn các năm trước.*\n\n"
        message += "Bạn có thể hỏi thêm về:\n"
        message += "- Tổ hợp môn xét tuyển của ngành\n"
        message += "- Điểm chuẩn của ngành theo các năm"
        
        
        return message
    
class ActionSuggestMajorByScoreWithMethodAndFaculty(Action):
    def name(self) -> str:
        return "action_suggest_major_by_score_with_method_and_faculty"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy các entity từ message
        score_entity = next(tracker.get_latest_entity_values("score"), None)
        method_entity = next(tracker.get_latest_entity_values("method"), None)
        faculty_entity = next(tracker.get_latest_entity_values("faculty"), None)
        
        # Kiểm tra các entity cần thiết
        missing_entities = []
        if not score_entity:
            missing_entities.append("điểm số")
        if not method_entity:
            missing_entities.append("phương thức xét tuyển")
        if not faculty_entity:
            missing_entities.append("khoa")
            
        if missing_entities:
            missing_str = ", ".join(missing_entities)
            message = f"❓ Vui lòng cung cấp {missing_str} để tôi có thể tư vấn ngành phù hợp."
            dispatcher.utter_message(text=message)
            return []
        
        try:
            # Chuyển đổi điểm sang số
            score = float(score_entity)
            
            # Chuẩn hóa phương thức và khoa
            method_id = normalize_method(method_entity)
            faculty_id = normalize_faculty(faculty_entity)
            faculty_id = int(faculty_id)
            
            if not method_id:
                dispatcher.utter_message(text=f"❌ Tôi không nhận ra phương thức '{method_entity}'. "
                                            f"Vui lòng thử lại với các phương thức như: xét điểm thi tốt nghiệp, "
                                            f"xét học bạ, đánh giá năng lực, đánh giá tư duy hoặc xét tuyển riêng.")
                return []
                
            if not faculty_id:
                dispatcher.utter_message(text=f"❌ Tôi không nhận ra khoa '{faculty_entity}'. "
                                            f"Vui lòng kiểm tra lại tên khoa.")
                return []
            
            # Lấy kết quả gợi ý ngành
            results = self.db.get_majors_by_score_method_and_faculty(score, method_id, faculty_id)
            
            if not results:
                dispatcher.utter_message(text=f"❌ Không tìm thấy ngành nào thuộc khoa này có điểm chuẩn "
                                            f"theo phương thức {method_entity}.")
                return []
            
            # Lọc kết quả để chỉ giữ lại các ngành vẫn áp dụng phương thức này trong năm hiện tại
            results = self._filter_valid_majors(results, method_id)
            
            if not results:
                dispatcher.utter_message(text=f"❌ Tôi đã tìm thấy một số ngành thuộc khoa này, "
                                            f"nhưng không có ngành nào còn áp dụng phương thức {method_entity} "
                                            f"trong năm học hiện tại.")
                return []
            
            # Tìm tên khoa để hiển thị
            faculty_name = None
            for group in results:
                for major in group["majors"]:
                    # Lấy tên khoa từ bất kỳ major nào
                    faculty_name_query = self.db.get_faculty_name_by_id(faculty_id)
                    if faculty_name_query:
                        faculty_name = faculty_name_query
                        break
                if faculty_name:
                    break
            
            if not faculty_name:
                faculty_name = faculty_entity
            
            # Tạo phản hồi
            message = self._create_response_message(results, score, method_entity, faculty_name)
            
            dispatcher.utter_message(text=message)
            
            return []
            
        except ValueError:
            dispatcher.utter_message(text=f"❌ Điểm số '{score_entity}' không hợp lệ. Vui lòng nhập một số.")
            return []
    
    def _filter_valid_majors(self, grouped_results: list, method_id: str) -> list:
        """
        Lọc kết quả để chỉ giữ lại các ngành vẫn áp dụng phương thức này trong năm hiện tại
        """
        if not grouped_results:
            return []
        
        filtered_groups = []
        
        for group in grouped_results:
            valid_majors = []
            for major in group["majors"]:
                # Kiểm tra xem ngành có còn áp dụng phương thức này không
                check_result = self.db.check_major_has_method(major["major_id"], method_id)
                
                # Nếu phương thức vẫn được áp dụng, giữ lại ngành này
                if check_result["exists"]:
                    valid_majors.append(major)
                else:
                    logging.debug(f"Major {major['major_name']} ({major['major_id']}) no longer uses method {method_id}")
            
            # Chỉ thêm nhóm vào kết quả nếu có ngành hợp lệ
            if valid_majors:
                filtered_groups.append({
                    "group": group["group"],
                    "majors": valid_majors
                })
        
        return filtered_groups
    
    def _create_response_message(self, grouped_results: list, score: float, method: str, faculty_name: str) -> str:
        """
        Tạo thông điệp phản hồi từ kết quả đã nhóm
        """
        message = f"📊 **Các ngành thuộc khoa {faculty_name} phù hợp với điểm {score} theo phương thức {method}:**\n\n"
        
        # Thông tin về các nhóm
        group_info = {
            "high": "🔥 **Khả năng đỗ cao**",
            "medium": "⚡ **Khả năng đỗ trung bình**",
            "low": "⚠️ **Khả năng đỗ thấp**"
        }
        
        group_desc = {
            "high": "*(Điểm của bạn >= điểm chuẩn)*",
            "medium": "*(Điểm của bạn < điểm chuẩn, chênh lệch ít)*",
            "low": "*(Điểm của bạn < điểm chuẩn, chênh lệch nhiều)*"
        }
        
        for group in grouped_results:
            group_name = group["group"]
            majors = group["majors"]
            
            if majors:
                message += f"{group_info.get(group_name, 'Khác')} {group_desc.get(group_name, '')}:\n\n"
                
                for i, major in enumerate(majors, 1):
                    message += f"{i}. **{major['major_name']}**\n"
                    message += f"   - Điểm chuẩn: {major['cutoff']} ({major['year']})\n"
                
                message += "\n"
        
        message += "💡 *Ghi chú: Các ngành được hiển thị đều áp dụng phương thức này trong năm học hiện tại. Kết quả dựa trên điểm chuẩn các năm trước.*\n\n"
        message += "Bạn có thể hỏi thêm về:\n"
        message += "- Tổ hợp môn xét tuyển của ngành\n"
        message += "- Cơ hội việc làm của các ngành này"
        
        return message
    
class ActionGetAdmissionProcessByMethod(Action):
    def name(self) -> str:
        return "action_get_admission_process_by_method"

    def __init__(self):
        self.admission_processes = {
            "xtt": self._get_xet_tuyen_thang_process(),
            "xtr": self._get_xet_tuyen_rieng_process(),
            "tn_thpt": self._get_tot_nghiep_thpt_process(),
            "hb_thpt": self._get_hoc_ba_process(),
            "dgnl": self._get_danh_gia_nang_luc_process(),
            "dgtd": self._get_danh_gia_tu_duy_process()
        }
        
        self.method_urls = {
            "xtt": "/admission/xettuyenthang",
            "xtr": "/admission/xettuyenrieng",
            "tn_thpt": "/admission/totnghiep_thpt",
            "hb_thpt": "/admission/hocba_thpt",
            "dgnl": "/admission/danhgianangluc",
            "dgtd": "/admission/danhgiatuduy"
        }

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
            
        # Lấy phương thức xét tuyển từ entity hoặc slot
        method_entity = next(tracker.get_latest_entity_values("method"), None)
        method_slot = tracker.get_slot("method")
        
        # Ưu tiên entity trong message hiện tại, nếu không có thì dùng slot
        method = method_entity or method_slot
        
        if not method:
            dispatcher.utter_message(text="❓ Vui lòng cho biết phương thức xét tuyển bạn muốn tìm hiểu quy trình đăng ký.")
            return []
        
        # Chuẩn hóa method để lấy ID
        method_id = normalize_method(method)
        
        if not method_id or method_id not in self.admission_processes:
            message = (f"❌ Tôi không tìm thấy thông tin về quy trình đăng ký cho phương thức \"{method}\". "
                      f"Vui lòng thử lại với các phương thức như: xét tuyển thẳng, xét tuyển riêng, "
                      f"xét điểm thi tốt nghiệp, xét học bạ, đánh giá năng lực hoặc đánh giá tư duy.")
            dispatcher.utter_message(text=message)
            return []
        
        # Lấy quy trình đăng ký cho phương thức tương ứng
        process_message = self.admission_processes[method_id]
        
        # Lấy URL tương ứng cho phương thức
        method_url = self.method_urls.get(method_id, "")
        
        # Thêm thông tin chi tiết về đường dẫn sau phần document
        additional_info = f"\n\nChi tiết các ngành xét tuyển bằng phương thức này tại {method_url}"
        
        # Gửi cả tin nhắn và thêm thông tin đường dẫn
        dispatcher.utter_message(text=process_message + additional_info)
        
        # Lưu slot để sử dụng sau này
        return []
    
    def _get_xet_tuyen_thang_process(self) -> str:
        intro = "Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét tuyển thẳng:"
        
        document_content = """
# Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét tuyển thẳng:

## Quy trình đăng ký và nộp hồ sơ:

1. **Đăng ký trực tuyến**: Thí sinh đăng ký trực tuyến tại đường dẫn https://tuyensinh.dut.udn.vn/

2. **Số lượng nguyện vọng**: 
   - Mỗi thí sinh chỉ được đăng ký duy nhất 01 hồ sơ xét tuyển thẳng
   - Trong mỗi hồ sơ, thí sinh có thể đăng ký tối đa 03 nguyện vọng vào 03 ngành học khác nhau

3. **Thứ tự xét tuyển**: 
   - Các nguyện vọng sẽ được xét theo thứ tự ưu tiên từ trên xuống dưới
   - Nếu trúng tuyển nguyện vọng đầu tiên, các nguyện vọng còn lại sẽ không được xét

4. **Hồ sơ và minh chứng**:
   - Cung cấp đầy đủ thông tin theo yêu cầu của trường
   - Đặc biệt quan trọng: Thông tin minh chứng cho đối tượng xét tuyển thẳng phải đầy đủ và xác thực
   - Hồ sơ thiếu thông tin hoặc thông tin không xác thực có thể dẫn đến việc không được xét tuyển

💡 Lưu ý: Hãy kiểm tra kỹ các giấy tờ minh chứng trước khi nộp để đảm bảo quyền lợi xét tuyển của bạn.
"""
        
        return intro + "\n\n<document>\n" + document_content + "\n<document>"

    def _get_xet_tuyen_rieng_process(self) -> str:
        intro = "Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét tuyển riêng:"
        
        document_content = """
# Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét tuyển riêng:

## Quy trình đăng ký và nộp hồ sơ:

1. **Nộp minh chứng thành tích**: 
   - Thí sinh nộp minh chứng thành tích (giải thưởng học thuật, chứng chỉ đặc biệt, v.v.) trực tuyến tại https://tuyensinh.dut.udn.vn/
   - Việc cung cấp thông tin minh chứng thành tích khi nộp hồ sơ là bắt buộc

2. **Đăng ký nguyện vọng chính thức**: 
   - Đăng ký nguyện vọng vào các ngành học của trường vào thời điểm xét tuyển chung theo quy định của Bộ Giáo dục và Đào tạo

3. **Số lượng nguyện vọng**: 
   - Thí sinh được đăng ký không giới hạn số lượng nguyện vọng vào tất cả các ngành học của Trường

4. **Điểm ưu tiên và minh chứng**:
   - Để được hưởng điểm ưu tiên, thí sinh cần cung cấp đầy đủ giấy tờ minh chứng liên quan

5. **Thứ tự xét tuyển**:
   - Các nguyện vọng được xét theo thứ tự ưu tiên từ trên xuống dưới 
   - Nếu trúng tuyển ở một nguyện vọng, các nguyện vọng còn lại sẽ không được xét

💡 Lưu ý: Chất lượng minh chứng thành tích sẽ ảnh hưởng trực tiếp đến kết quả xét tuyển. Hãy đảm bảo cung cấp đầy đủ và chính xác các giấy tờ liên quan.
"""
        
        return intro + "\n\n<document>\n" + document_content + "\n<document>"

    def _get_tot_nghiep_thpt_process(self) -> str:
        intro = "Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét điểm thi tốt nghiệp THPT:"
        
        document_content = """
# Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét điểm thi tốt nghiệp THPT:

## Quy trình đăng ký và nộp hồ sơ:

1. **Đăng ký nguyện vọng**: 
   - Thí sinh đăng ký nguyện vọng xét tuyển vào Trường Đại học Bách khoa - ĐHĐN trên hệ thống xét tuyển chung của Bộ Giáo dục và Đào tạo vào thời điểm quy định

2. **Số lượng nguyện vọng**: 
   - Thí sinh được đăng ký không giới hạn số lượng nguyện vọng vào các ngành học của trường

3. **Điểm ưu tiên**: 
   - Thí sinh cần cung cấp đầy đủ giấy tờ minh chứng để được hưởng điểm ưu tiên (nếu có)

4. **Thứ tự xét tuyển**: 
   - Các nguyện vọng được xét theo thứ tự ưu tiên từ cao xuống thấp
   - Nếu đã trúng tuyển vào một nguyện vọng, các nguyện vọng tiếp theo sẽ không được xét

💡 Lưu ý: Thời gian đăng ký xét tuyển theo phương thức này sẽ theo lịch chung của Bộ Giáo dục và Đào tạo. Hãy cập nhật thông tin thường xuyên trên trang web của Bộ và của Trường.
"""
        
        return intro + "\n\n<document>\n" + document_content + "\n<document>"

    def _get_hoc_ba_process(self) -> str:
        intro = "Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét kết quả học tập THPT (Học bạ):"
        
        document_content = """
# Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét kết quả học tập THPT (Học bạ):

## Quy trình đăng ký và nộp hồ sơ:

1. **Đăng ký nguyện vọng**: 
   - Thí sinh đăng ký nguyện vọng xét tuyển bằng kết quả học tập THPT trên hệ thống xét tuyển chung của Bộ Giáo dục và Đào tạo vào thời điểm quy định

2. **Số lượng nguyện vọng**: 
   - Thí sinh được đăng ký không giới hạn số lượng nguyện vọng vào các ngành học của Trường

3. **Điểm ưu tiên**: 
   - Thí sinh cần cung cấp đầy đủ giấy tờ minh chứng để được hưởng điểm ưu tiên (nếu có)

4. **Thứ tự xét tuyển**: 
   - Các nguyện vọng được xét theo thứ tự ưu tiên từ cao xuống thấp
   - Nếu đã trúng tuyển vào một nguyện vọng, các nguyện vọng tiếp theo sẽ không được xét

💡 Lưu ý: Đảm bảo học bạ của bạn được xác nhận đầy đủ và chính xác. Việc tính điểm học bạ sẽ dựa trên quy định cụ thể của trường, hãy tham khảo thêm trên trang web tuyển sinh của Trường.
"""
        
        return intro + "\n\n<document>\n" + document_content + "\n<document>"

    def _get_danh_gia_nang_luc_process(self) -> str:
        intro = "Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét kết quả thi đánh giá năng lực:"
        
        document_content = """
# Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét kết quả thi đánh giá năng lực:

## Quy trình đăng ký và nộp hồ sơ:

1. **Đăng ký nguyện vọng**: 
   - Thí sinh sử dụng kết quả kỳ thi đánh giá năng lực của Đại học Quốc gia TP.HCM để đăng ký xét tuyển
   - Đăng ký trên hệ thống xét tuyển chung của Bộ Giáo dục và Đào tạo vào thời điểm quy định

2. **Số lượng nguyện vọng**: 
   - Thí sinh được đăng ký không giới hạn số lượng nguyện vọng vào các ngành học của trường

3. **Điểm ưu tiên**: 
   - Thí sinh cần cung cấp đầy đủ giấy tờ minh chứng để được hưởng điểm ưu tiên (nếu có)

4. **Thứ tự xét tuyển**: 
   - Các nguyện vọng được xét theo thứ tự ưu tiên từ cao xuống thấp
   - Nếu đã trúng tuyển vào một nguyện vọng, các nguyện vọng tiếp theo sẽ không được xét

💡 Lưu ý: Đảm bảo bạn đã tham gia kỳ thi đánh giá năng lực do Đại học Quốc gia TP.HCM tổ chức và có kết quả hợp lệ trong năm xét tuyển. Điểm đánh giá năng lực có thời hạn sử dụng theo quy định của đơn vị tổ chức thi.
"""
        
        return intro + "\n\n<document>\n" + document_content + "\n<document>"

    def _get_danh_gia_tu_duy_process(self) -> str:
        intro = "Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét kết quả thi đánh giá tư duy:"
        
        document_content = """
# Cách thức đăng kí xét tuyển vào Trường Đại Học Bách Khoa năm 2025 theo phương thức Xét kết quả thi đánh giá tư duy:

## Quy trình đăng ký và nộp hồ sơ:

1. **Đăng ký nguyện vọng**: 
   - Thí sinh sử dụng kết quả kỳ thi đánh giá tư duy của Đại học Bách khoa Hà Nội để đăng ký xét tuyển
   - Đăng ký trên hệ thống xét tuyển chung của Bộ Giáo dục và Đào tạo vào thời điểm quy định

2. **Số lượng nguyện vọng**: 
   - Thí sinh được đăng ký không giới hạn số lượng nguyện vọng vào các ngành học của trường

3. **Điểm ưu tiên**: 
   - Thí sinh cần cung cấp đầy đủ giấy tờ minh chứng để được hưởng điểm ưu tiên (nếu có)

4. **Thứ tự xét tuyển**: 
   - Các nguyện vọng được xét theo thứ tự ưu tiên từ cao xuống thấp
   - Nếu đã trúng tuyển vào một nguyện vọng, các nguyện vọng tiếp theo sẽ không được xét

💡 Lưu ý: Đảm bảo bạn đã tham gia kỳ thi đánh giá tư duy do Đại học Bách khoa Hà Nội tổ chức và có kết quả hợp lệ trong năm xét tuyển. Điểm đánh giá tư duy có thời hạn sử dụng theo quy định của đơn vị tổ chức thi.
"""
        
        return intro + "\n\n<document>\n" + document_content + "\n<document>"