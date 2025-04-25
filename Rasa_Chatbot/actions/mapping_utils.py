from typing import Optional
import re

# Dictionary ánh xạ các phương thức xét tuyển
METHOD_MAPPING = {
    "riêng": "xtr",
    "xét tuyển riêng": "xtr",
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
    "học bạ": "hb_thpt",
    "học bạ thpt": "hb_thpt",
    "tuyển thẳng": "xtt",
    "xtt": "xtt",
    "xét tuyển thẳng": "xtt",
}

# Từ điển phụ cho các biến thể cách viết phương thức xét tuyển
METHOD_VARIANTS = {
    "tn_thpt": ["thi thpt", "điểm thi", "tốt nghiệp thpt", "thpt", "tn", "tốt nghiệp trung học phổ thông"],
    "dgnl": ["năng lực", "dgnl", "đgnl", "vact", "apt", "bài test năng lực"],
    "dgtd": ["tư duy", "dgtd", "tsa", "bài test tư duy"],
    "hb_thpt": ["học bạ", "xét học bạ", "điểm học bạ", "tbhb", "xhb", "học bạ thpt"],
    "xtr": ["tuyển riêng", "xét riêng", "riêng", "phỏng vấn"]
}

# Dictionary ánh xạ tên ngành
MAJOR_MAPPING = {
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
    "công nghệ thông tin ngoại ngữ": "cntt_nnn",
    "cntt ngoại ngữ": "cntt_nnn",
    
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
MAJOR_KEYWORDS = {
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
    "thực phẩm": ["thực phẩm", "cntp", "công nghệ thực phẩm"],
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
    """
    Làm sạch văn bản và xóa các ký tự đặc biệt
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s&-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def normalize_major(text: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa và ánh xạ tên ngành từ văn bản đầu vào
    """
    if not text:
        return None
            
    # Làm sạch và chuẩn hóa văn bản đầu vào
    normalized_text = clean_text(text)
    
    # Thử tìm kiếm trực tiếp trong mapping
    if normalized_text in MAJOR_MAPPING:
        return MAJOR_MAPPING[normalized_text]
    
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
    for key, value in MAJOR_MAPPING.items():
        # Tính điểm dựa trên có bao nhiêu từ của key có trong text
        key_words = key.split()
        score = sum(1 for word in key_words if word in normalized_text)
        
        # Cộng điểm nếu có từ khóa đặc biệt
        for kw_group, keywords in MAJOR_KEYWORDS.items():
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
    for key, value in MAJOR_MAPPING.items():
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
    
    # Thử chính xác từng từ khóa trong METHOD_MAPPING
    for key, value in METHOD_MAPPING.items():
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
    
    for method_name, variants in METHOD_VARIANTS.items():
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
            # Tìm giá trị tương ứng trong METHOD_MAPPING
            best_match = next((v for k, v in METHOD_MAPPING.items() if method_name.startswith(v)), method_name)
            
    # Trả về kết quả tốt nhất nếu có
    if best_match and max_score > 0:
        return best_match
        
    return None