from typing import List, Dict, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.graph_connector import GraphConnector  # ✅ import

class ActionCutoffScore(Action):
    def name(self) -> str:
        return "action_cutoff_score"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:

        # Các hàm normalize như cũ
        method_mapping = {
            "riêng": "Xét tuyển riêng",
            "thpt": "Điểm thi tốt nghiệp THPT",
            "tốt nghiệp": "Điểm thi tốt nghiệp THPT",
            "tn": "Điểm thi tốt nghiệp THPT",
            "đánh giá năng lực": "Đánh giá năng lực",
            "dgnl": "Đánh giá năng lực",
            "vact": "Đánh giá năng lực",
            "apt": "Đánh giá năng lực",
            "đánh giá tư duy": "Đánh giá tư duy",
            "tsa": "Đánh giá tư duy",
            "dgtd": "Đánh giá tư duy"
        }

        def normalize_method(text: Optional[str]) -> Optional[str]:
            if not text:
                return None
            text = text.lower()
            for key, value in method_mapping.items():
                if key in text:
                    return value
            return None

        def normalize_major(text: Optional[str]) -> Optional[str]:
            if not text:
                return None
            text = text.lower()
            if any(k in text for k in ["ai", "trí tuệ", "khoa học dữ liệu"]):
                return "cntt_ai"
            elif any(k in text for k in ["nhật", "ngoại", "nnn"]):
                return "cntt_nnn"
            elif any(k in text for k in ["htdn", "đặc thù", "hợp tác", "dt"]):
                return "cntt_htdn"
            return None

        major_keyword = normalize_major(tracker.get_slot("major"))
        method_keyword = normalize_method(tracker.get_slot("method"))

        # Truy vấn và xử lý kết quả
        if major_keyword and method_keyword:
            rows = self.db.get_cutoff_by_major_and_method(major_keyword, method_keyword)
            if rows:
                message = f"**Điểm chuẩn {method_keyword} của ngành {rows[0]['major']}**:\n"
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
        method_mapping = {
            "riêng": "xtr",
            "xét tuyển riêng": "xtr",
            "tốt nghiệp thpt": "tn_thpt",
            "tốt nghiệp": "tn_thpt",
            "tn": "tn_thpt",
            "đánh giá năng lực": "dgnl",
            "dgnl": "dgtd",
            "vact": "dgnl",
            "apt": "dgnl",
            "đánh giá tư duy": "dgtd",
            "tsa": "dgtd",
            "dgtd": "dgtd",
            "học bạ": "hb_thpt",
            "học bạ thpt": "hb_thpt",
            "tuyển thẳng": "xtt",
            "xtt": "xtt",
            "xét tuyển thẳng": "xtt",
        }

        def normalize_method(text: Optional[str]) -> Optional[str]:
            if not text:
                return None
            text = text.lower()
            for key, value in method_mapping.items():
                if key in text:
                    return value
            return None
        method_keyword = normalize_method(tracker.get_slot("method"))

        if method_keyword:
            rows = self.db.get_major_by_method(method_keyword)
            if rows:
                message = f"📌 **Các ngành có xét tuyển bằng phương thức {method_keyword}**:\n"
                for row in rows:
                    message += f"- {row['major']}\n"
            else:
                message = "❌ Không tìm thấy ngành nào có phương thức tuyển sinh này."
        else:
            message = "❗ Vui lòng cung cấp tên phương thức xét tuyển."

        dispatcher.utter_message(text=message)
        return []