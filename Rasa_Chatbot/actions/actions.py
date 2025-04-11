from typing import List, Dict, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCutoffScore(Action):
    def name(self) -> str:
        return "action_cutoff_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:
        
        # Lấy slot
        major = tracker.get_slot("major")
        method = tracker.get_slot("method")

        # Mapping từ khóa về phương thức
        method_mapping = {
            "riêng": "Xét tuyển riêng",
            "thpt": "Xét tuyển bằng Điểm thi Tốt nghiệp THPT",
            "tốt nghiệp": "Xét tuyển bằng Điểm thi Tốt nghiệp THPT",
            "tn": "Xét tuyển bằng Điểm thi Tốt nghiệp THPT",
            "đánh giá năng lực": "Xét tuyển bằng Điểm thi Đánh giá năng lực của ĐHQG TPHCM",
            "dgnl": "Xét tuyển bằng Điểm thi Đánh giá năng lực của ĐHQG TPHCM",
            "vact": "Xét tuyển bằng Điểm thi Đánh giá năng lực của ĐHQG TPHCM",
            "apt": "Xét tuyển bằng Điểm thi Đánh giá năng lực của ĐHQG TPHCM",
            "đánh giá tư duy": "Xét tuyển bằng Điểm thi Đánh giá tư duy của Đại Học Bách Khoa Hà Nội",
            "tsa": "Xét tuyển bằng Điểm thi Đánh giá tư duy của Đại Học Bách Khoa Hà Nội",
            "dgtd": "Xét tuyển bằng Điểm thi Đánh giá tư duy của Đại Học Bách Khoa Hà Nội"
        }

        # Mapping ngành theo keyword
        def normalize_major(major_text: str) -> Optional[str]:
            major_lower = major_text.lower()
            if any(k in major_lower for k in ["ai", "trí tuệ", "khoa học dữ liệu"]):
                return "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), Chuyên ngành Khoa học dữ liệu và trí tuệ nhân tạo"
            elif any(k in major_lower for k in ["nhật", "ngoại", "nnn"]):
                return "Công nghệ thông tin (Ngoại ngữ nhật)"
            elif any(k in major_lower for k in ["htdn", "đặc thù", "đặc", "hợp tác", "dt"]):
                return "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)"
            return None

        def normalize_method(method_text: str) -> Optional[str]:
            method_lower = method_text.lower()
            for keyword, value in method_mapping.items():
                if keyword in method_lower:
                    return value
            return None

        method_key = normalize_method(method) if method else None
        major_key = normalize_major(major) if major else None

        # Dữ liệu điểm chuẩn
        data = {
            "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)": {
                "Xét tuyển riêng": "• Năm 2023: 289.4\n• Năm 2024: 288.6",
                "Xét tuyển bằng Điểm thi Tốt nghiệp THPT": "• Năm 2023: 25.86\n• Năm 2024: 26.10",
                "Xét tuyển bằng Điểm thi Đánh giá năng lực của ĐHQG TPHCM": "• Năm 2023: 927.0\n• Năm 2024: 958.0",
                "Xét tuyển bằng Điểm thi Đánh giá tư duy của Đại Học Bách Khoa Hà Nội": "• Năm 2023: 69.13\n• Năm 2024: 66.64"
            },
            "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), Chuyên ngành Khoa học dữ liệu và trí tuệ nhân tạo": {
                "Xét tuyển riêng": "• Năm 2023: 298.6\n• Năm 2024: 298.9",
                "Xét tuyển bằng Điểm thi Tốt nghiệp THPT": "• Năm 2023: 26.45\n• Năm 2024: 27.11",
                "Xét tuyển bằng Điểm thi Đánh giá năng lực của ĐHQG TPHCM": "• Năm 2023: 979.6\n• Năm 2024: 926.0",
                "Xét tuyển bằng Điểm thi Đánh giá tư duy của Đại Học Bách Khoa Hà Nội": "• Năm 2023: 72.97\n• Năm 2024: 73.57"
            },
            "Công nghệ thông tin (Ngoại ngữ nhật)": {
                "Xét tuyển riêng": "• Năm 2023: 280.0\n• Năm 2024: 229.3",
                "Xét tuyển bằng Điểm thi Tốt nghiệp THPT": "• Năm 2023: 25.00\n• Năm 2024: 25.55",
                "Xét tuyển bằng Điểm thi Đánh giá năng lực của ĐHQG TPHCM": "• Năm 2023: 820\n• Năm 2024: 806",
                "Xét tuyển bằng Điểm thi Đánh giá tư duy của Đại Học Bách Khoa Hà Nội": "• Năm 2023: 61.93\n• Năm 2024: 62.07"
            }
        }

        # Tạo phản hồi
        message = ""

        if major_key and method_key:
            scores = data.get(major_key, {}).get(method_key)
            if scores:
                message = f"**Điểm chuẩn {method_key} của {major_key}**:\n{scores}"
            else:
                message = "Xin lỗi, không có dữ liệu cho ngành và phương thức bạn yêu cầu."
        elif major_key:
            scores_all = data.get(major_key)
            if scores_all:
                message = f"**Điểm chuẩn của {major_key}**:\n"
                for method_name, score in scores_all.items():
                    message += f"\n👉 {method_name}:\n{score}\n"
            else:
                message = "Xin lỗi, không tìm thấy thông tin cho ngành bạn hỏi."
        elif method_key:
            message = f"**Điểm chuẩn theo phương thức {method_key}**:\n"
            found = False
            for major_name, methods in data.items():
                if method_key in methods:
                    found = True
                    message += f"\n👉 {major_name}:\n{methods[method_key]}\n"
            if not found:
                message = "Không tìm thấy ngành nào có phương thức tuyển sinh như bạn hỏi."
        else:
            message = "**Tất cả điểm chuẩn hiện có:**\n"
            for major_name, methods in data.items():
                message += f"\n📌 {major_name}:\n"
                for method_name, score in methods.items():
                    message += f"- {method_name}:\n{score}\n"

        dispatcher.utter_message(text=message)
        return []
