from typing import List, Dict, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.graph_connector import GraphConnector
from actions.mapping_utils import normalize_major, normalize_method, normalize_achievement_field, normalize_subject  # Import các hàm tiện ích
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
                message += "\n💡 *Bạn có thể tham khảo điểm chuẩn của ngành này theo từng năm và phương thức xét tuyển.*"
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
            else:
                if result["major_name"] and result["method_name"]:
                    message = f"❌ **Không, ngành {result['major_name']} không xét tuyển bằng phương thức {result['method_name']}.**"
                elif result["major_name"]:
                    message = f"❌ **Không tìm thấy phương thức xét tuyển \"{method_input}\" cho ngành {result['major_name']}.**"
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
                    message += "\n\n💡 *Lưu ý: Chỉ tiêu có thể thay đổi theo từng năm, đây là thông tin mới nhất mà tôi có.*"
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
            
            message += "\n💡 *Bạn có thể tìm hiểu thêm về điểm chuẩn, tổ hợp môn và phương thức xét tuyển của các ngành này.*"
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
            message += "\n💡 *Bạn có thể hỏi thêm về điểm chuẩn hoặc thông tin chi tiết của từng ngành.*"
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