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

ACHIEVEMENT_FIELD_MAPPING = {
    # Khoa học cơ bản
    "toán": "toán",
    "toán học": "toán",
    "giải toán": "toán",
    "olympic toán": "toán",
    
    "lý": "vật lý",
    "vật lý": "vật lý",
    "vật lí": "vật lý",
    "giải vật lý": "vật lý",
    "olympic vật lý": "vật lý",
    
    "hóa": "hóa học",
    "hóa học": "hóa học",
    "giải hóa": "hóa học",
    "olympic hóa": "hóa học",
    
    "sinh": "sinh học",
    "sinh học": "sinh học",
    "giải sinh": "sinh học",
    "olympic sinh học": "sinh học",
    
    # Công nghệ thông tin
    "tin": "tin học",
    "tin học": "tin học",
    "giải tin": "tin học",
    "olympic tin học": "tin học",
    "lập trình": "tin học",
    "cntt": "tin học",
    "công nghệ thông tin": "tin học",
    
    "phần mềm": "phần mềm hệ thống",
    "phần mềm hệ thống": "phần mềm hệ thống",
    "hệ thống phần mềm": "phần mềm hệ thống",
    "software": "phần mềm hệ thống",
    "system software": "phần mềm hệ thống",
    
    # Hệ thống nhúng và robot
    "robot": "robot và máy thông minh",
    "robot và máy thông minh": "robot và máy thông minh",
    "máy thông minh": "robot và máy thông minh",
    "robotics": "robot và máy thông minh",
    
    "hệ thống nhúng": "hệ thống nhúng",
    "nhúng": "hệ thống nhúng",
    "embedded": "hệ thống nhúng",
    "iot": "hệ thống nhúng",
    
    # Sinh học ứng dụng
    "vi sinh": "vi sinh vật",
    "vi sinh vật": "vi sinh vật",
    
    "hóa sinh": "hóa sinh",
    "sinh hóa": "hóa sinh",
    
    "kỹ thuật y sinh": "kỹ thuật y sinh",
    "y sinh": "kỹ thuật y sinh",
    
    "sinh học tế bào": "sinh học tế bào và phân tử",
    "sinh học phân tử": "sinh học tế bào và phân tử",
    "sinh học tế bào và phân tử": "sinh học tế bào và phân tử",
    "tế bào học": "sinh học tế bào và phân tử",
    
    "y sinh và khoa học sức khỏe": "y sinh và khoa học sức khỏe",
    "khoa học sức khỏe": "y sinh và khoa học sức khỏe",
    
    # Vật liệu và Điện tử
    "khoa học vật liệu": "khoa học vật liệu",
    "vật liệu": "khoa học vật liệu",
    "hoá học, khoa học vật liệu": "khoa học vật liệu",
    
    "thông tin-điện tử-viễn thông": "thông tin điện tử viễn thông",
    "điện tử viễn thông": "thông tin điện tử viễn thông",
    "thông tin viễn thông": "thông tin điện tử viễn thông",
    "đtvt": "thông tin điện tử viễn thông",
    "viễn thông": "thông tin điện tử viễn thông",
    "điện tử": "thông tin điện tử viễn thông",
    
    # Cơ khí
    "cơ khí": "kỹ thuật cơ khí",
    "kỹ thuật cơ khí": "kỹ thuật cơ khí",
    
    # Môi trường
    "khoa học trái đất": "khoa học trái đất và môi trường",
    "khoa học trái đất và môi trường": "khoa học trái đất và môi trường",
    "địa chất": "khoa học trái đất và môi trường",
    
    "môi trường": "tài nguyên và môi trường",
    "tài nguyên": "tài nguyên và môi trường",
    "tài nguyên & môi trường": "tài nguyên và môi trường",
    "tài nguyên và môi trường": "tài nguyên và môi trường",
}


# Từ điển phụ cho các biến thể cách viết thành tích
ACHIEVEMENT_VARIANTS = {
    "toán": ["toán", "toán học", "giải toán", "olympic toán", "hsg toán", "học sinh giỏi toán"],
    "vật lý": ["lý", "vật lý", "vật lí", "giải lý", "olympic vật lý", "hsg vật lý", "học sinh giỏi vật lý"],
    "hóa học": ["hóa", "hóa học", "giải hóa", "olympic hóa học", "hsg hóa", "học sinh giỏi hóa"],
    "sinh học": ["sinh", "sinh học", "giải sinh", "olympic sinh học", "hsg sinh", "học sinh giỏi sinh"],
    "tin học": ["tin", "tin học", "giải tin", "olympic tin học", "lập trình", "công nghệ thông tin"],
    "phần mềm hệ thống": ["phần mềm", "phần mềm hệ thống", "hệ thống phần mềm", "software"],
    "robot và máy thông minh": ["robot", "robotics", "máy thông minh", "robot và máy thông minh"],
    "hệ thống nhúng": ["hệ thống nhúng", "nhúng", "embedded", "iot", "internet of things"],
    "vi sinh vật": ["vi sinh", "vi sinh vật", "vi trùng học"],
    "hóa sinh": ["hóa sinh", "sinh hóa", "biochemistry"],
    "kỹ thuật y sinh": ["kỹ thuật y sinh", "y sinh", "biomedical", "bioengineering"],
    "sinh học tế bào và phân tử": ["sinh học tế bào", "sinh học phân tử", "sinh học tế bào và phân tử", "molecular biology", "cell biology"],
    "y sinh và khoa học sức khỏe": ["y sinh và khoa học sức khỏe", "khoa học sức khỏe", "health science"],
    "khoa học vật liệu": ["khoa học vật liệu", "vật liệu", "materials science"],
    "thông tin điện tử viễn thông": ["thông tin-điện tử-viễn thông", "điện tử viễn thông", "viễn thông", "điện tử", "telecommunications"],
    "kỹ thuật cơ khí": ["cơ khí", "kỹ thuật cơ khí", "mechanical engineering"],
    "khoa học trái đất và môi trường": ["khoa học trái đất", "khoa học trái đất và môi trường", "địa chất", "earth science"],
    "tài nguyên và môi trường": ["môi trường", "tài nguyên", "tài nguyên & môi trường", "tài nguyên và môi trường", "environmental science"]
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

def normalize_achievement_field(text: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa và ánh xạ tên lĩnh vực giải thưởng/thành tích từ văn bản đầu vào
    """
    if not text:
        return None
            
    # Làm sạch và chuẩn hóa văn bản đầu vào
    normalized_text = clean_text(text)
    
    # Thử tìm kiếm trực tiếp trong mapping
    if normalized_text in ACHIEVEMENT_FIELD_MAPPING:
        return ACHIEVEMENT_FIELD_MAPPING[normalized_text]
    
    # Tìm kiếm dựa trên từng từ khóa trong text và tính điểm khớp
    match_scores = {}
    for key, value in ACHIEVEMENT_FIELD_MAPPING.items():
        # Tính điểm dựa trên có bao nhiêu từ của key có trong text
        key_words = key.split()
        score = sum(1 for word in key_words if word in normalized_text)
        
        # Cộng điểm nếu có từ khóa đặc biệt từ variants
        for field_id, keywords in ACHIEVEMENT_VARIANTS.items():
            if value == field_id and any(kw in normalized_text for kw in keywords):
                score += 2
        
        # Cộng điểm nếu key là một phần của text
        if key in normalized_text:
            score += 3
            
        # Cộng điểm nếu là từ khóa chính xác
        if key == normalized_text:
            score += 5
            
        # Lưu điểm và tên lĩnh vực
        if score > 0:
            match_scores[value] = match_scores.get(value, 0) + score
    
    # Trả về kết quả có điểm cao nhất nếu có
    if match_scores:
        return max(match_scores.items(), key=lambda x: x[1])[0]
    
    return None

def find_achievement_fields(text: str) -> list:
    """
    Tìm tất cả các lĩnh vực thành tích có thể có trong một đoạn văn bản
    """
    if not text:
        return []
    
    normalized_text = clean_text(text)
    found_fields = []
    
    # Kiểm tra tất cả các từ khóa trong từ điển
    for key, value in ACHIEVEMENT_FIELD_MAPPING.items():
        if key in normalized_text and value not in found_fields:
            found_fields.append(value)
            
    # Kiểm tra các biến thể
    for field_id, variants in ACHIEVEMENT_VARIANTS.items():
        if field_id not in found_fields:  # Chỉ kiểm tra nếu chưa tìm thấy
            for variant in variants:
                if variant in normalized_text:
                    found_fields.append(field_id)
                    break
    
    return found_fields

# Dictionary ánh xạ tên môn học
SUBJECT_MAPPING = {
    # Toán học
    "toán": "toán",
    "toán học": "toán",
    "đại số": "toán",
    "hình học": "toán",
    "giải tích": "toán",
    "mathematics": "toán",
    "algebra": "toán",
    "geometry": "toán",
    "calculus": "toán",
    
    # Vật lý
    "lý": "vật lý",
    "vật lý": "vật lý",
    "vật lí": "vật lý",
    "physics": "vật lý",
    
    # Tiếng Anh
    "anh": "tiếng anh",
    "tiếng anh": "tiếng anh",
    "ta": "tiếng anh",
    "ngoại ngữ anh": "tiếng anh",
    "english": "tiếng anh",
    "foreign language english": "tiếng anh",
    
    # Tiếng Nhật
    "nhật": "tiếng nhật",
    "tiếng nhật": "tiếng nhật",
    "ngoại ngữ nhật": "tiếng nhật",
    "ngoại ngữ tiếng nhật": "tiếng nhật",
    "tiếng nhật bản": "tiếng nhật",
    "japanese": "tiếng nhật",
    
    # Hóa học
    "hóa": "hóa học",
    "hoá": "hóa học",
    "hóa học": "hóa học",
    "hoá học": "hóa học",
    "chemistry": "hóa học",
    
    # Sinh học
    "sinh": "sinh học",
    "sinh học": "sinh học",
    "sinh vật": "sinh học",
    "sinh vật học": "sinh học",
    "biology": "sinh học",
    
    # Lịch sử
    "sử": "lịch sử",
    "lịch sử": "lịch sử",
    "sử học": "lịch sử",
    "history": "lịch sử",
    
    # Địa lý
    "địa": "địa lý",
    "địa lý": "địa lý",
    "địa lí": "địa lý",
    "geography": "địa lý",
    "địa học": "địa lý",
    
    # Công nghệ
    "công nghệ": "công nghệ",
    "kĩ thuật công nghệ": "công nghệ",
    "kỹ thuật công nghệ": "công nghệ",
    "technology": "công nghệ",
    "tech": "công nghệ",
    
    # Tin học
    "tin": "tin học",
    "tin học": "tin học",
    "công nghệ thông tin": "tin học",
    "cntt": "tin học",
    "informatics": "tin học",
    "it": "tin học",
    "ict": "tin học",
    
    # Giáo dục kinh tế và pháp luật
    "gdkt": "giáo dục kinh tế và pháp luật",
    "gdpl": "giáo dục kinh tế và pháp luật",
    "gdktpl": "giáo dục kinh tế và pháp luật",
    "giáo dục kinh tế": "giáo dục kinh tế và pháp luật",
    "giáo dục pháp luật": "giáo dục kinh tế và pháp luật",
    "giáo dục kinh tế và pháp luật": "giáo dục kinh tế và pháp luật",
    "kinh tế và pháp luật": "giáo dục kinh tế và pháp luật",
    "economics and law": "giáo dục kinh tế và pháp luật",
    "kinh tế pháp luật": "giáo dục kinh tế và pháp luật",
    
    # Vẽ mỹ thuật
    "vẽ": "vẽ mỹ thuật",
    "mỹ thuật": "vẽ mỹ thuật",
    "vẽ mỹ thuật": "vẽ mỹ thuật",
    "hội họa": "vẽ mỹ thuật",
    "mĩ thuật": "vẽ mỹ thuật",
    "vẽ mĩ thuật": "vẽ mỹ thuật",
    "art": "vẽ mỹ thuật",
    "drawing": "vẽ mỹ thuật",
    "fine art": "vẽ mỹ thuật",
    
    # Ngữ văn
    "văn": "ngữ văn",
    "ngữ văn": "ngữ văn",
    "văn học": "ngữ văn",
    "văn học việt nam": "ngữ văn",
    "literature": "ngữ văn"
}

# Danh sách các từ khóa quan trọng để xác định môn học chính xác
SUBJECT_KEYWORDS = {
    "toán": ["toán", "đại số", "hình học", "giải tích", "number", "số học"],
    "vật lý": ["vật lý", "lý", "vật lí", "sức", "điện", "nhiệt", "cơ học"],
    "tiếng anh": ["anh", "tiếng anh", "english", "từ vựng", "ngữ pháp"],
    "tiếng nhật": ["nhật", "tiếng nhật", "kana", "kanji", "hiragana"],
    "hóa học": ["hóa", "hoá", "hóa học", "nguyên tố", "phân tử"],
    "sinh học": ["sinh", "sinh học", "tế bào", "di truyền", "thực vật"],
    "lịch sử": ["sử", "lịch sử", "thời kỳ", "triều đại", "thời đại"],
    "địa lý": ["địa", "địa lý", "bản đồ", "khí hậu", "dân số"],
    "công nghệ": ["công nghệ", "kỹ thuật", "thiết bị", "phương pháp"],
    "tin học": ["tin", "tin học", "máy tính", "lập trình", "phần mềm"],
    "giáo dục kinh tế và pháp luật": ["kinh tế", "pháp luật", "gdktpl", "gdkt", "gdpl", "luật"],
    "vẽ mỹ thuật": ["vẽ", "mỹ thuật", "hội họa", "màu sắc", "bố cục"],
    "ngữ văn": ["văn", "ngữ văn", "văn học", "tác phẩm", "tác giả"]
}

# Từ điển phụ cho các biến thể cách viết môn học
SUBJECT_VARIANTS = {
    "toán": ["toán", "toán học", "đại số", "hình học", "giải tích", "số học", "mathematics", "algebra", "calculus"],
    "vật lý": ["vật lý", "lý", "vật lí", "physics", "cơ học", "nhiệt học", "điện học", "quang học"],
    "tiếng anh": ["tiếng anh", "anh", "anh văn", "english", "foreign language", "ngoại ngữ anh"],
    "tiếng nhật": ["tiếng nhật", "nhật", "nhật ngữ", "japanese", "ngoại ngữ nhật"],
    "hóa học": ["hóa học", "hoá học", "hóa", "hoá", "chemistry", "nguyên tố hóa học"],
    "sinh học": ["sinh học", "sinh", "sinh vật", "biology", "thực vật học", "động vật học"],
    "lịch sử": ["lịch sử", "sử", "sử học", "history", "lịch sử thế giới", "lịch sử việt nam"],
    "địa lý": ["địa lý", "địa", "địa lí", "geography", "bản đồ học", "địa chất"],
    "công nghệ": ["công nghệ", "kĩ thuật công nghệ", "technology", "kĩ thuật", "kỹ thuật"],
    "tin học": ["tin học", "tin", "cntt", "informatics", "it", "công nghệ thông tin", "máy tính"],
    "giáo dục kinh tế và pháp luật": ["gdktpl", "gdkt", "gdpl", "kinh tế pháp luật", "giáo dục kinh tế", "giáo dục pháp luật"],
    "vẽ mỹ thuật": ["vẽ mỹ thuật", "mỹ thuật", "vẽ", "hội họa", "mĩ thuật", "vẽ mĩ thuật", "art"],
    "ngữ văn": ["ngữ văn", "văn", "văn học", "literature", "văn học việt nam", "văn học nước ngoài"]
}

def normalize_subject(text: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa và ánh xạ tên môn học từ văn bản đầu vào
    
    Args:
        text (str): Tên môn học cần chuẩn hóa
        
    Returns:
        str: Tên môn học đã chuẩn hóa (tiếng Việt) hoặc None nếu không nhận dạng được
    """
    if not text:
        return None
            
    # Làm sạch và chuẩn hóa văn bản đầu vào
    normalized_text = clean_text(text)
    
    # Thử tìm kiếm trực tiếp trong mapping
    if normalized_text in SUBJECT_MAPPING:
        return SUBJECT_MAPPING[normalized_text]
    
    # Tìm kiếm dựa trên từng từ khóa trong text và tính điểm khớp
    match_scores = {}
    for key, value in SUBJECT_MAPPING.items():
        # Tính điểm dựa trên có bao nhiêu từ của key có trong text
        key_words = key.split()
        score = sum(1 for word in key_words if word in normalized_text)
        
        # Cộng điểm nếu có từ khóa đặc biệt
        for subject_name, keywords in SUBJECT_KEYWORDS.items():
            if subject_name == value and any(kw in normalized_text for kw in keywords):
                score += 2
        
        # Cộng điểm nếu key là một phần của text
        if key in normalized_text:
            score += 3
            
        # Lưu điểm và tên môn học đầy đủ
        if score > 0:
            match_scores[value] = match_scores.get(value, 0) + score
    
    # Trả về kết quả có điểm cao nhất nếu có
    if match_scores:
        return max(match_scores.items(), key=lambda x: x[1])[0]
    
    # Thử tìm kiếm trong danh sách các biến thể
    for subject, variants in SUBJECT_VARIANTS.items():
        for variant in variants:
            if variant in normalized_text:
                return subject
            
    return None

def find_subjects_in_text(text: str) -> list:
    """
    Tìm tất cả các môn học có thể có trong một đoạn văn bản
    
    Args:
        text (str): Đoạn văn bản cần tìm kiếm
        
    Returns:
        list: Danh sách các môn học tìm thấy (đã chuẩn hóa)
    """
    if not text:
        return []
    
    normalized_text = clean_text(text)
    found_subjects = []
    
    # Kiểm tra các từ khóa chính xác
    for key, value in SUBJECT_MAPPING.items():
        if key in normalized_text and value not in found_subjects:
            found_subjects.append(value)
    
    # Kiểm tra các từ khóa đặc biệt
    for subject_name, keywords in SUBJECT_KEYWORDS.items():
        if subject_name not in found_subjects:
            for keyword in keywords:
                if keyword in normalized_text:
                    found_subjects.append(subject_name)
                    break
    
    return found_subjects

# Dictionary ánh xạ tên khoa
FACULTY_MAPPING = {
    # Công nghệ Nhiệt - Điện lạnh
    "nhiệt": "104",
    "công nghệ nhiệt": "104",
    "công nghệ nhiệt điện lạnh": "104",
    "điện lạnh": "104",
    "nhiệt lạnh": "104",
    "kỹ thuật nhiệt": "104",
    
    # Điện
    "điện": "105",
    "khoa điện": "105",
    "kỹ thuật điện": "105",
    "hệ thống điện": "105",
    
    # Môi trường
    "môi trường": "117",
    "khoa môi trường": "117",
    "kỹ thuật môi trường": "117",
    "công nghệ môi trường": "117",
    
    # Kiến trúc
    "kiến trúc": "121",
    "khoa kiến trúc": "121",
    "kt": "121",
    "kts": "121",
    "thiết kế kiến trúc": "121",
    
    # Xây dựng Dân dụng và Công nghiệp
    "xây dựng dân dụng và công nghiệp": "110",
    "xd dân dụng": "110",
    "xd công nghiệp": "110",
    "xddd&cn": "110",
    "xd dd&cn": "110",
    "dân dụng": "110",
    "xây dựng dân dụng": "110",
    "dd&cn": "110",
    
    # Xây dựng Công trình thủy
    "xây dựng công trình thủy": "111",
    "công trình thủy": "111",
    "xây dựng thủy": "111",
    "ctt": "111",
    "xdctt": "111",
    "thủy lợi": "111",
    
    # Công nghệ thông tin
    "công nghệ thông tin": "102",
    "cntt": "102",
    "it": "102",
    "tin học": "102",
    "khoa công nghệ thông tin": "102",
    
    # Điện tử viễn thông
    "điện tử viễn thông": "106",
    "đtvt": "106",
    "điện tử": "106",
    "viễn thông": "106",
    "khoa điện tử": "106",
    "kỹ thuật điện tử": "106",
    "kỹ thuật điện tử viễn thông": "106",
    
    # Hóa
    "hóa": "107",
    "khoa hóa": "107",
    "hóa học": "107",
    "kỹ thuật hóa học": "107",
    "công nghệ hóa": "107",
    
    # Xây dựng cầu đường
    "xây dựng cầu đường": "109",
    "cầu đường": "109",
    "xdcđ": "109",
    "công trình giao thông": "109",
    "đường bộ": "109",
    "xây dựng giao thông": "109",
    
    # Cơ khí
    "cơ khí": "101",
    "khoa cơ khí": "101",
    "chế tạo máy": "101",
    "kỹ thuật cơ khí": "101",
    "cơ điện tử": "101",
    
    # Quản lý dự án
    "quản lý dự án": "118",
    "qldự án": "118",
    "qlda": "118",
    "quản lý xây dựng": "118",
    "quản lý": "118",
    "dự án": "118",
    
    # Khoa học Công nghệ tiên tiến
    "khoa học công nghệ tiên tiến": "123",
    "công nghệ tiên tiến": "123",
    "khcn tiên tiến": "123",
    "tiên tiến": "123",
    "khoa học tiên tiến": "123",
    
    # Cơ khí Giao thông
    "cơ khí giao thông": "103",
    "ckgt": "103",
    "kỹ thuật ô tô": "103",
    "cơ khí động lực": "103",
    "ô tô": "103",
    "kỹ thuật tàu thủy": "103"
}

# Danh sách các từ khóa quan trọng để xác định khoa chính xác
FACULTY_KEYWORDS = {
    "104": ["nhiệt", "điện lạnh", "lạnh", "công nghệ nhiệt", "kỹ thuật nhiệt"],
    "105": ["điện", "kỹ thuật điện", "hệ thống điện", "tự động hóa"],
    "117": ["môi trường", "kỹ thuật môi trường", "tài nguyên"],
    "121": ["kiến trúc", "thiết kế", "kts", "kiến trúc sư"],
    "110": ["xây dựng dân dụng", "dân dụng", "công nghiệp", "xd", "dd&cn"],
    "111": ["công trình thủy", "thủy", "thủy lợi", "đập", "hồ chứa"],
    "102": ["công nghệ thông tin", "cntt", "lập trình", "phần mềm", "it"],
    "106": ["điện tử", "viễn thông", "đtvt", "truyền thông", "kỹ thuật điện tử"],
    "107": ["hóa", "hóa học", "công nghệ hóa", "vật liệu"],
    "109": ["cầu đường", "giao thông", "xây dựng cầu", "đường bộ"],
    "101": ["cơ khí", "chế tạo máy", "cơ điện tử", "kỹ thuật cơ khí"],
    "118": ["quản lý dự án", "dự án", "quản lý xây dựng", "qlda"],
    "123": ["tiên tiến", "công nghệ tiên tiến", "khoa học tiên tiến"],
    "103": ["cơ khí giao thông", "ô tô", "tàu thủy", "động lực", "ckgt"]
}

# Từ điển phụ cho các biến thể cách viết khoa
FACULTY_VARIANTS = {
    "104": ["nhiệt", "điện lạnh", "công nghệ nhiệt - điện lạnh", "kỹ thuật nhiệt lạnh"],
    "105": ["điện", "kỹ thuật điện", "khoa điện", "điện năng"],
    "117": ["môi trường", "khoa môi trường", "kỹ thuật môi trường", "tài nguyên và môi trường"],
    "121": ["kiến trúc", "khoa kiến trúc", "thiết kế kiến trúc", "kt"],
    "110": ["xây dựng dân dụng và công nghiệp", "xddd&cn", "dân dụng và công nghiệp", "dd&cn"],
    "111": ["xây dựng công trình thủy", "công trình thủy", "thủy lợi công trình", "xdctt"],
    "102": ["công nghệ thông tin", "cntt", "tin học", "khoa cntt", "it"],
    "106": ["điện tử viễn thông", "đtvt", "truyền thông", "kỹ thuật điện tử viễn thông"],
    "107": ["hóa", "khoa hóa", "khoa hóa học", "kỹ thuật hóa học", "công nghệ hóa"],
    "109": ["xây dựng cầu đường", "cầu đường", "xdcđ", "công trình giao thông", "kỹ thuật cầu đường"],
    "101": ["cơ khí", "khoa cơ khí", "kỹ thuật cơ khí", "chế tạo máy", "cơ học"],
    "118": ["quản lý dự án", "qlda", "quản lý công trình", "quản lý xây dựng"],
    "123": ["khoa học công nghệ tiên tiến", "tiên tiến", "công nghệ tiên tiến", "khcn tiên tiến"],
    "103": ["cơ khí giao thông", "ckgt", "kỹ thuật ô tô", "kỹ thuật tàu thủy", "động lực học"]
}

def normalize_faculty(text: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa và ánh xạ tên khoa từ văn bản đầu vào
    
    Args:
        text (str): Tên khoa cần chuẩn hóa
        
    Returns:
        str: ID hoặc tên khoa đã chuẩn hóa hoặc None nếu không nhận dạng được
    """
    if not text:
        return None
            
    # Làm sạch và chuẩn hóa văn bản đầu vào
    normalized_text = clean_text(text)
    
    # Thử tìm kiếm trực tiếp trong mapping
    if normalized_text in FACULTY_MAPPING:
        return FACULTY_MAPPING[normalized_text]
    
    # Tìm kiếm dựa trên từng từ khóa trong text và tính điểm khớp
    match_scores = {}
    for key, value in FACULTY_MAPPING.items():
        # Tính điểm dựa trên có bao nhiêu từ của key có trong text
        key_words = key.split()
        score = sum(1 for word in key_words if word in normalized_text)
        
        # Cộng điểm nếu có từ khóa đặc biệt
        for faculty_id, keywords in FACULTY_KEYWORDS.items():
            if faculty_id == value and any(kw in normalized_text for kw in keywords):
                score += 2
        
        # Cộng điểm nếu key là một phần của text
        if key in normalized_text:
            score += 3
            
        # Lưu điểm và ID khoa
        if score > 0:
            match_scores[value] = match_scores.get(value, 0) + score
    
    # Trả về kết quả có điểm cao nhất nếu có
    if match_scores:
        return max(match_scores.items(), key=lambda x: x[1])[0]
    
    # Thử tìm kiếm trong danh sách các biến thể
    for faculty_id, variants in FACULTY_VARIANTS.items():
        for variant in variants:
            if variant in normalized_text:
                return faculty_id
            
    return None

def find_faculties_in_text(text: str) -> list:
    """
    Tìm tất cả các khoa có thể có trong một đoạn văn bản
    
    Args:
        text (str): Đoạn văn bản cần tìm kiếm
        
    Returns:
        list: Danh sách các ID khoa tìm thấy
    """
    if not text:
        return []
    
    normalized_text = clean_text(text)
    found_faculties = []
    
    # Kiểm tra các từ khóa chính xác
    for key, value in FACULTY_MAPPING.items():
        if key in normalized_text and value not in found_faculties:
            found_faculties.append(value)
    
    # Kiểm tra các từ khóa đặc biệt
    for faculty_id, keywords in FACULTY_KEYWORDS.items():
        if faculty_id not in found_faculties:
            for keyword in keywords:
                if keyword in normalized_text:
                    found_faculties.append(faculty_id)
                    break
    
    return found_faculties