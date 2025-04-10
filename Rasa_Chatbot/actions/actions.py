from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCutoffScore(Action):
    def name(self) -> str:
        return "action_cutoff_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Lấy slot
        major = tracker.get_slot("major")
        method = tracker.get_slot("method")

        # Dữ liệu điểm chuẩn
        data = {
            "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)": {
                "Xét tuyển riêng": "• Năm 2023: 289.4\n• Năm 2024: 288.6",
                "Xét tuyển bằng Điểm thi Tốt nghiệp THPT": "• Năm 2023: 25.86\n• Năm 2024: 26.1"
            },
            "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), Chuyên ngành Khoa học dữ liệu và trí tuệ nhân tạo": {
                "Xét tuyển riêng": "• Năm 2023: 298.6\n• Năm 2024: 298.9",
                "Xét tuyển bằng Điểm thi Tốt nghiệp THPT": "• Năm 2023: 26.45\n• Năm 2024: 27.11"
            },
            "Công nghệ thông tin (Ngoại ngữ nhật)": {
                "Xét tuyển riêng": "• Năm 2023: 280.0\n• Năm 2024: 229.3",
                "Xét tuyển bằng Điểm thi Tốt nghiệp THPT": "• Năm 2023: 25.00\n• Năm 2024: 25.55"
            }
        }

        # Chuẩn hóa method
        method_key = None
        if method:
            method_lower = method.lower()
            if "riêng" in method_lower:
                method_key = "Xét tuyển riêng"
            elif "thpt" in method_lower or "tốt nghiệp" in method_lower:
                method_key = "Xét tuyển bằng Điểm thi Tốt nghiệp THPT"

        # Chuẩn hóa major
        major_key = None
        if major:
            major_lower = major.lower()
            if "htdn" in major_lower or ("đặc" in major_lower and "hợp tác" in major_lower):
                major_key = "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)"
            elif "ai" in major_lower or "trí tuệ" in major_lower or "khoa học dữ liệu" in major_lower:
                major_key = "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), Chuyên ngành Khoa học dữ liệu và trí tuệ nhân tạo"
            elif "nhật" in major_lower or "ngoại" in major_lower or "nnn" in major_lower:
                major_key = "Công nghệ thông tin (Ngoại ngữ nhật)"

        # Tạo kết quả phản hồi
        message = ""

        if major_key and method_key:
            # Trường hợp có đủ ngành và phương thức
            scores = data.get(major_key, {}).get(method_key)
            if scores:
                message = f"**Điểm chuẩn {method_key} của {major_key}**:\n{scores}"
            else:
                message = "Xin lỗi, không có dữ liệu cho ngành và phương thức bạn yêu cầu."
        elif major_key:
            # Chỉ có ngành, trả về tất cả phương thức cho ngành đó
            scores_all = data.get(major_key)
            if scores_all:
                message = f"**Điểm chuẩn của {major_key}**:\n"
                for method_name, score in scores_all.items():
                    message += f"\n👉 {method_name}:\n{score}\n"
            else:
                message = "Xin lỗi, không tìm thấy thông tin cho ngành bạn hỏi."
        elif method_key:
            # Chỉ có phương thức, trả về tất cả ngành áp dụng phương thức đó
            message = f"**Điểm chuẩn theo phương thức {method_key}**:\n"
            found = False
            for major_name, methods in data.items():
                if method_key in methods:
                    found = True
                    message += f"\n👉 {major_name}:\n{methods[method_key]}\n"
            if not found:
                message = "Không tìm thấy ngành nào có phương thức tuyển sinh như bạn hỏi."
        else:
            # Không có cả 2, trả về toàn bộ
            message = "**Tất cả điểm chuẩn hiện có:**\n"
            for major_name, methods in data.items():
                message += f"\n📌 {major_name}:\n"
                for method_name, score in methods.items():
                    message += f"- {method_name}:\n{score}\n"

        dispatcher.utter_message(text=message)
        return []
