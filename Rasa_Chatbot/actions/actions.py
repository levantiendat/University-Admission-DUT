from typing import List, Dict, Optional, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.graph_connector import GraphConnector
from actions.mapping_utils import normalize_major, normalize_method, normalize_achievement_field, normalize_subject, normalize_faculty  # Import các hàm tiện ích
from actions.mapping_utils import normalize_student_interests, normalize_personality_strengths, normalize_achievement_field, normalize_subjects_strengths, comprehensive_major_suggestion, MAJOR_MAPPING
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

class ActionDetailMethod(Action):
    def name(self) -> str:
        return "action_detail_method"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy thông tin từ entity method trong message
        method_entity = next(tracker.get_latest_entity_values("method"), None)
        
        # Chuẩn hóa tên phương thức sử dụng hàm từ mapping_utils
        method_keyword = normalize_method(method_entity)
        
        if method_keyword:
            # Truy vấn dữ liệu tổ hợp môn từ Neo4j
            detail = self.db.get_detail_method(method_keyword)
            detail = detail[0] if detail else None
            if detail:
                message = f"📚 Thông tin chi tiết phương thức {detail['method']}**:\n\n"
                message += f"{detail['description']}\n"
                message += f"\n💡 *Bạn có thể tham khảo thêm thông tin chi tiết về phương thức ở {detail['methodUrl']}.*"
            else:
                message = f"❗ Không tìm thấy thông tin chi tiết về phương thức **{method_keyword}**.\n\nVui lòng kiểm tra lại tên phương thức hoặc liên hệ với nhà trường để biết thêm thông tin."
        else:
            message = "❓ Vui lòng cho biết tên phương thức cụ thể bạn muốn tìm hiểu về thông tin chi tiết.\n\nVí dụ: *\"Thông tin chi tiết phương thức xét tuyển học bạ là gì?\"*"
            
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
                major_url = major_info.get('majorUrl')
                
                
                if not major_name:
                    continue
                
                major_count += 1
                message += f"{major_count}. {major_name}\n"
                
                # Xử lý và hiển thị các tổ hợp môn
                subject_combinations = major_info.get('subject_combinations', [])
                
                if subject_combinations and len(subject_combinations) > 0:
                    message += "   *Tổ hợp môn*:\n"
                    for combo in subject_combinations:
                        message += f"   - {combo}\n"
                else:
                    message += "   *Tổ hợp môn*: Thông tin không có sẵn\n"
                
                message += f"Xem chi tiết ngành này {major_url}\n"
                
            
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
            message += f"{i}. {major['major']}. Xem chi tiết ngành {major['majorUrl']}\n"
            
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
        
        group_desc = {
            "high": "*(Điểm chuẩn gần với điểm của bạn, chênh lệch rất ít)*",
            "medium": "*(Điểm chuẩn cách điểm của bạn một khoảng vừa phải)*", 
            "low": "*(Điểm chuẩn cách điểm của bạn khá xa)*"
        }
        
        for group in grouped_results:
            group_name = group["group"]
            majors = group["majors"]
            
            if majors:
                message += f"{group_info.get(group_name, 'Khác')} {group_desc.get(group_name, '')}:\n\n"
                
                for i, major in enumerate(majors, 1):
                    message += f"{i}. {major['major_name']}. Xem chi tiết ngành {major['major_url']}\n"
                
                message += "\n"
        
        message += "💡 *Kết quả dựa trên điểm chuẩn quy đổi từ năm 2023 và 2024 với tỷ lệ 1:4. Các ngành được hiển thị đều áp dụng phương thức này trong năm học hiện tại.*\n\n"
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
            "high": "*(Điểm chuẩn gần với điểm của bạn, chênh lệch rất ít)*",
            "medium": "*(Điểm chuẩn cách điểm của bạn một khoảng vừa phải)*", 
            "low": "*(Điểm chuẩn cách điểm của bạn khá xa)*"
        }
        
        for group in grouped_results:
            group_name = group["group"]
            majors = group["majors"]
            
            if majors:
                message += f"{group_info.get(group_name, 'Khác')} {group_desc.get(group_name, '')}:\n\n"
                
                for i, major in enumerate(majors, 1):
                    message += f"{i}. {major['major_name']}. Xem chi tiết ngành {major['major_url']}\n"
                
                message += "\n"
        
        message += "💡 *Kết quả dựa trên điểm chuẩn quy đổi từ năm 2023 và 2024 với tỷ lệ 1:4. Các ngành được hiển thị đều áp dụng phương thức này trong năm học hiện tại.*\n\n"
        message += "Bạn có thể hỏi thêm về:\n"
        message += "- Tổ hợp môn xét tuyển của ngành\n"
        message += "- Cơ hội việc làm của các ngành này"
        
        return message

class ActionSuggestMajorByScoreAndSubjects(Action):
    def name(self) -> str:
        return "action_suggest_major_by_score_and_subjects"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy điểm số từ entity
        score_entity = next(tracker.get_latest_entity_values("score"), None)
        
        # Lấy phương thức từ entity
        method_entity = next(tracker.get_latest_entity_values("method"), None)
        
        # Lấy các môn học từ entity
        subjects = list(tracker.get_latest_entity_values("subject"))
        
        # Kiểm tra các thông tin cần thiết
        missing_info = []
        if not score_entity:
            missing_info.append("điểm số")
        if not method_entity:
            missing_info.append("phương thức xét tuyển")
        if not subjects or len(subjects) == 0:
            missing_info.append("các môn học/khối thi")
            
        if missing_info:
            missing_str = ", ".join(missing_info)
            message = f"❓ Vui lòng cung cấp {missing_str} để tôi có thể tư vấn ngành phù hợp."
            dispatcher.utter_message(text=message)
            return []
        
        # Chuẩn hóa các môn học
        normalized_subjects = []
        for subject in subjects:
            normalized_subject = normalize_subject(subject)
            if normalized_subject and normalized_subject not in normalized_subjects:
                normalized_subjects.append(normalized_subject)
        
        logging.debug(f"Normalized subjects: {normalized_subjects}")
        
        if not normalized_subjects:
            message = "❓ Vui lòng cung cấp tên các môn học hợp lệ để tôi có thể tư vấn ngành phù hợp."
            dispatcher.utter_message(text=message)
            return []
        
        # Giới hạn số lượng môn tối đa là 3 (khối thi thường gồm 3 môn)
        if len(normalized_subjects) > 3:
            normalized_subjects = normalized_subjects[:3]
            logging.debug(f"Limited to 3 subjects for combination: {normalized_subjects}")
        
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
            results = self.db.get_majors_by_score_method_and_subjects(score, method_id, normalized_subjects)
            
            if not results:
                subjects_str = ", ".join(normalized_subjects)
                dispatcher.utter_message(text=f"❌ Không tìm thấy ngành nào phù hợp với điểm {score} "
                                            f"theo phương thức {method_entity} "
                                            f"và tổ hợp môn {subjects_str}.")
                return []
            
            # Lọc kết quả để chỉ giữ lại các ngành vẫn áp dụng phương thức này trong năm hiện tại
            results = self._filter_valid_majors(results, method_id)
            
            if not results:
                subjects_str = ", ".join(normalized_subjects)
                dispatcher.utter_message(text=f"❌ Tôi đã tìm thấy một số ngành phù hợp với điểm {score} "
                                            f"và tổ hợp môn {subjects_str}, "
                                            f"nhưng không có ngành nào còn áp dụng phương thức {method_entity} "
                                            f"trong năm học hiện tại.")
                return []
            
            # Tạo phản hồi
            subjects_str = ", ".join(normalized_subjects)
            message = self._create_response_message(results, score, method_entity, subjects_str)
            
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("score", score_entity),
                SlotSet("method", method_entity),
                SlotSet("current_subjects", normalized_subjects)
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
    
    def _create_response_message(self, grouped_results: list, score: float, method: str, subjects_str: str) -> str:
        """
        Tạo thông điệp phản hồi từ kết quả đã nhóm
        """
        message = f"📊 Các ngành phù hợp với điểm {score} theo phương thức {method} và tổ hợp môn {subjects_str}:\n\n"
        
        # Thông tin về các nhóm
        group_info = {
            "high": "🔥 Tỷ lệ đỗ cao",
            "medium": "⚡ Tỷ lệ đỗ trung bình",
            "low": "⚠️ Tỷ lệ đỗ thấp"
        }
        
        group_desc = {
            "high": "(Điểm chuẩn gần với điểm của bạn, chênh lệch rất ít)",
            "medium": "(Điểm chuẩn cách điểm của bạn một khoảng vừa phải)", 
            "low": "(Điểm chuẩn cách điểm của bạn khá xa)"
        }
        
        for group in grouped_results:
            group_name = group["group"]
            majors = group["majors"]
            
            if majors:
                message += f"{group_info.get(group_name, 'Khác')} {group_desc.get(group_name, '')}:\n\n"
                
                for i, major in enumerate(majors, 1):
                    message += f"{i}. {major['major_name']}. Xem chi tiết ngành {major['major_url']}\n"
                
                message += "\n"
        
        message += "💡 *Kết quả dựa trên điểm chuẩn quy đổi từ năm 2023 và 2024 với tỷ lệ 1:4 và tổ hợp môn phù hợp. Các ngành được hiển thị đều áp dụng phương thức này trong năm học hiện tại.*\n\n"
        message += "Bạn có thể hỏi thêm về:\n"
        message += "- Thông tin chi tiết về từng ngành\n"
        message += "- Cơ hội việc làm của các ngành này\n"
        message += "- Điểm chuẩn theo các năm"
        
        return message

class ActionGetAdmissionProcessByMethod(Action):
    def name(self) -> str:
        return "action_get_admission_process_by_method"

    def __init__(self):
        self.db = GraphConnector()

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
        
        if not method_id:
            message = (f"❌ Tôi không tìm thấy thông tin về quy trình đăng ký cho phương thức \"{method}\". "
                      f"Vui lòng thử lại với các phương thức như: xét tuyển thẳng, xét tuyển riêng, "
                      f"xét điểm thi tốt nghiệp, xét học bạ, đánh giá năng lực hoặc đánh giá tư duy.")
            dispatcher.utter_message(text=message)
            return []
        
        # Lấy quy trình đăng ký cho phương thức tương ứng
        method_details = self.db.get_detail_method(method_id)
        method_detail = method_details[0] if method_details else None
        if not method_details:
            dispatcher.utter_message(text=f"❌ Không tìm thấy thông tin chi tiết cho phương thức \"{method}\".")
            return []
        else:
            message = f"🏫 **Quy trình đăng ký xét tuyển theo phương thức {method_detail['method']}:**\n\n"
            message += "<document>\n"
            message += method_detail["application_process"]
            message += "\n<document>"
            message += f"\n\n💡 *Lưu ý: Thí sinh tham khảo thông tin chi tiết phương thức tại {method_detail['methodUrl']}"
            dispatcher.utter_message(text=message)
        # Lưu slot để sử dụng sau này
        return []
    
class ActionCalculateScore(Action):
    def name(self) -> str:
        return "action_calculate_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy tất cả các entity subject và score từ message
        subject_entities = list(tracker.get_latest_entity_values("subject"))
        score_entities = list(tracker.get_latest_entity_values("score"))
        
        logging.debug(f"Subject entities: {subject_entities}")
        logging.debug(f"Score entities: {score_entities}")
        
        # Kiểm tra nếu không đủ thông tin
        if not subject_entities or not score_entities:
            dispatcher.utter_message(text="❓ Tôi cần thông tin rõ ràng về môn học và điểm tương ứng để tính toán. "
                                         "Vui lòng cung cấp điểm cho từng môn học cụ thể.")
            return []
        
        # Tạo dictionary môn học và điểm
        subjects_scores = {}
        
        # Chuẩn hóa tên môn và điểm
        for i, subject in enumerate(subject_entities):
            if i >= len(score_entities):
                break
                
            # Chuẩn hóa tên môn học
            normalized_subject = normalize_subject(subject.lower())
            if not normalized_subject:
                continue
                
            # Chuyển điểm số thành float
            try:
                score = float(score_entities[i])
                # Đảm bảo điểm nằm trong khoảng hợp lệ
                if 0 <= score <= 10:
                    # Làm tròn đến 2 chữ số thập phân
                    subjects_scores[normalized_subject] = round(score, 2)
            except ValueError:
                continue
        
        # Nếu không có dữ liệu hợp lệ
        if not subjects_scores:
            dispatcher.utter_message(text="❌ Không thể tính toán điểm với dữ liệu đã cung cấp. "
                                         "Vui lòng đảm bảo điểm số hợp lệ (từ 0 đến 10).")
            return []
            
        if len(subjects_scores) > 8:
            # Chỉ lấy 6 môn đầu tiên
            limited_subjects = dict(list(subjects_scores.items())[:8])
            subjects_scores = limited_subjects
        
        # Tạo URL để chia sẻ
        share_url = self.create_share_url(subjects_scores)
        
        # Tạo câu trả lời
        message = self.create_response_message(subjects_scores, share_url)
        
        dispatcher.utter_message(text=message)
        
        return []
    
    def create_share_url(self, subjects_scores: dict) -> str:
        """Tạo URL chia sẻ để người dùng có thể truy cập tool tính điểm"""
        params = []
        for subject, score in subjects_scores.items():
            params.append(f"{subject}={score}")
        
        return f"/calculatescore/thpt?{'&'.join(params)}"
    
    def create_response_message(self, subjects_scores: dict, share_url: str) -> str:
        """Tạo thông báo phản hồi với kết quả tính toán"""
        # Hiển thị thông tin môn học đã nhập
        message = "📚 **Thông tin điểm các môn:**\n\n"
        for subject, score in subjects_scores.items():
            message += f"- {subject.capitalize()}: {score}\n"
        
        # Thêm URL cho công cụ tính toán chi tiết
        message += f"\n💡 Điểm của các khối xét tuyển từ điểm của bạn có thể truy cập '{share_url}'"
        
        return message
    
class ActionSuggestMajorsByStrengths(Action):
    def name(self) -> Text:
        return "action_suggest_majors_by_strengths"
        
    def __init__(self):
        self.db = GraphConnector()
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lấy thông tin về sở thích từ slot
        interests_text = tracker.get_slot("student_interests")
        academic_strengths_text = tracker.get_slot("academic_strengths") 
        personality_text = tracker.get_slot("personality_traits")
        
        # Nếu không có thông tin, yêu cầu người dùng nhập
        if not interests_text and not academic_strengths_text and not personality_text:
            message = (
                "Để gợi ý ngành học phù hợp, hãy cho tôi biết về sở thích, "
                "điểm mạnh học tập hoặc tính cách của bạn. Ví dụ:\n\n"
                "• \"*Em thích lập trình, công nghệ và giải quyết vấn đề*\"\n" 
                "• \"*Em giỏi toán, lý và thích làm việc với máy tính*\"\n"
                "• \"*Em là người tỉ mỉ, kiên nhẫn và thích khám phá cái mới*\""
            )
            dispatcher.utter_message(text=message)
            return []
        
        # Phân tích và chuẩn hóa dữ liệu đầu vào
        interests = []
        if interests_text:
            interests = normalize_student_interests(interests_text)
            
        academic_strengths = []
        if academic_strengths_text:
            academic_strengths = normalize_subjects_strengths(academic_strengths_text)
            
        personality_traits = []
        if personality_text:
            personality_traits = normalize_personality_strengths(personality_text)
        
        # Ghi log cho việc debug
        logging.debug(f"Sở thích: {interests}")
        logging.debug(f"Điểm mạnh học tập: {academic_strengths}")
        logging.debug(f"Tính cách: {personality_traits}")
        
        # Nếu không tìm thấy bất kỳ thông tin gợi ý nào
        if not interests and not academic_strengths and not personality_traits:
            message = (
                "Tôi chưa thể xác định rõ sở thích và điểm mạnh của bạn. Hãy chia sẻ cụ thể hơn về:\n\n"
                "• Các môn học bạn thích và giỏi (như toán, lý, hóa, sinh...)\n"
                "• Sở thích (như lập trình, máy tính, xây dựng, thiết kế...)\n"
                "• Tính cách và kỹ năng (như thích giải quyết vấn đề, làm việc nhóm, tỉ mỉ...)"
            )
            dispatcher.utter_message(text=message)
            return []
        
        # Tạo gợi ý tổng hợp
        suggestions = comprehensive_major_suggestion(
            interests, 
            academic_strengths, 
            personality_traits
        )
        
        if not suggestions:
            message = (
                "Tôi chưa tìm thấy ngành học phù hợp với thông tin bạn cung cấp. "
                "Hãy cung cấp thêm thông tin về sở thích và điểm mạnh của bạn."
            )
            dispatcher.utter_message(text=message)
            return []
        
        # Lấy thêm thông tin chi tiết về mỗi ngành học từ Neo4j
        major_details = {}
        for major_id in suggestions.keys():
            # Lấy thông tin chi tiết từ Neo4j
            details = self.db.get_major_quota_and_name(major_id)
            if details and details["found"]:
                major_details[major_id] = details
        
        # Tạo phản hồi
        message = "📚 **Dựa vào thông tin của bạn, các ngành học phù hợp nhất là:**\n\n"
        
        suggested_major_ids = []  # Danh sách lưu ID của các ngành được gợi ý
        
        for i, (major_id, details) in enumerate(suggestions.items(), 1):
            # Thông tin từ gợi ý
            score = details['score']
            
            # Lấy thông tin chi tiết từ Neo4j nếu có
            if major_id in major_details:
                neo4j_details = major_details[major_id]
                major_name = neo4j_details["name"]
                quota = neo4j_details.get("quota", "Chưa cập nhật")
                major_url = neo4j_details.get("majorUrl", "")
                
                # Thêm vào danh sách ngành gợi ý
                suggested_major_ids.append(major_id)
                
                # Tạo thông tin hiển thị
                message += f"{i}. **{major_name}** (Độ phù hợp: {score*100:.0f}%)\n"
                if quota:
                    message += f"   - Chỉ tiêu: {quota}\n"
                
                # Thêm giải thích
                for explanation in details['explanation']:
                    message += f"   - {explanation}\n"
                
                # Thêm link chi tiết ngành học
                if major_url:
                    message += f"   - [Xem chi tiết về ngành học]( {major_url} )\n"
            else:
                # Nếu không tìm thấy thông tin chi tiết, hiển thị tên ngành từ ID
                # Viết hoa chữ cái đầu của mỗi từ trong tên ngành
                major_name = ' '.join(word.capitalize() for word in major_id.split('_'))
                message += f"{i}. **{major_name}** (Độ phù hợp: {score*100:.0f}%)\n"
                
                # Thêm giải thích
                for explanation in details['explanation']:
                    message += f"   - {explanation}\n"
            
            message += "\n"
        
        # Thêm gợi ý tiếp theo
        message += (
            "💡 Bạn có thể tìm hiểu thêm về các ngành này bằng cách hỏi tôi như:\n"
            "• \"Cho em thông tin về ngành Công Nghệ Thông Tin\"\n"
            "• \"Tổ hợp môn nào xét tuyển vào Kỹ thuật Điện tử?\"\n"
            "• \"Ngành Kỹ thuật Xây dựng học những gì?\""
        )
        
        dispatcher.utter_message(text=message)
        
        # Lưu các ngành được đề xuất vào slot để tiếp tục trò chuyện
        return [SlotSet("suggested_majors", suggested_major_ids)]