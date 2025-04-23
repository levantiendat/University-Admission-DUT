from typing import List, Dict, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.graph_connector import GraphConnector  # ✅ import
import logging  # Thêm import cho thư viện logging

# Cấu hình logging (tùy chọn)
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

        # Các hàm normalize như cũ
        method_mapping = {
            "riêng": "xtr",
            "thpt": "tn_thpt",
            "tốt nghiệp": "tn_thpt",
            "tn": "tn_thpt",
            "đánh giá năng lực": "dgnl",
            "dgnl": "dgnl",
            "vact": "dgnl",
            "apt": "dgnl",
            "đánh giá tư duy": "dgtd",
            "tsa": "dgtd",
            "dgtd": "dgtd",
            "học bạ": "hb_thpt"
        }

        major_mapping = {
            # Công nghệ thông tin
            "cntt đặc thù": "cntt_htdn",
            "cntt htdn": "cntt_htdn",
            "công nghệ thông tin đặc thù": "cntt_htdn",
            "công nghệ thông tin hợp tác doanh nghiệp": "cntt_htdn",
            "công nghệ thông tin đặc thù - hợp tác doanh nghiệp": "cntt_htdn",
            "cntt": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table
            "công nghệ thông tin": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table

            "cntt nhật": "cntt_nnn",
            "cntt tiếng nhật": "cntt_nnn",
            "cntt nn nhật": "cntt_nnn",
            "công nghệ thông tin ngoại ngữ nhật": "cntt_nnn",
            "công nghệ thông tin nhật": "cntt_nnn",
            "công nghệ thông tin tiếng nhật": "cntt_nnn",
            
            "cntt ai": "cntt_ai",
            "cntt khdl": "cntt_ai",
            "cntt khdl & ttnt": "cntt_ai",
            "cntt ttnt": "cntt_ai",
            "công nghệ thông tin trí tuệ nhân tạo": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu và trí tuệ nhân tạo": "cntt_ai",
            "cntt đặc thù khdl": "cntt_ai",
            
            # Kỹ thuật máy tính
            "ktmt": "ktmt",
            "kỹ thuật máy tính": "ktmt",
            
            # Công nghệ sinh học
            "cnsh": "cnsinhhoc",
            "công nghệ sinh học": "cnsinhhoc",
            "cnsh y dược": "cnsinhhoc_yd",
            "cnsh yd": "cnsinhhoc_yd",
            "công nghệ sinh học y dược": "cnsinhhoc_yd",
            "công nghệ sinh học chuyên ngành y dược": "cnsinhhoc_yd",
            "sinh học y dược": "cnsinhhoc_yd",
            
            # Công nghệ kỹ thuật vật liệu xây dựng
            "cnkt vlxd": "vlxd",
            "công nghệ kỹ thuật vật liệu xây dựng": "vlxd",
            "vật liệu xây dựng": "vlxd",
            
            # Công nghệ chế tạo máy
            "cnctm": "ctm",
            "công nghệ chế tạo máy": "ctm",
            "chế tạo máy": "ctm",
            
            # Quản lý công nghiệp
            "qlcn": "qlcn",
            "quản lý công nghiệp": "qlcn",
            
            # Công nghệ dầu khí và khai thác dầu
            "cndk&ktd": "daukhi",
            "cndk": "daukhi",
            "công nghệ dầu khí": "daukhi",
            "công nghệ dầu khí và khai thác dầu": "daukhi",
            "dầu khí và khai thác dầu": "daukhi",
            "khai thác dầu": "daukhi",
            
            # Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)
            "pfiev": "pfiev",
            "kỹ sư chất lượng cao việt - pháp": "pfiev",
            "ctđt kỹ sư clc việt - pháp": "pfiev",
            "kỹ sư việt pháp": "pfiev",
            "chương trình việt pháp": "pfiev",
            
            # Kỹ thuật Cơ khí
            "ktck": "ck_dongluc",  # Note: default to dynamic mechanical option
            "kỹ thuật cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            "cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            
            "ktck ckđl": "ck_dongluc",
            "cơ khí động lực": "ck_dongluc",
            "ktck chuyên ngành cơ khí động lực": "ck_dongluc",
            "kỹ thuật cơ khí động lực": "ck_dongluc",
            
            "ktck ckhk": "ck_hk",
            "kỹ thuật cơ khí hàng không": "ck_hk",
            "cơ khí hàng không": "ck_hk",
            "ktck chuyên ngành ckhk": "ck_hk",
            
            # Kỹ thuật Cơ điện tử
            "ktcđt": "cdt",
            "kỹ thuật cơ điện tử": "cdt",
            "cơ điện tử": "cdt",
            "cdt": "cdt",
            
            # Kỹ thuật nhiệt
            "ktn": "ktnhiet",
            "kỹ thuật nhiệt": "ktnhiet",
            "kỹ thuật nhiệt lạnh": "ktnhiet",
            
            "ktn qlnl": "ktnqlnl",
            "kỹ thuật nhiệt quản lý năng lượng": "ktnqlnl",
            "ktn chuyên ngành qlnl": "ktnqlnl",
            "kỹ thuật nhiệt qlnl": "ktnqlnl",
            "quản lý năng lượng": "ktnqlnl",
            
            # Kỹ thuật Tàu thủy
            "kttt": "tauthuy",
            "kỹ thuật tàu thủy": "tauthuy",
            "tàu thủy": "tauthuy",
            
            # Kỹ thuật Điện
            "ktđ": "ktdien",
            "kỹ thuật điện": "ktdien",
            "điện": "ktdien",
            
            # Kỹ thuật điện tử - viễn thông
            "ktđt-vt": "dtvt",
            "ktđtvt": "dtvt",
            "kỹ thuật điện tử - viễn thông": "dtvt",
            "ktđt viễn thông": "dtvt",
            "kỹ thuật điện tử viễn thông": "dtvt",
            "điện tử viễn thông": "dtvt",
            "đtvt": "dtvt",
            
            # Kỹ thuật điện tử - viễn thông, chuyên ngành vi điện tử - thiết kế vi mạch
            "ktđt-vt vđt-tkvm": "vidientu_vimach",
            "điện tử vi mạch": "vidientu_vimach",
            "vi điện tử": "vidientu_vimach",
            "thiết kế vi mạch": "vidientu_vimach",
            
            # Kỹ thuật Điều khiển và Tự động hóa
            "ktđk&tđh": "tudonghoa",
            "ktđktđh": "tudonghoa",
            "kỹ thuật điều khiển và tự động hóa": "tudonghoa",
            "ktđk và tđh": "tudonghoa",
            "kỹ thuật điều khiển tự động hóa": "tudonghoa",
            "điều khiển tự động hóa": "tudonghoa",
            "tự động hóa": "tudonghoa",
            "điều khiển và tự động hóa": "tudonghoa",
            
            # Kỹ thuật hóa học
            "kthh": "kthh",
            "kỹ thuật hóa học": "kthh",
            "hóa học": "kthh",
            
            # Kỹ thuật môi trường
            "ktmt": "mt",
            "kỹ thuật môi trường": "mt",
            "môi trường": "mt",
            
            # Kỹ thuật hệ thống công nghiệp
            "kthtcn": "htcn",
            "kỹ thuật hệ thống công nghiệp": "htcn",
            "hệ thống công nghiệp": "htcn",
            
            # Chương trình tiên tiến Việt-Mỹ
            "cttt ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến kỹ thuật điện tử viễn thông": "tien_tien_dtvt",
            "cttt việt-mỹ ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến ktđtvt": "tien_tien_dtvt",
            "tiên tiến điện tử viễn thông": "tien_tien_dtvt",
            "cttt đtvt": "tien_tien_dtvt",
            
            "cttt htn&iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "cttt việt-mỹ htn và iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "cttt htn": "tien_tien_nhung_iot",
            "hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "hệ thống nhúng": "tien_tien_nhung_iot",
            
            # Công nghệ thực phẩm
            "cntp": "cntp",
            "công nghệ thực phẩm": "cntp",
            "thực phẩm": "cntp",
            
            # Kiến trúc
            "kt": "kientruc",
            "kiến trúc": "kientruc",
            
            # Kỹ thuật xây dựng
            "ktxd xddd&cn": "xddc_cn",
            "kỹ thuật xây dựng dân dụng và công nghiệp": "xddc_cn",
            "ktxd chuyên ngành xddd&cn": "xddc_cn",
            "xây dựng dân dụng và công nghiệp": "xddc_cn",
            "xd dân dụng": "xddc_cn",
            "xd công nghiệp": "xddc_cn",
            "kỹ thuật xây dựng dân dụng": "xddc_cn",
            
            "ktxd thxd": "thxd",
            "kỹ thuật xây dựng tin học xây dựng": "thxd",
            "ktxd chuyên ngành thxd": "thxd",
            "tin học xây dựng": "thxd",
            "thxd": "thxd",
            
            "ktxd đttm": "xdtttm",
            "kỹ thuật xây dựng đô thị thông minh": "xdtttm",
            "ktxd qlxd đttm": "xdtttm",
            "kỹ thuật và quản lý xây dựng đô thị thông minh": "xdtttm",
            "xây dựng đô thị thông minh": "xdtttm",
            "đô thị thông minh": "xdtttm",
            
            "ktxd mhtt&ttnt": "bim_ai",
            "kỹ thuật xây dựng mô hình thông tin và ttnt": "bim_ai",
            "ktxd chuyên ngành mhtt và ttnt": "bim_ai",
            "kỹ thuật xây dựng mhtt và ttnt": "bim_ai",
            "mô hình thông tin trong xây dựng": "bim_ai",
            "mhtt và ttnt trong xây dựng": "bim_ai",
            "trí tuệ nhân tạo trong xây dựng": "bim_ai",
            
            # Kỹ thuật xây dựng công trình thủy
            "ktxdctt": "ctthuy",
            "kỹ thuật xây dựng công trình thủy": "ctthuy",
            "xây dựng công trình thủy": "ctthuy",
            "công trình thủy": "ctthuy",
            
            # Kỹ thuật xây dựng công trình giao thông
            "ktxdctgt": "ctgt",
            "kỹ thuật xây dựng công trình giao thông": "ctgt",
            "xây dựng công trình giao thông": "ctgt",
            "công trình giao thông": "ctgt",
            "cầu đường": "ctgt",
            
            "ktxdctgt đstđc": "duongsat",
            "xây dựng đường sắt tốc độ cao": "duongsat",
            "ktxdctgt chuyên ngành đstđc": "duongsat",
            "xây dựng đường sắt đô thị": "duongsat",
            "đường sắt tốc độ cao": "duongsat",
            "đường sắt đô thị": "duongsat",
            
            # Kinh tế xây dựng
            "ktxd": "ktxd",
            "kinh tế xây dựng": "ktxd",
            
            # Kỹ thuật cơ sở hạ tầng
            "ktcsht": "cshatng",
            "kỹ thuật cơ sở hạ tầng": "cshatng",
            "cơ sở hạ tầng": "cshatng",
            "hạ tầng": "cshatng",
            
            # Quản lý tài nguyên và môi trường
            "qltn&mt": "qltn_mt",
            "quản lý tài nguyên và môi trường": "qltn_mt",
            "qltnmt": "qltn_mt",
            "tài nguyên và môi trường": "qltn_mt",
            "tài nguyên môi trường": "qltn_mt",

            "ô tô": "oto",
            "kỹ thuật ô tô": "oto",
        }

        # Danh sách các từ khóa quan trọng để xác định ngành chính xác
        major_keywords = {
            "cntt": ["công nghệ thông tin", "cntt"],
            "ktmt": ["kỹ thuật máy tính", "ktmt"],
            "cnsh": ["công nghệ sinh học", "cnsh"],
            "vlxd": ["vật liệu xây dựng", "vlxd"],
            "ctm": ["chế tạo máy", "ctm"],
            "qlcn": ["quản lý công nghiệp", "qlcn"],
            "dầu khí": ["dầu khí", "khai thác dầu"],
            "pfiev": ["pfiev", "việt pháp"],
            "cơ khí": ["cơ khí", "ckhk", "ckđl"],
            "cơ điện tử": ["cơ điện tử", "cđt"],
            "nhiệt": ["nhiệt", "năng lượng"],
            "tàu thủy": ["tàu thủy"],
            "điện": ["điện", "ktđ"],
            "điện tử": ["điện tử", "viễn thông", "đtvt"],
            "tự động hóa": ["tự động hóa", "điều khiển"],
            "hóa học": ["hóa học"],
            "môi trường": ["môi trường"],
            "hệ thống": ["hệ thống công nghiệp"],
            "tiên tiến": ["tiên tiến", "việt-mỹ", "cttt"],
            "nhúng": ["nhúng", "iot"],
            "thực phẩm": ["thực phẩm", "cntp"],
            "kiến trúc": ["kiến trúc"],
            "xây dựng": ["xây dựng", "ktxd", "xd"],
            "dân dụng": ["dân dụng", "công nghiệp"],
            "tin học xây dựng": ["tin học xây dựng"],
            "đô thị thông minh": ["đô thị thông minh"],
            "công trình thủy": ["công trình thủy"],
            "giao thông": ["giao thông", "cầu đường"],
            "đường sắt": ["đường sắt"],
            "kinh tế xây dựng": ["kinh tế xây dựng"],
            "hạ tầng": ["hạ tầng", "csht"],
            "tài nguyên": ["tài nguyên", "tnmt"],
            "ô tô": ["ô tô", "xe hơi"],
        }

        def clean_text(text):
            # Làm sạch văn bản và xóa các ký tự đặc biệt
            import re
            text = text.lower().strip()
            text = re.sub(r'[^\w\s&-]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text

        def normalize_major(text: Optional[str]) -> Optional[str]:
            if not text:
                return None
                
            # Làm sạch và chuẩn hóa văn bản đầu vào
            normalized_text = clean_text(text)
            
            # Thử tìm kiếm trực tiếp trong mapping
            if normalized_text in major_mapping:
                return major_mapping[normalized_text]
            
            # Giải quyết các trường hợp đặc biệt
            if normalized_text == "ktxd":
                # Nếu chỉ có "ktxd" thì mặc định là "Kinh tế xây dựng"
                return "Kinh tế xây dựng"
            
            if normalized_text == "ktmt":
                # Nếu chỉ có "ktmt" có thể là "Kỹ thuật máy tính" hoặc "Kỹ thuật môi trường"
                # Mặc định là "Kỹ thuật máy tính"
                if "môi trường" in normalized_text:
                    return "Kỹ thuật môi trường"
                return "Kỹ thuật máy tính"
            
            # Tìm kiếm dựa trên từng từ khóa trong text và tính điểm khớp
            match_scores = {}
            for key, value in major_mapping.items():
                # Tính điểm dựa trên có bao nhiêu từ của key có trong text
                key_words = key.split()
                score = sum(1 for word in key_words if word in normalized_text)
                
                # Cộng điểm nếu có từ khóa đặc biệt
                for kw_group, keywords in major_keywords.items():
                    if any(kw in key for kw in keywords) and any(kw in normalized_text for kw in keywords):
                        score += 2
                
                # Cộng điểm nếu key là một phần của text
                if key in normalized_text:
                    score += 3
                    
                # Lưu điểm và tên ngành đầy đủ
                if score > 0:
                    match_scores[value] = match_scores.get(value, 0) + score
            
            # Trả về kết quả có điểm cao nhất nếu có
            if match_scores:
                return max(match_scores.items(), key=lambda x: x[1])[0]
                    
            # Nếu không tìm thấy từ khóa, tìm kiếm keyword có trong text
            for key, value in major_mapping.items():
                if key in normalized_text:
                    return value
                    
            return None

        def normalize_method(text: Optional[str]) -> Optional[str]:
            """
            Cải thiện xác định phương thức xét tuyển từ văn bản nhập vào.
            """
            if not text:
                return None
                
            # Làm sạch và chuẩn hóa văn bản
            text = clean_text(text)
            
            # Tạo từ điển phụ cho các biến thể cách viết phương thức xét tuyển
            method_variants = {
                "tn_thpt": ["thi thpt", "điểm thi", "tốt nghiệp thpt", "thpt", "tn", "tốt nghiệp trung học phổ thông"],
                "dgnl": ["năng lực", "dgnl", "đgnl", "vact", "apt", "bài test năng lực"],
                "dgtd": ["tư duy", "dgtd", "tsa", "bài test tư duy"],
                "hb_thpt": ["học bạ", "xét học bạ", "điểm học bạ", "tbhb", "xhb", "học bạ thpt"],
                "xtr": ["tuyển riêng", "xét riêng", "riêng", "phỏng vấn"]
            }
            
            # Thử chính xác từng từ khóa trong method_mapping
            for key, value in method_mapping.items():
                if key == text:  # Khớp chính xác
                    return value
                elif key in text:  # Khớp một phần
                    # Kiểm tra nếu key là một từ hoàn chỉnh trong text
                    words = text.split()
                    if key in words:
                        return value
            
            # Sử dụng từ điển phụ để tìm kiếm khi không có kết quả trực tiếp
            best_match = None
            max_score = 0
            
            for method_name, variants in method_variants.items():
                # Tính điểm cho mỗi phương thức dựa vào sự xuất hiện của các biến thể
                score = 0
                for variant in variants:
                    if variant in text:
                        # Từ khóa hoàn chỉnh có điểm cao hơn
                        if variant in text.split():
                            score += 2
                        else:
                            score += 1
                        
                # Lưu kết quả có điểm cao nhất
                if score > max_score:
                    max_score = score
                    # Tìm giá trị tương ứng trong method_mapping
                    best_match = next((v for k, v in method_mapping.items() if method_name.startswith(v)), method_name)
                    
            # Trả về kết quả tốt nhất nếu có
            if best_match and max_score > 0:
                return best_match
                
            return None

        # Lấy dữ liệu từ tracker
        major_input = tracker.get_slot("major")
        method_input = tracker.get_slot("method")
        
        # Ghi log thông tin đầu vào để debug (tùy chọn)
        # logging.debug(f"Major input: {major_input}, Method input: {method_input}")
        
        # Chuẩn hóa dữ liệu
        major_keyword = normalize_major(major_input)
        method_keyword = normalize_method(method_input)

        print(f"Normalized major: {major_keyword}, Normalized method: {method_keyword}")
        # Ghi log thông tin đã chuẩn hóa để debug (tùy chọn)
        logging.debug(f"Normalized major: {major_keyword}, Normalized method: {method_keyword}")
        
        # Ghi log kết quả chuẩn hóa để debug (tùy chọn)
        # logging.debug(f"Normalized major: {major_keyword}, Normalized method: {method_keyword}")

        # Truy vấn và xử lý kết quả như cũ
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
    
class ActionCombinationMajor(Action):
    def name(self) -> str:
        return "action_combination_major"

    def __init__(self):
        self.db = GraphConnector()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[Dict]:

        # Ánh xạ từ tên viết tắt hoặc từ khóa sang tên đầy đủ của ngành
        major_mapping = {
            # Công nghệ thông tin
            "cntt đặc thù": "cntt_htdn",
            "cntt htdn": "cntt_htdn",
            "công nghệ thông tin đặc thù": "cntt_htdn",
            "công nghệ thông tin hợp tác doanh nghiệp": "cntt_htdn",
            "công nghệ thông tin đặc thù - hợp tác doanh nghiệp": "cntt_htdn",
            "cntt": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table
            "công nghệ thông tin": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table

            "cntt nhật": "cntt_nnn",
            "cntt tiếng nhật": "cntt_nnn",
            "cntt nn nhật": "cntt_nnn",
            "công nghệ thông tin ngoại ngữ nhật": "cntt_nnn",
            "công nghệ thông tin nhật": "cntt_nnn",
            "công nghệ thông tin tiếng nhật": "cntt_nnn",
            
            "cntt ai": "cntt_ai",
            "cntt khdl": "cntt_ai",
            "cntt khdl & ttnt": "cntt_ai",
            "cntt ttnt": "cntt_ai",
            "công nghệ thông tin trí tuệ nhân tạo": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu và trí tuệ nhân tạo": "cntt_ai",
            "cntt đặc thù khdl": "cntt_ai",
            
            # Kỹ thuật máy tính
            "ktmt": "ktmt",
            "kỹ thuật máy tính": "ktmt",
            
            # Công nghệ sinh học
            "cnsh": "cnsinhhoc",
            "công nghệ sinh học": "cnsinhhoc",
            "cnsh y dược": "cnsinhhoc_yd",
            "cnsh yd": "cnsinhhoc_yd",
            "công nghệ sinh học y dược": "cnsinhhoc_yd",
            "công nghệ sinh học chuyên ngành y dược": "cnsinhhoc_yd",
            "sinh học y dược": "cnsinhhoc_yd",
            
            # Công nghệ kỹ thuật vật liệu xây dựng
            "cnkt vlxd": "vlxd",
            "công nghệ kỹ thuật vật liệu xây dựng": "vlxd",
            "vật liệu xây dựng": "vlxd",
            
            # Công nghệ chế tạo máy
            "cnctm": "ctm",
            "công nghệ chế tạo máy": "ctm",
            "chế tạo máy": "ctm",
            
            # Quản lý công nghiệp
            "qlcn": "qlcn",
            "quản lý công nghiệp": "qlcn",
            
            # Công nghệ dầu khí và khai thác dầu
            "cndk&ktd": "daukhi",
            "cndk": "daukhi",
            "công nghệ dầu khí": "daukhi",
            "công nghệ dầu khí và khai thác dầu": "daukhi",
            "dầu khí và khai thác dầu": "daukhi",
            "khai thác dầu": "daukhi",
            
            # Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)
            "pfiev": "pfiev",
            "kỹ sư chất lượng cao việt - pháp": "pfiev",
            "ctđt kỹ sư clc việt - pháp": "pfiev",
            "kỹ sư việt pháp": "pfiev",
            "chương trình việt pháp": "pfiev",
            
            # Kỹ thuật Cơ khí
            "ktck": "ck_dongluc",  # Note: default to dynamic mechanical option
            "kỹ thuật cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            "cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            
            "ktck ckđl": "ck_dongluc",
            "cơ khí động lực": "ck_dongluc",
            "ktck chuyên ngành cơ khí động lực": "ck_dongluc",
            "kỹ thuật cơ khí động lực": "ck_dongluc",
            
            "ktck ckhk": "ck_hk",
            "kỹ thuật cơ khí hàng không": "ck_hk",
            "cơ khí hàng không": "ck_hk",
            "ktck chuyên ngành ckhk": "ck_hk",
            
            # Kỹ thuật Cơ điện tử
            "ktcđt": "cdt",
            "kỹ thuật cơ điện tử": "cdt",
            "cơ điện tử": "cdt",
            "cdt": "cdt",
            
            # Kỹ thuật nhiệt
            "ktn": "ktnhiet",
            "kỹ thuật nhiệt": "ktnhiet",
            "kỹ thuật nhiệt lạnh": "ktnhiet",
            
            "ktn qlnl": "ktnqlnl",
            "kỹ thuật nhiệt quản lý năng lượng": "ktnqlnl",
            "ktn chuyên ngành qlnl": "ktnqlnl",
            "kỹ thuật nhiệt qlnl": "ktnqlnl",
            "quản lý năng lượng": "ktnqlnl",
            
            # Kỹ thuật Tàu thủy
            "kttt": "tauthuy",
            "kỹ thuật tàu thủy": "tauthuy",
            "tàu thủy": "tauthuy",
            
            # Kỹ thuật Điện
            "ktđ": "ktdien",
            "kỹ thuật điện": "ktdien",
            "điện": "ktdien",
            
            # Kỹ thuật điện tử - viễn thông
            "ktđt-vt": "dtvt",
            "ktđtvt": "dtvt",
            "kỹ thuật điện tử - viễn thông": "dtvt",
            "ktđt viễn thông": "dtvt",
            "kỹ thuật điện tử viễn thông": "dtvt",
            "điện tử viễn thông": "dtvt",
            "đtvt": "dtvt",
            
            # Kỹ thuật điện tử - viễn thông, chuyên ngành vi điện tử - thiết kế vi mạch
            "ktđt-vt vđt-tkvm": "vidientu_vimach",
            "điện tử vi mạch": "vidientu_vimach",
            "vi điện tử": "vidientu_vimach",
            "thiết kế vi mạch": "vidientu_vimach",
            
            # Kỹ thuật Điều khiển và Tự động hóa
            "ktđk&tđh": "tudonghoa",
            "ktđktđh": "tudonghoa",
            "kỹ thuật điều khiển và tự động hóa": "tudonghoa",
            "ktđk và tđh": "tudonghoa",
            "kỹ thuật điều khiển tự động hóa": "tudonghoa",
            "điều khiển tự động hóa": "tudonghoa",
            "tự động hóa": "tudonghoa",
            "điều khiển và tự động hóa": "tudonghoa",
            
            # Kỹ thuật hóa học
            "kthh": "kthh",
            "kỹ thuật hóa học": "kthh",
            "hóa học": "kthh",
            
            # Kỹ thuật môi trường
            "ktmt": "mt",
            "kỹ thuật môi trường": "mt",
            "môi trường": "mt",
            
            # Kỹ thuật hệ thống công nghiệp
            "kthtcn": "htcn",
            "kỹ thuật hệ thống công nghiệp": "htcn",
            "hệ thống công nghiệp": "htcn",
            
            # Chương trình tiên tiến Việt-Mỹ
            "cttt ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến kỹ thuật điện tử viễn thông": "tien_tien_dtvt",
            "cttt việt-mỹ ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến ktđtvt": "tien_tien_dtvt",
            "tiên tiến điện tử viễn thông": "tien_tien_dtvt",
            "cttt đtvt": "tien_tien_dtvt",
            
            "cttt htn&iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "cttt việt-mỹ htn và iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "cttt htn": "tien_tien_nhung_iot",
            "hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "hệ thống nhúng": "tien_tien_nhung_iot",
            
            # Công nghệ thực phẩm
            "cntp": "cntp",
            "công nghệ thực phẩm": "cntp",
            "thực phẩm": "cntp",
            
            # Kiến trúc
            "kt": "kientruc",
            "kiến trúc": "kientruc",
            
            # Kỹ thuật xây dựng
            "ktxd xddd&cn": "xddc_cn",
            "kỹ thuật xây dựng dân dụng và công nghiệp": "xddc_cn",
            "ktxd chuyên ngành xddd&cn": "xddc_cn",
            "xây dựng dân dụng và công nghiệp": "xddc_cn",
            "xd dân dụng": "xddc_cn",
            "xd công nghiệp": "xddc_cn",
            "kỹ thuật xây dựng dân dụng": "xddc_cn",
            
            "ktxd thxd": "thxd",
            "kỹ thuật xây dựng tin học xây dựng": "thxd",
            "ktxd chuyên ngành thxd": "thxd",
            "tin học xây dựng": "thxd",
            "thxd": "thxd",
            
            "ktxd đttm": "xdtttm",
            "kỹ thuật xây dựng đô thị thông minh": "xdtttm",
            "ktxd qlxd đttm": "xdtttm",
            "kỹ thuật và quản lý xây dựng đô thị thông minh": "xdtttm",
            "xây dựng đô thị thông minh": "xdtttm",
            "đô thị thông minh": "xdtttm",
            
            "ktxd mhtt&ttnt": "bim_ai",
            "kỹ thuật xây dựng mô hình thông tin và ttnt": "bim_ai",
            "ktxd chuyên ngành mhtt và ttnt": "bim_ai",
            "kỹ thuật xây dựng mhtt và ttnt": "bim_ai",
            "mô hình thông tin trong xây dựng": "bim_ai",
            "mhtt và ttnt trong xây dựng": "bim_ai",
            "trí tuệ nhân tạo trong xây dựng": "bim_ai",
            
            # Kỹ thuật xây dựng công trình thủy
            "ktxdctt": "ctthuy",
            "kỹ thuật xây dựng công trình thủy": "ctthuy",
            "xây dựng công trình thủy": "ctthuy",
            "công trình thủy": "ctthuy",
            
            # Kỹ thuật xây dựng công trình giao thông
            "ktxdctgt": "ctgt",
            "kỹ thuật xây dựng công trình giao thông": "ctgt",
            "xây dựng công trình giao thông": "ctgt",
            "công trình giao thông": "ctgt",
            "cầu đường": "ctgt",
            
            "ktxdctgt đstđc": "duongsat",
            "xây dựng đường sắt tốc độ cao": "duongsat",
            "ktxdctgt chuyên ngành đstđc": "duongsat",
            "xây dựng đường sắt đô thị": "duongsat",
            "đường sắt tốc độ cao": "duongsat",
            "đường sắt đô thị": "duongsat",
            
            # Kinh tế xây dựng
            "ktxd": "ktxd",
            "kinh tế xây dựng": "ktxd",
            
            # Kỹ thuật cơ sở hạ tầng
            "ktcsht": "cshatng",
            "kỹ thuật cơ sở hạ tầng": "cshatng",
            "cơ sở hạ tầng": "cshatng",
            "hạ tầng": "cshatng",
            
            # Quản lý tài nguyên và môi trường
            "qltn&mt": "qltn_mt",
            "quản lý tài nguyên và môi trường": "qltn_mt",
            "qltnmt": "qltn_mt",
            "tài nguyên và môi trường": "qltn_mt",
            "tài nguyên môi trường": "qltn_mt",

            "ô tô": "oto",
            "kỹ thuật ô tô": "oto",
        }

        # Danh sách các từ khóa quan trọng để xác định ngành chính xác
        major_keywords = {
            "cntt": ["công nghệ thông tin", "cntt"],
            "ktmt": ["kỹ thuật máy tính", "ktmt"],
            "cnsh": ["công nghệ sinh học", "cnsh"],
            "vlxd": ["vật liệu xây dựng", "vlxd"],
            "ctm": ["chế tạo máy", "ctm"],
            "qlcn": ["quản lý công nghiệp", "qlcn"],
            "dầu khí": ["dầu khí", "khai thác dầu"],
            "pfiev": ["pfiev", "việt pháp"],
            "cơ khí": ["cơ khí", "ckhk", "ckđl"],
            "cơ điện tử": ["cơ điện tử", "cđt"],
            "nhiệt": ["nhiệt", "năng lượng"],
            "tàu thủy": ["tàu thủy"],
            "điện": ["điện", "ktđ"],
            "điện tử": ["điện tử", "viễn thông", "đtvt"],
            "tự động hóa": ["tự động hóa", "điều khiển"],
            "hóa học": ["hóa học"],
            "môi trường": ["môi trường"],
            "hệ thống": ["hệ thống công nghiệp"],
            "tiên tiến": ["tiên tiến", "việt-mỹ", "cttt"],
            "nhúng": ["nhúng", "iot"],
            "thực phẩm": ["thực phẩm", "cntp"],
            "kiến trúc": ["kiến trúc"],
            "xây dựng": ["xây dựng", "ktxd", "xd"],
            "dân dụng": ["dân dụng", "công nghiệp"],
            "tin học xây dựng": ["tin học xây dựng"],
            "đô thị thông minh": ["đô thị thông minh"],
            "công trình thủy": ["công trình thủy"],
            "giao thông": ["giao thông", "cầu đường"],
            "đường sắt": ["đường sắt"],
            "kinh tế xây dựng": ["kinh tế xây dựng"],
            "hạ tầng": ["hạ tầng", "csht"],
            "tài nguyên": ["tài nguyên", "tnmt"],
            "oto": ["ô tô", "kỹ thuật ô tô"]
        }

        def clean_text(text):
            # Làm sạch văn bản và xóa các ký tự đặc biệt
            import re
            text = text.lower().strip()
            text = re.sub(r'[^\w\s&-]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text

        def normalize_major(text: Optional[str]) -> Optional[str]:
            if not text:
                return None
                
            # Làm sạch và chuẩn hóa văn bản đầu vào
            normalized_text = clean_text(text)
            
            # Thử tìm kiếm trực tiếp trong mapping
            if normalized_text in major_mapping:
                return major_mapping[normalized_text]
            
            # Giải quyết các trường hợp đặc biệt
            if normalized_text == "ktxd":
                # Nếu chỉ có "ktxd" thì mặc định là "Kinh tế xây dựng"
                return "Kinh tế xây dựng"
            
            if normalized_text == "ktmt":
                # Nếu chỉ có "ktmt" có thể là "Kỹ thuật máy tính" hoặc "Kỹ thuật môi trường"
                # Mặc định là "Kỹ thuật máy tính"
                if "môi trường" in normalized_text:
                    return "Kỹ thuật môi trường"
                return "Kỹ thuật máy tính"
            
            # Tìm kiếm dựa trên từng từ khóa trong text và tính điểm khớp
            match_scores = {}
            for key, value in major_mapping.items():
                # Tính điểm dựa trên có bao nhiêu từ của key có trong text
                key_words = key.split()
                score = sum(1 for word in key_words if word in normalized_text)
                
                # Cộng điểm nếu có từ khóa đặc biệt
                for kw_group, keywords in major_keywords.items():
                    if any(kw in key for kw in keywords) and any(kw in normalized_text for kw in keywords):
                        score += 2
                
                # Cộng điểm nếu key là một phần của text
                if key in normalized_text:
                    score += 3
                    
                # Lưu điểm và tên ngành đầy đủ
                if score > 0:
                    match_scores[value] = match_scores.get(value, 0) + score
            
            # Trả về kết quả có điểm cao nhất nếu có
            if match_scores:
                return max(match_scores.items(), key=lambda x: x[1])[0]
                    
            # Nếu không tìm thấy từ khóa, tìm kiếm keyword có trong text
            for key, value in major_mapping.items():
                if key in normalized_text:
                    return value
                    
            return None

        # Lấy thông tin từ entity major trong message
        major_entity = next(tracker.get_latest_entity_values("major"), None)
        
        # Chuẩn hóa tên ngành
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

        # Các hàm normalize giống như trong ActionCutoffScore
        method_mapping = {
            "riêng": "xtr",
            "thpt": "tn_thpt",
            "tốt nghiệp": "tn_thpt",
            "tn": "tn_thpt",
            "đánh giá năng lực": "dgnl",
            "dgnl": "dgnl",
            "vact": "dgnl",
            "apt": "dgnl",
            "đánh giá tư duy": "dgtd",
            "tsa": "dgtd",
            "dgtd": "dgtd",
            "học bạ": "hb_thpt"
        }

        major_mapping = {
            # Công nghệ thông tin
            "cntt đặc thù": "cntt_htdn",
            "cntt htdn": "cntt_htdn",
            "công nghệ thông tin đặc thù": "cntt_htdn",
            "công nghệ thông tin hợp tác doanh nghiệp": "cntt_htdn",
            "công nghệ thông tin đặc thù - hợp tác doanh nghiệp": "cntt_htdn",
            "cntt": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table
            "công nghệ thông tin": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table

            "cntt nhật": "cntt_nnn",
            "cntt tiếng nhật": "cntt_nnn",
            "cntt nn nhật": "cntt_nnn",
            "công nghệ thông tin ngoại ngữ nhật": "cntt_nnn",
            "công nghệ thông tin nhật": "cntt_nnn",
            "công nghệ thông tin tiếng nhật": "cntt_nnn",
            
            "cntt ai": "cntt_ai",
            "cntt khdl": "cntt_ai",
            "cntt khdl & ttnt": "cntt_ai",
            "cntt ttnt": "cntt_ai",
            "công nghệ thông tin trí tuệ nhân tạo": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu và trí tuệ nhân tạo": "cntt_ai",
            "cntt đặc thù khdl": "cntt_ai",
            
            # Kỹ thuật máy tính
            "ktmt": "ktmt",
            "kỹ thuật máy tính": "ktmt",
            
            # Công nghệ sinh học
            "cnsh": "cnsinhhoc",
            "công nghệ sinh học": "cnsinhhoc",
            "cnsh y dược": "cnsinhhoc_yd",
            "cnsh yd": "cnsinhhoc_yd",
            "công nghệ sinh học y dược": "cnsinhhoc_yd",
            "công nghệ sinh học chuyên ngành y dược": "cnsinhhoc_yd",
            "sinh học y dược": "cnsinhhoc_yd",
            
            # Công nghệ kỹ thuật vật liệu xây dựng
            "cnkt vlxd": "vlxd",
            "công nghệ kỹ thuật vật liệu xây dựng": "vlxd",
            "vật liệu xây dựng": "vlxd",
            
            # Công nghệ chế tạo máy
            "cnctm": "ctm",
            "công nghệ chế tạo máy": "ctm",
            "chế tạo máy": "ctm",
            
            # Quản lý công nghiệp
            "qlcn": "qlcn",
            "quản lý công nghiệp": "qlcn",
            
            # Công nghệ dầu khí và khai thác dầu
            "cndk&ktd": "daukhi",
            "cndk": "daukhi",
            "công nghệ dầu khí": "daukhi",
            "công nghệ dầu khí và khai thác dầu": "daukhi",
            "dầu khí và khai thác dầu": "daukhi",
            "khai thác dầu": "daukhi",
            
            # Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)
            "pfiev": "pfiev",
            "kỹ sư chất lượng cao việt - pháp": "pfiev",
            "ctđt kỹ sư clc việt - pháp": "pfiev",
            "kỹ sư việt pháp": "pfiev",
            "chương trình việt pháp": "pfiev",
            
            # Kỹ thuật Cơ khí
            "ktck": "ck_dongluc",  # Note: default to dynamic mechanical option
            "kỹ thuật cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            "cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            
            "ktck ckđl": "ck_dongluc",
            "cơ khí động lực": "ck_dongluc",
            "ktck chuyên ngành cơ khí động lực": "ck_dongluc",
            "kỹ thuật cơ khí động lực": "ck_dongluc",
            
            "ktck ckhk": "ck_hk",
            "kỹ thuật cơ khí hàng không": "ck_hk",
            "cơ khí hàng không": "ck_hk",
            "ktck chuyên ngành ckhk": "ck_hk",
            
            # Kỹ thuật Cơ điện tử
            "ktcđt": "cdt",
            "kỹ thuật cơ điện tử": "cdt",
            "cơ điện tử": "cdt",
            "cdt": "cdt",
            
            # Kỹ thuật nhiệt
            "ktn": "ktnhiet",
            "kỹ thuật nhiệt": "ktnhiet",
            "kỹ thuật nhiệt lạnh": "ktnhiet",
            
            "ktn qlnl": "ktnqlnl",
            "kỹ thuật nhiệt quản lý năng lượng": "ktnqlnl",
            "ktn chuyên ngành qlnl": "ktnqlnl",
            "kỹ thuật nhiệt qlnl": "ktnqlnl",
            "quản lý năng lượng": "ktnqlnl",
            
            # Kỹ thuật Tàu thủy
            "kttt": "tauthuy",
            "kỹ thuật tàu thủy": "tauthuy",
            "tàu thủy": "tauthuy",
            
            # Kỹ thuật Điện
            "ktđ": "ktdien",
            "kỹ thuật điện": "ktdien",
            "điện": "ktdien",
            
            # Kỹ thuật điện tử - viễn thông
            "ktđt-vt": "dtvt",
            "ktđtvt": "dtvt",
            "kỹ thuật điện tử - viễn thông": "dtvt",
            "ktđt viễn thông": "dtvt",
            "kỹ thuật điện tử viễn thông": "dtvt",
            "điện tử viễn thông": "dtvt",
            "đtvt": "dtvt",
            
            # Kỹ thuật điện tử - viễn thông, chuyên ngành vi điện tử - thiết kế vi mạch
            "ktđt-vt vđt-tkvm": "vidientu_vimach",
            "điện tử vi mạch": "vidientu_vimach",
            "vi điện tử": "vidientu_vimach",
            "thiết kế vi mạch": "vidientu_vimach",
            
            # Kỹ thuật Điều khiển và Tự động hóa
            "ktđk&tđh": "tudonghoa",
            "ktđktđh": "tudonghoa",
            "kỹ thuật điều khiển và tự động hóa": "tudonghoa",
            "ktđk và tđh": "tudonghoa",
            "kỹ thuật điều khiển tự động hóa": "tudonghoa",
            "điều khiển tự động hóa": "tudonghoa",
            "tự động hóa": "tudonghoa",
            "điều khiển và tự động hóa": "tudonghoa",
            
            # Kỹ thuật hóa học
            "kthh": "kthh",
            "kỹ thuật hóa học": "kthh",
            "hóa học": "kthh",
            
            # Kỹ thuật môi trường
            "ktmt": "mt",
            "kỹ thuật môi trường": "mt",
            "môi trường": "mt",
            
            # Kỹ thuật hệ thống công nghiệp
            "kthtcn": "htcn",
            "kỹ thuật hệ thống công nghiệp": "htcn",
            "hệ thống công nghiệp": "htcn",
            
            # Chương trình tiên tiến Việt-Mỹ
            "cttt ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến kỹ thuật điện tử viễn thông": "tien_tien_dtvt",
            "cttt việt-mỹ ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến ktđtvt": "tien_tien_dtvt",
            "tiên tiến điện tử viễn thông": "tien_tien_dtvt",
            "cttt đtvt": "tien_tien_dtvt",
            
            "cttt htn&iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "cttt việt-mỹ htn và iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "cttt htn": "tien_tien_nhung_iot",
            "hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "hệ thống nhúng": "tien_tien_nhung_iot",
            
            # Công nghệ thực phẩm
            "cntp": "cntp",
            "công nghệ thực phẩm": "cntp",
            "thực phẩm": "cntp",
            
            # Kiến trúc
            "kt": "kientruc",
            "kiến trúc": "kientruc",
            
            # Kỹ thuật xây dựng
            "ktxd xddd&cn": "xddc_cn",
            "kỹ thuật xây dựng dân dụng và công nghiệp": "xddc_cn",
            "ktxd chuyên ngành xddd&cn": "xddc_cn",
            "xây dựng dân dụng và công nghiệp": "xddc_cn",
            "xd dân dụng": "xddc_cn",
            "xd công nghiệp": "xddc_cn",
            "kỹ thuật xây dựng dân dụng": "xddc_cn",
            
            "ktxd thxd": "thxd",
            "kỹ thuật xây dựng tin học xây dựng": "thxd",
            "ktxd chuyên ngành thxd": "thxd",
            "tin học xây dựng": "thxd",
            "thxd": "thxd",
            
            "ktxd đttm": "xdtttm",
            "kỹ thuật xây dựng đô thị thông minh": "xdtttm",
            "ktxd qlxd đttm": "xdtttm",
            "kỹ thuật và quản lý xây dựng đô thị thông minh": "xdtttm",
            "xây dựng đô thị thông minh": "xdtttm",
            "đô thị thông minh": "xdtttm",
            
            "ktxd mhtt&ttnt": "bim_ai",
            "kỹ thuật xây dựng mô hình thông tin và ttnt": "bim_ai",
            "ktxd chuyên ngành mhtt và ttnt": "bim_ai",
            "kỹ thuật xây dựng mhtt và ttnt": "bim_ai",
            "mô hình thông tin trong xây dựng": "bim_ai",
            "mhtt và ttnt trong xây dựng": "bim_ai",
            "trí tuệ nhân tạo trong xây dựng": "bim_ai",
            
            # Kỹ thuật xây dựng công trình thủy
            "ktxdctt": "ctthuy",
            "kỹ thuật xây dựng công trình thủy": "ctthuy",
            "xây dựng công trình thủy": "ctthuy",
            "công trình thủy": "ctthuy",
            
            # Kỹ thuật xây dựng công trình giao thông
            "ktxdctgt": "ctgt",
            "kỹ thuật xây dựng công trình giao thông": "ctgt",
            "xây dựng công trình giao thông": "ctgt",
            "công trình giao thông": "ctgt",
            "cầu đường": "ctgt",
            
            "ktxdctgt đstđc": "duongsat",
            "xây dựng đường sắt tốc độ cao": "duongsat",
            "ktxdctgt chuyên ngành đstđc": "duongsat",
            "xây dựng đường sắt đô thị": "duongsat",
            "đường sắt tốc độ cao": "duongsat",
            "đường sắt đô thị": "duongsat",
            
            # Kinh tế xây dựng
            "ktxd": "ktxd",
            "kinh tế xây dựng": "ktxd",
            
            # Kỹ thuật cơ sở hạ tầng
            "ktcsht": "cshatng",
            "kỹ thuật cơ sở hạ tầng": "cshatng",
            "cơ sở hạ tầng": "cshatng",
            "hạ tầng": "cshatng",
            
            # Quản lý tài nguyên và môi trường
            "qltn&mt": "qltn_mt",
            "quản lý tài nguyên và môi trường": "qltn_mt",
            "qltnmt": "qltn_mt",
            "tài nguyên và môi trường": "qltn_mt",
            "tài nguyên môi trường": "qltn_mt",

            "ô tô": "oto",
            "kỹ thuật ô tô": "oto",
        }

        # Danh sách các từ khóa quan trọng để xác định ngành chính xác
        major_keywords = {
            "cntt": ["công nghệ thông tin", "cntt"],
            "ktmt": ["kỹ thuật máy tính", "ktmt"],
            "cnsh": ["công nghệ sinh học", "cnsh"],
            "vlxd": ["vật liệu xây dựng", "vlxd"],
            "ctm": ["chế tạo máy", "ctm"],
            "qlcn": ["quản lý công nghiệp", "qlcn"],
            "dầu khí": ["dầu khí", "khai thác dầu"],
            "pfiev": ["pfiev", "việt pháp"],
            "cơ khí": ["cơ khí", "ckhk", "ckđl"],
            "cơ điện tử": ["cơ điện tử", "cđt"],
            "nhiệt": ["nhiệt", "năng lượng"],
            "tàu thủy": ["tàu thủy"],
            "điện": ["điện", "ktđ"],
            "điện tử": ["điện tử", "viễn thông", "đtvt"],
            "tự động hóa": ["tự động hóa", "điều khiển"],
            "hóa học": ["hóa học"],
            "môi trường": ["môi trường"],
            "hệ thống": ["hệ thống công nghiệp"],
            "tiên tiến": ["tiên tiến", "việt-mỹ", "cttt"],
            "nhúng": ["nhúng", "iot"],
            "thực phẩm": ["thực phẩm", "cntp"],
            "kiến trúc": ["kiến trúc"],
            "xây dựng": ["xây dựng", "ktxd", "xd"],
            "dân dụng": ["dân dụng", "công nghiệp"],
            "tin học xây dựng": ["tin học xây dựng"],
            "đô thị thông minh": ["đô thị thông minh"],
            "công trình thủy": ["công trình thủy"],
            "giao thông": ["giao thông", "cầu đường"],
            "đường sắt": ["đường sắt"],
            "kinh tế xây dựng": ["kinh tế xây dựng"],
            "hạ tầng": ["hạ tầng", "csht"],
            "tài nguyên": ["tài nguyên", "tnmt"],
            "ô tô": ["ô tô", "xe hơi"],
        }

        def clean_text(text):
            # Làm sạch văn bản và xóa các ký tự đặc biệt
            import re
            text = text.lower().strip()
            text = re.sub(r'[^\w\s&-]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text

        def normalize_major(text: Optional[str]) -> Optional[str]:
            if not text:
                return None
                
            # Làm sạch và chuẩn hóa văn bản đầu vào
            normalized_text = clean_text(text)
            
            # Thử tìm kiếm trực tiếp trong mapping
            if normalized_text in major_mapping:
                return major_mapping[normalized_text]
            
            # Giải quyết các trường hợp đặc biệt
            if normalized_text == "ktxd":
                # Nếu chỉ có "ktxd" thì mặc định là "Kinh tế xây dựng"
                return "ktxd"
            
            if normalized_text == "ktmt":
                # Nếu chỉ có "ktmt" có thể là "Kỹ thuật máy tính" hoặc "Kỹ thuật môi trường"
                # Mặc định là "Kỹ thuật máy tính"
                if "môi trường" in normalized_text:
                    return "mt"
                return "ktmt"
            
            # Tìm kiếm dựa trên từng từ khóa trong text và tính điểm khớp
            match_scores = {}
            for key, value in major_mapping.items():
                # Tính điểm dựa trên có bao nhiêu từ của key có trong text
                key_words = key.split()
                score = sum(1 for word in key_words if word in normalized_text)
                
                # Cộng điểm nếu có từ khóa đặc biệt
                for kw_group, keywords in major_keywords.items():
                    if any(kw in key for kw in keywords) and any(kw in normalized_text for kw in keywords):
                        score += 2
                
                # Cộng điểm nếu key là một phần của text
                if key in normalized_text:
                    score += 3
                    
                # Lưu điểm và tên ngành đầy đủ
                if score > 0:
                    match_scores[value] = match_scores.get(value, 0) + score
            
            # Trả về kết quả có điểm cao nhất nếu có
            if match_scores:
                return max(match_scores.items(), key=lambda x: x[1])[0]
                    
            # Nếu không tìm thấy từ khóa, tìm kiếm keyword có trong text
            for key, value in major_mapping.items():
                if key in normalized_text:
                    return value
                    
            return None

        # Lấy dữ liệu từ tracker
        major_input = tracker.get_slot("major")
        
        # Chuẩn hóa dữ liệu
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

        # Các hàm normalize giống như trong ActionCutoffScore
        method_mapping = {
            "riêng": "xtr",
            "thpt": "tn_thpt",
            "tốt nghiệp": "tn_thpt",
            "tn": "tn_thpt",
            "đánh giá năng lực": "dgnl",
            "dgnl": "dgnl",
            "vact": "dgnl",
            "apt": "dgnl",
            "đánh giá tư duy": "dgtd",
            "tsa": "dgtd",
            "dgtd": "dgtd",
            "học bạ": "hb_thpt"
        }

        major_mapping = {
            # Công nghệ thông tin
            "cntt đặc thù": "cntt_htdn",
            "cntt htdn": "cntt_htdn",
            "công nghệ thông tin đặc thù": "cntt_htdn",
            "công nghệ thông tin hợp tác doanh nghiệp": "cntt_htdn",
            "công nghệ thông tin đặc thù - hợp tác doanh nghiệp": "cntt_htdn",
            "cntt": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table
            "công nghệ thông tin": "cntt_htdn",  # Note: default to cntt_htdn since no generic CNTT in table

            "cntt nhật": "cntt_nnn",
            "cntt tiếng nhật": "cntt_nnn",
            "cntt nn nhật": "cntt_nnn",
            "công nghệ thông tin ngoại ngữ nhật": "cntt_nnn",
            "công nghệ thông tin nhật": "cntt_nnn",
            "công nghệ thông tin tiếng nhật": "cntt_nnn",
            
            "cntt ai": "cntt_ai",
            "cntt khdl": "cntt_ai",
            "cntt khdl & ttnt": "cntt_ai",
            "cntt ttnt": "cntt_ai",
            "công nghệ thông tin trí tuệ nhân tạo": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu": "cntt_ai",
            "công nghệ thông tin khoa học dữ liệu và trí tuệ nhân tạo": "cntt_ai",
            "cntt đặc thù khdl": "cntt_ai",
            
            # Kỹ thuật máy tính
            "ktmt": "ktmt",
            "kỹ thuật máy tính": "ktmt",
            
            # Công nghệ sinh học
            "cnsh": "cnsinhhoc",
            "công nghệ sinh học": "cnsinhhoc",
            "cnsh y dược": "cnsinhhoc_yd",
            "cnsh yd": "cnsinhhoc_yd",
            "công nghệ sinh học y dược": "cnsinhhoc_yd",
            "công nghệ sinh học chuyên ngành y dược": "cnsinhhoc_yd",
            "sinh học y dược": "cnsinhhoc_yd",
            
            # Công nghệ kỹ thuật vật liệu xây dựng
            "cnkt vlxd": "vlxd",
            "công nghệ kỹ thuật vật liệu xây dựng": "vlxd",
            "vật liệu xây dựng": "vlxd",
            
            # Công nghệ chế tạo máy
            "cnctm": "ctm",
            "công nghệ chế tạo máy": "ctm",
            "chế tạo máy": "ctm",
            
            # Quản lý công nghiệp
            "qlcn": "qlcn",
            "quản lý công nghiệp": "qlcn",
            
            # Công nghệ dầu khí và khai thác dầu
            "cndk&ktd": "daukhi",
            "cndk": "daukhi",
            "công nghệ dầu khí": "daukhi",
            "công nghệ dầu khí và khai thác dầu": "daukhi",
            "dầu khí và khai thác dầu": "daukhi",
            "khai thác dầu": "daukhi",
            
            # Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)
            "pfiev": "pfiev",
            "kỹ sư chất lượng cao việt - pháp": "pfiev",
            "ctđt kỹ sư clc việt - pháp": "pfiev",
            "kỹ sư việt pháp": "pfiev",
            "chương trình việt pháp": "pfiev",
            
            # Kỹ thuật Cơ khí
            "ktck": "ck_dongluc",  # Note: default to dynamic mechanical option
            "kỹ thuật cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            "cơ khí": "ck_dongluc",  # Note: default to dynamic mechanical option
            
            "ktck ckđl": "ck_dongluc",
            "cơ khí động lực": "ck_dongluc",
            "ktck chuyên ngành cơ khí động lực": "ck_dongluc",
            "kỹ thuật cơ khí động lực": "ck_dongluc",
            
            "ktck ckhk": "ck_hk",
            "kỹ thuật cơ khí hàng không": "ck_hk",
            "cơ khí hàng không": "ck_hk",
            "ktck chuyên ngành ckhk": "ck_hk",
            
            # Kỹ thuật Cơ điện tử
            "ktcđt": "cdt",
            "kỹ thuật cơ điện tử": "cdt",
            "cơ điện tử": "cdt",
            "cdt": "cdt",
            
            # Kỹ thuật nhiệt
            "ktn": "ktnhiet",
            "kỹ thuật nhiệt": "ktnhiet",
            "kỹ thuật nhiệt lạnh": "ktnhiet",
            
            "ktn qlnl": "ktnqlnl",
            "kỹ thuật nhiệt quản lý năng lượng": "ktnqlnl",
            "ktn chuyên ngành qlnl": "ktnqlnl",
            "kỹ thuật nhiệt qlnl": "ktnqlnl",
            "quản lý năng lượng": "ktnqlnl",
            
            # Kỹ thuật Tàu thủy
            "kttt": "tauthuy",
            "kỹ thuật tàu thủy": "tauthuy",
            "tàu thủy": "tauthuy",
            
            # Kỹ thuật Điện
            "ktđ": "ktdien",
            "kỹ thuật điện": "ktdien",
            "điện": "ktdien",
            
            # Kỹ thuật điện tử - viễn thông
            "ktđt-vt": "dtvt",
            "ktđtvt": "dtvt",
            "kỹ thuật điện tử - viễn thông": "dtvt",
            "ktđt viễn thông": "dtvt",
            "kỹ thuật điện tử viễn thông": "dtvt",
            "điện tử viễn thông": "dtvt",
            "đtvt": "dtvt",
            
            # Kỹ thuật điện tử - viễn thông, chuyên ngành vi điện tử - thiết kế vi mạch
            "ktđt-vt vđt-tkvm": "vidientu_vimach",
            "điện tử vi mạch": "vidientu_vimach",
            "vi điện tử": "vidientu_vimach",
            "thiết kế vi mạch": "vidientu_vimach",
            
            # Kỹ thuật Điều khiển và Tự động hóa
            "ktđk&tđh": "tudonghoa",
            "ktđktđh": "tudonghoa",
            "kỹ thuật điều khiển và tự động hóa": "tudonghoa",
            "ktđk và tđh": "tudonghoa",
            "kỹ thuật điều khiển tự động hóa": "tudonghoa",
            "điều khiển tự động hóa": "tudonghoa",
            "tự động hóa": "tudonghoa",
            "điều khiển và tự động hóa": "tudonghoa",
            
            # Kỹ thuật hóa học
            "kthh": "kthh",
            "kỹ thuật hóa học": "kthh",
            "hóa học": "kthh",
            
            # Kỹ thuật môi trường
            "ktmt": "mt",
            "kỹ thuật môi trường": "mt",
            "môi trường": "mt",
            
            # Kỹ thuật hệ thống công nghiệp
            "kthtcn": "htcn",
            "kỹ thuật hệ thống công nghiệp": "htcn",
            "hệ thống công nghiệp": "htcn",
            
            # Chương trình tiên tiến Việt-Mỹ
            "cttt ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến kỹ thuật điện tử viễn thông": "tien_tien_dtvt",
            "cttt việt-mỹ ktđtvt": "tien_tien_dtvt",
            "chương trình tiên tiến ktđtvt": "tien_tien_dtvt",
            "tiên tiến điện tử viễn thông": "tien_tien_dtvt",
            "cttt đtvt": "tien_tien_dtvt",
            
            "cttt htn&iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "cttt việt-mỹ htn và iot": "tien_tien_nhung_iot",
            "chương trình tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "tiên tiến hệ thống nhúng": "tien_tien_nhung_iot",
            "cttt htn": "tien_tien_nhung_iot",
            "hệ thống nhúng và iot": "tien_tien_nhung_iot",
            "hệ thống nhúng": "tien_tien_nhung_iot",
            
            # Công nghệ thực phẩm
            "cntp": "cntp",
            "công nghệ thực phẩm": "cntp",
            "thực phẩm": "cntp",
            
            # Kiến trúc
            "kt": "kientruc",
            "kiến trúc": "kientruc",
            
            # Kỹ thuật xây dựng
            "ktxd xddd&cn": "xddc_cn",
            "kỹ thuật xây dựng dân dụng và công nghiệp": "xddc_cn",
            "ktxd chuyên ngành xddd&cn": "xddc_cn",
            "xây dựng dân dụng và công nghiệp": "xddc_cn",
            "xd dân dụng": "xddc_cn",
            "xd công nghiệp": "xddc_cn",
            "kỹ thuật xây dựng dân dụng": "xddc_cn",
            
            "ktxd thxd": "thxd",
            "kỹ thuật xây dựng tin học xây dựng": "thxd",
            "ktxd chuyên ngành thxd": "thxd",
            "tin học xây dựng": "thxd",
            "thxd": "thxd",
            
            "ktxd đttm": "xdtttm",
            "kỹ thuật xây dựng đô thị thông minh": "xdtttm",
            "ktxd qlxd đttm": "xdtttm",
            "kỹ thuật và quản lý xây dựng đô thị thông minh": "xdtttm",
            "xây dựng đô thị thông minh": "xdtttm",
            "đô thị thông minh": "xdtttm",
            
            "ktxd mhtt&ttnt": "bim_ai",
            "kỹ thuật xây dựng mô hình thông tin và ttnt": "bim_ai",
            "ktxd chuyên ngành mhtt và ttnt": "bim_ai",
            "kỹ thuật xây dựng mhtt và ttnt": "bim_ai",
            "mô hình thông tin trong xây dựng": "bim_ai",
            "mhtt và ttnt trong xây dựng": "bim_ai",
            "trí tuệ nhân tạo trong xây dựng": "bim_ai",
            
            # Kỹ thuật xây dựng công trình thủy
            "ktxdctt": "ctthuy",
            "kỹ thuật xây dựng công trình thủy": "ctthuy",
            "xây dựng công trình thủy": "ctthuy",
            "công trình thủy": "ctthuy",
            
            # Kỹ thuật xây dựng công trình giao thông
            "ktxdctgt": "ctgt",
            "kỹ thuật xây dựng công trình giao thông": "ctgt",
            "xây dựng công trình giao thông": "ctgt",
            "công trình giao thông": "ctgt",
            "cầu đường": "ctgt",
            
            "ktxdctgt đstđc": "duongsat",
            "xây dựng đường sắt tốc độ cao": "duongsat",
            "ktxdctgt chuyên ngành đstđc": "duongsat",
            "xây dựng đường sắt đô thị": "duongsat",
            "đường sắt tốc độ cao": "duongsat",
            "đường sắt đô thị": "duongsat",
            
            # Kinh tế xây dựng
            "ktxd": "ktxd",
            "kinh tế xây dựng": "ktxd",
            
            # Kỹ thuật cơ sở hạ tầng
            "ktcsht": "cshatng",
            "kỹ thuật cơ sở hạ tầng": "cshatng",
            "cơ sở hạ tầng": "cshatng",
            "hạ tầng": "cshatng",
            
            # Quản lý tài nguyên và môi trường
            "qltn&mt": "qltn_mt",
            "quản lý tài nguyên và môi trường": "qltn_mt",
            "qltnmt": "qltn_mt",
            "tài nguyên và môi trường": "qltn_mt",
            "tài nguyên môi trường": "qltn_mt",

            "ô tô": "oto",
            "kỹ thuật ô tô": "oto",
        }

        # Danh sách các từ khóa quan trọng để xác định ngành chính xác
        major_keywords = {
            "cntt": ["công nghệ thông tin", "cntt"],
            "ktmt": ["kỹ thuật máy tính", "ktmt"],
            "cnsh": ["công nghệ sinh học", "cnsh"],
            "vlxd": ["vật liệu xây dựng", "vlxd"],
            "ctm": ["chế tạo máy", "ctm"],
            "qlcn": ["quản lý công nghiệp", "qlcn"],
            "dầu khí": ["dầu khí", "khai thác dầu"],
            "pfiev": ["pfiev", "việt pháp"],
            "cơ khí": ["cơ khí", "ckhk", "ckđl"],
            "cơ điện tử": ["cơ điện tử", "cđt"],
            "nhiệt": ["nhiệt", "năng lượng"],
            "tàu thủy": ["tàu thủy"],
            "điện": ["điện", "ktđ"],
            "điện tử": ["điện tử", "viễn thông", "đtvt"],
            "tự động hóa": ["tự động hóa", "điều khiển"],
            "hóa học": ["hóa học"],
            "môi trường": ["môi trường"],
            "hệ thống": ["hệ thống công nghiệp"],
            "tiên tiến": ["tiên tiến", "việt-mỹ", "cttt"],
            "nhúng": ["nhúng", "iot"],
            "thực phẩm": ["thực phẩm", "cntp"],
            "kiến trúc": ["kiến trúc"],
            "xây dựng": ["xây dựng", "ktxd", "xd"],
            "dân dụng": ["dân dụng", "công nghiệp"],
            "tin học xây dựng": ["tin học xây dựng"],
            "đô thị thông minh": ["đô thị thông minh"],
            "công trình thủy": ["công trình thủy"],
            "giao thông": ["giao thông", "cầu đường"],
            "đường sắt": ["đường sắt"],
            "kinh tế xây dựng": ["kinh tế xây dựng"],
            "hạ tầng": ["hạ tầng", "csht"],
            "tài nguyên": ["tài nguyên", "tnmt"],
            "ô tô": ["ô tô", "xe hơi"],
        }

        def clean_text(text):
            # Làm sạch văn bản và xóa các ký tự đặc biệt
            import re
            text = text.lower().strip()
            text = re.sub(r'[^\w\s&-]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text

        def normalize_major(text: Optional[str]) -> Optional[str]:
            if not text:
                return None
                
            # Làm sạch và chuẩn hóa văn bản đầu vào
            normalized_text = clean_text(text)
            
            # Thử tìm kiếm trực tiếp trong mapping
            if normalized_text in major_mapping:
                return major_mapping[normalized_text]
            
            # Giải quyết các trường hợp đặc biệt
            if normalized_text == "ktxd":
                # Nếu chỉ có "ktxd" thì mặc định là "Kinh tế xây dựng"
                return "ktxd"
            
            if normalized_text == "ktmt":
                # Nếu chỉ có "ktmt" có thể là "Kỹ thuật máy tính" hoặc "Kỹ thuật môi trường"
                # Mặc định là "Kỹ thuật máy tính"
                if "môi trường" in normalized_text:
                    return "mt"
                return "ktmt"
            
            # Tìm kiếm dựa trên từng từ khóa trong text và tính điểm khớp
            match_scores = {}
            for key, value in major_mapping.items():
                # Tính điểm dựa trên có bao nhiêu từ của key có trong text
                key_words = key.split()
                score = sum(1 for word in key_words if word in normalized_text)
                
                # Cộng điểm nếu có từ khóa đặc biệt
                for kw_group, keywords in major_keywords.items():
                    if any(kw in key for kw in keywords) and any(kw in normalized_text for kw in keywords):
                        score += 2
                
                # Cộng điểm nếu key là một phần của text
                if key in normalized_text:
                    score += 3
                    
                # Lưu điểm và tên ngành đầy đủ
                if score > 0:
                    match_scores[value] = match_scores.get(value, 0) + score
            
            # Trả về kết quả có điểm cao nhất nếu có
            if match_scores:
                return max(match_scores.items(), key=lambda x: x[1])[0]
                    
            # Nếu không tìm thấy từ khóa, tìm kiếm keyword có trong text
            for key, value in major_mapping.items():
                if key in normalized_text:
                    return value
                    
            return None

        def normalize_method(text: Optional[str]) -> Optional[str]:
            """
            Cải thiện xác định phương thức xét tuyển từ văn bản nhập vào.
            """
            if not text:
                return None
                
            # Làm sạch và chuẩn hóa văn bản
            text = clean_text(text)
            
            # Tạo từ điển phụ cho các biến thể cách viết phương thức xét tuyển
            method_variants = {
                "tn_thpt": ["thi thpt", "điểm thi", "tốt nghiệp thpt", "thpt", "tn", "tốt nghiệp trung học phổ thông"],
                "dgnl": ["năng lực", "dgnl", "đgnl", "vact", "apt", "bài test năng lực"],
                "dgtd": ["tư duy", "dgtd", "tsa", "bài test tư duy"],
                "hb_thpt": ["học bạ", "xét học bạ", "điểm học bạ", "tbhb", "xhb", "học bạ thpt"],
                "xtr": ["tuyển riêng", "xét riêng", "riêng", "phỏng vấn"]
            }
            
            # Thử chính xác từng từ khóa trong method_mapping
            for key, value in method_mapping.items():
                if key == text:  # Khớp chính xác
                    return value
                elif key in text:  # Khớp một phần
                    # Kiểm tra nếu key là một từ hoàn chỉnh trong text
                    words = text.split()
                    if key in words:
                        return value
            
            # Sử dụng từ điển phụ để tìm kiếm khi không có kết quả trực tiếp
            best_match = None
            max_score = 0
            
            for method_name, variants in method_variants.items():
                # Tính điểm cho mỗi phương thức dựa vào sự xuất hiện của các biến thể
                score = 0
                for variant in variants:
                    if variant in text:
                        # Từ khóa hoàn chỉnh có điểm cao hơn
                        if variant in text.split():
                            score += 2
                        else:
                            score += 1
                        
                # Lưu kết quả có điểm cao nhất
                if score > max_score:
                    max_score = score
                    # Tìm giá trị tương ứng trong method_mapping
                    best_match = next((v for k, v in method_mapping.items() if method_name.startswith(v)), method_name)
                    
            # Trả về kết quả tốt nhất nếu có
            if best_match and max_score > 0:
                return best_match
                
            return None

        # Lấy dữ liệu từ tracker
        major_input = tracker.get_slot("major")
        method_input = tracker.get_slot("method")
        
        # Chuẩn hóa dữ liệu
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