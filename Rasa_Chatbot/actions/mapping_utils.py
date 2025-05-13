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

# Mapping sở thích và điểm mạnh với ngành học
STUDENT_STRENGTH_MAPPING = {
    # Sở thích về máy tính, công nghệ
    "lập trình": ["cntt_htdn", "cntt_ai", "cntt_nnn", "ktmt"],
    "máy tính": ["cntt_htdn", "cntt_ai", "cntt_nnn", "ktmt"],
    "phần mềm": ["cntt_htdn", "cntt_ai", "cntt_nnn"],
    "thiết kế web": ["cntt_htdn", "cntt_nnn"],
    "thiết kế app": ["cntt_htdn", "cntt_nnn"],
    "game": ["cntt_htdn", "cntt_ai"],
    "trí tuệ nhân tạo": ["cntt_ai"],
    "ai": ["cntt_ai"],
    "dữ liệu": ["cntt_ai"],
    "phân tích dữ liệu": ["cntt_ai"],
    "data": ["cntt_ai"],
    "công nghệ": ["cntt_htdn", "ktmt", "dtvt", "vidientu_vimach", "tien_tien_dtvt", "tien_tien_nhung_iot"],
    
    # Sở thích về khoa học tự nhiên
    "vật lý": ["ktmt", "ck_dongluc", "ck_hk", "cdt", "ktnhiet", "ktdien", "dtvt", "vidientu_vimach", "tudonghoa"],
    "toán học": ["cntt_ai", "ktmt", "ktdien", "dtvt", "tudonghoa"],
    "hóa học": ["cnsinhhoc", "cnsinhhoc_yd", "vlxd", "daukhi", "kthh", "mt", "cntp"],
    "sinh học": ["cnsinhhoc", "cnsinhhoc_yd", "mt", "cntp"],
    
    # Sở thích về kỹ thuật, cơ khí
    "cơ khí": ["ck_dongluc", "ck_hk", "cdt", "ctm", "oto"],
    "động cơ": ["ck_dongluc", "ckgt", "oto"],
    "chế tạo": ["ctm", "cdt"],
    "ô tô": ["oto", "ck_dongluc"],
    "xe hơi": ["oto", "ck_dongluc"],
    "máy móc": ["ctm", "ck_dongluc", "ck_hk", "cdt"],
    "robot": ["cdt", "tudonghoa", "tien_tien_nhung_iot"],
    "tự động hóa": ["tudonghoa", "cdt", "ktdien"],
    "điện": ["ktdien", "tudonghoa"],
    "điện tử": ["dtvt", "vidientu_vimach", "tudonghoa", "tien_tien_dtvt"],
    "vi mạch": ["vidientu_vimach", "tien_tien_dtvt"],
    
    # Sở thích về xây dựng, kiến trúc
    "xây dựng": ["xddc_cn", "thxd", "xdtttm", "bim_ai", "ctthuy", "ctgt", "duongsat", "ktxd", "cshatng"],
    "kiến trúc": ["kientruc", "xddc_cn", "thxd"],
    "thiết kế nhà": ["kientruc", "xddc_cn"],
    "cầu đường": ["ctgt", "duongsat"],
    "công trình": ["xddc_cn", "ctthuy", "ctgt", "duongsat", "ktxd", "cshatng"],
    "đô thị": ["xdtttm", "ktxd"],
    "hạ tầng": ["cshatng", "xddc_cn", "ctgt", "xdtttm"],
    "bim": ["bim_ai", "thxd"],
    
    # Sở thích về môi trường, năng lượng
    "môi trường": ["mt", "qltn_mt", "cnsinhhoc"],
    "năng lượng": ["ktnqlnl", "ktnhiet"],
    "tài nguyên": ["qltn_mt", "mt"],
    "nhiệt": ["ktnhiet", "ktnqlnl"],
    "điện lạnh": ["ktnhiet"],
    
    # Sở thích về hóa học, vật liệu
    "vật liệu": ["vlxd", "kthh"],
    "dầu khí": ["daukhi"],
    "hóa dầu": ["daukhi", "kthh"],
    
    # Sở thích về thực phẩm
    "thực phẩm": ["cntp", "cnsinhhoc"],
    "chế biến": ["cntp"],
    "dinh dưỡng": ["cntp", "cnsinhhoc_yd"],
    
    # Sở thích về sinh học, y dược
    "y dược": ["cnsinhhoc_yd"],
    "dược phẩm": ["cnsinhhoc_yd", "kthh"],
    "công nghệ sinh học": ["cnsinhhoc", "cnsinhhoc_yd"],
    
    # Sở thích về quản lý
    "quản lý": ["qlcn", "ktxd", "qltn_mt"],
    "kinh tế": ["ktxd", "qlcn"],
    "tổ chức": ["qlcn", "ktxd"],
    "công nghiệp": ["qlcn", "htcn"],
    
    # Sở thích về biển, tàu thuyền
    "tàu thủy": ["tauthuy"],
    "biển": ["tauthuy", "ctthuy"],
    "đóng tàu": ["tauthuy"],
    
    # Sở thích về ngoại ngữ
    "tiếng nhật": ["cntt_nnn"],
    "nhật bản": ["cntt_nnn"],
    "ngoại ngữ": ["cntt_nnn"],
    
    # Sở thích về tiên tiến
    "quốc tế": ["pfiev", "tien_tien_dtvt", "tien_tien_nhung_iot"],
    "tiên tiến": ["pfiev", "tien_tien_dtvt", "tien_tien_nhung_iot"],
    "việt pháp": ["pfiev"],
    "pháp": ["pfiev"],
    "việt mỹ": ["tien_tien_dtvt", "tien_tien_nhung_iot"],
    "mỹ": ["tien_tien_dtvt", "tien_tien_nhung_iot"],
    
    # Điểm mạnh theo môn học
    "giỏi toán": ["cntt_ai", "cntt_htdn", "ktmt", "tudonghoa", "dtvt", "ktdien"],
    "giỏi lý": ["ck_dongluc", "dtvt", "ktmt", "ktdien", "tauthuy", "cdt", "ktnhiet"],
    "giỏi hóa": ["cnsinhhoc", "cnsinhhoc_yd", "kthh", "daukhi", "mt"],
    "giỏi sinh": ["cnsinhhoc", "cnsinhhoc_yd", "mt"],
    "giỏi tin": ["cntt_htdn", "cntt_ai", "cntt_nnn", "ktmt", "thxd", "bim_ai"],
    "giỏi anh": ["cntt_nnn", "tien_tien_dtvt", "tien_tien_nhung_iot", "pfiev"],
    "giỏi vẽ": ["kientruc", "thxd", "xddc_cn"],
    
    # Điểm mạnh về kỹ năng
    "tư duy logic": ["cntt_htdn", "cntt_ai", "ktmt", "tudonghoa", "dtvt"],
    "tư duy sáng tạo": ["kientruc", "cntt_htdn", "cdt", "cntt_ai"],
    "thích giải quyết vấn đề": ["cntt_ai", "cntt_htdn", "ktmt", "qlcn", "htcn"],
    "thích thực hành": ["cntt_htdn", "cdt", "ctm", "ck_dongluc", "cntp", "tudonghoa"],
    "thích làm việc nhóm": ["cntt_htdn", "qlcn", "ktxd", "xddc_cn"],
    "thích làm việc độc lập": ["cntt_htdn", "ktmt", "tudonghoa", "cnsinhhoc"],
    "kỹ năng giao tiếp": ["qlcn", "ktxd"],
    "kỹ năng quản lý": ["qlcn", "ktxd", "qltn_mt"],
    "tỉ mỉ": ["kientruc", "vidientu_vimach", "cdt", "cnsinhhoc_yd", "thxd"],
    "kiên nhẫn": ["cnsinhhoc", "vidientu_vimach", "cntp", "kthh"],
    "thích thể hiện bản thân": ["kientruc", "xddc_cn"],
    
    # Tính cách chung
    "thích công nghệ": ["cntt_htdn", "cntt_ai", "cntt_nnn", "ktmt", "dtvt", "vidientu_vimach"],
    "thích khám phá": ["cntt_ai", "cnsinhhoc", "mt", "qltn_mt", "daukhi"],
    "thích tìm tòi": ["cntt_ai", "cnsinhhoc", "kthh", "qltn_mt"],
    "thích sáng tạo": ["kientruc", "cntt_htdn", "cntt_ai", "cdt"],
    "thích trải nghiệm": ["cntt_htdn", "ck_dongluc", "oto", "kientruc"],
    "thích chính xác": ["ktmt", "vidientu_vimach", "bim_ai", "thxd"],
    "thích thực tế": ["ck_dongluc", "oto", "cdt", "ctm", "qlcn"],
    "thích mới mẻ": ["cntt_ai", "kientruc", "cnsinhhoc"],
    "thích ổn định": ["ktdien", "xddc_cn", "qlcn", "ktxd"],
    "hướng nội": ["cntt_htdn", "ktmt", "thxd"],
    "hướng ngoại": ["qlcn", "ktxd", "kientruc"],
}

# Trọng số mức độ phù hợp của các sở thích/điểm mạnh với ngành
STRENGTH_WEIGHT = {
    # Sở thích và điểm mạnh chính của ngành CNTT
    "lập trình": {"cntt_htdn": 1.0, "cntt_ai": 0.9, "cntt_nnn": 0.9, "ktmt": 0.8, "vidientu_vimach": 0.6},
    "máy tính": {"cntt_htdn": 1.0, "ktmt": 0.9, "cntt_ai": 0.8, "cntt_nnn": 0.8, "dtvt": 0.6},
    "phân tích dữ liệu": {"cntt_ai": 1.0, "cntt_htdn": 0.7, "ktmt": 0.5},
    "giỏi toán": {"cntt_ai": 1.0, "cntt_htdn": 0.9, "ktmt": 0.9, "dtvt": 0.8, "tudonghoa": 0.8, "htcn": 0.7},
    
    # Sở thích và điểm mạnh chính của ngành kỹ thuật cơ khí
    "cơ khí": {"ck_dongluc": 1.0, "ctm": 0.9, "ck_hk": 0.9, "cdt": 0.8, "oto": 0.9},
    "máy móc": {"ctm": 1.0, "ck_dongluc": 0.9, "oto": 0.8, "cdt": 0.8},
    "động cơ": {"oto": 1.0, "ck_dongluc": 0.9},
    
    # Sở thích và điểm mạnh chính của ngành xây dựng
    "xây dựng": {"xddc_cn": 1.0, "ctthuy": 0.8, "ctgt": 0.8, "ktxd": 0.7, "cshatng": 0.8},
    "kiến trúc": {"kientruc": 1.0, "xddc_cn": 0.7, "thxd": 0.5},
    "thiết kế nhà": {"kientruc": 1.0, "xddc_cn": 0.8},
    
    # Sở thích và điểm mạnh chính của ngành điện
    "điện": {"ktdien": 1.0, "tudonghoa": 0.8, "dtvt": 0.6},
    "điện tử": {"dtvt": 1.0, "vidientu_vimach": 0.9, "tudonghoa": 0.7, "tien_tien_dtvt": 0.9},
    
    # Sở thích và điểm mạnh chính của ngành sinh học
    "sinh học": {"cnsinhhoc": 1.0, "cnsinhhoc_yd": 0.9, "mt": 0.6, "cntp": 0.5},
    "y dược": {"cnsinhhoc_yd": 1.0, "cnsinhhoc": 0.7},
    "công nghệ sinh học": {"cnsinhhoc": 1.0, "cnsinhhoc_yd": 0.9},
    
    # Sở thích và điểm mạnh chính của ngành quản lý
    "quản lý": {"qlcn": 1.0, "ktxd": 0.9, "qltn_mt": 0.8, "htcn": 0.7},
    "kinh tế": {"ktxd": 1.0, "qlcn": 0.8},
    
    # Sở thích và điểm mạnh chính của ngành năng lượng, môi trường
    "môi trường": {"mt": 1.0, "qltn_mt": 0.9, "cnsinhhoc": 0.5},
    "năng lượng": {"ktnqlnl": 1.0, "ktnhiet": 0.9, "ktdien": 0.7},
    
    # Tính cách và kỹ năng
    "tư duy logic": {"cntt_htdn": 1.0, "cntt_ai": 0.9, "ktmt": 0.9, "dtvt": 0.8, "tudonghoa": 0.8},
    "kỹ năng quản lý": {"qlcn": 1.0, "ktxd": 0.9, "qltn_mt": 0.8},
    "thích thực hành": {"ctm": 1.0, "cdt": 0.9, "oto": 0.9, "ck_dongluc": 0.8, "cntp": 0.8},
    "tỉ mỉ": {"vidientu_vimach": 1.0, "kientruc": 0.9, "cnsinhhoc_yd": 0.9, "thxd": 0.8},
    "thích sáng tạo": {"kientruc": 1.0, "cntt_ai": 0.8, "cdt": 0.7, "cntt_htdn": 0.7}
}

# Thêm danh sách ngành theo nhóm lĩnh vực
FIELD_MAJOR_GROUPS = {
    "công nghệ thông tin": ["cntt_htdn", "cntt_ai", "cntt_nnn", "ktmt", "tien_tien_nhung_iot"],
    "kỹ thuật điện - điện tử": ["ktdien", "dtvt", "vidientu_vimach", "tudonghoa", "tien_tien_dtvt"],
    "cơ khí - chế tạo": ["ck_dongluc", "ck_hk", "cdt", "ctm", "oto", "tauthuy"],
    "xây dựng - kiến trúc": ["xddc_cn", "thxd", "xdtttm", "bim_ai", "ctthuy", "ctgt", "duongsat", "ktxd", "cshatng", "kientruc"],
    "hóa - sinh học": ["cnsinhhoc", "cnsinhhoc_yd", "kthh", "cntp"],
    "năng lượng - môi trường": ["ktnhiet", "ktnqlnl", "mt", "qltn_mt", "daukhi"],
    "quản lý - kinh tế": ["qlcn", "htcn", "ktxd"]
}

# Lĩnh vực yêu thích - nhóm ngành phù hợp
INTEREST_FIELD_MAPPING = {
    "máy tính": "công nghệ thông tin",
    "lập trình": "công nghệ thông tin",
    "phần mềm": "công nghệ thông tin",
    "ai": "công nghệ thông tin",
    "điện tử": "kỹ thuật điện - điện tử",
    "robot": "kỹ thuật điện - điện tử",
    "viễn thông": "kỹ thuật điện - điện tử",
    "cơ khí": "cơ khí - chế tạo",
    "ô tô": "cơ khí - chế tạo",
    "máy móc": "cơ khí - chế tạo",
    "tàu biển": "cơ khí - chế tạo",
    "xây dựng": "xây dựng - kiến trúc",
    "kiến trúc": "xây dựng - kiến trúc",
    "thiết kế nhà": "xây dựng - kiến trúc",
    "cầu đường": "xây dựng - kiến trúc",
    "sinh học": "hóa - sinh học",
    "y dược": "hóa - sinh học",
    "hóa học": "hóa - sinh học",
    "thực phẩm": "hóa - sinh học",
    "môi trường": "năng lượng - môi trường",
    "năng lượng": "năng lượng - môi trường",
    "nhiệt": "năng lượng - môi trường",
    "quản lý": "quản lý - kinh tế",
    "kinh tế": "quản lý - kinh tế"
}

# Môn học - nhóm ngành phù hợp
SUBJECT_FIELD_MAPPING = {
    "toán": ["công nghệ thông tin", "kỹ thuật điện - điện tử", "quản lý - kinh tế"],
    "lý": ["kỹ thuật điện - điện tử", "cơ khí - chế tạo", "năng lượng - môi trường"],
    "hóa": ["hóa - sinh học", "năng lượng - môi trường"],
    "sinh": ["hóa - sinh học"],
    "tin": ["công nghệ thông tin"],
    "vẽ": ["xây dựng - kiến trúc", "cơ khí - chế tạo"]
}

def normalize_student_interests(interests_text):
    """
    Chuẩn hóa văn bản sở thích của học sinh thành danh sách các từ khóa
    
    Args:
        interests_text (str): Văn bản mô tả sở thích của học sinh
        
    Returns:
        list: Danh sách các từ khóa sở thích đã chuẩn hóa
    """
    if not interests_text:
        return []
    
    interests_text = clean_text(interests_text)
    found_interests = []
    
    # Tìm kiếm các từ khóa trong văn bản
    for interest in STUDENT_STRENGTH_MAPPING.keys():
        if interest in interests_text:
            found_interests.append(interest)
    
    return found_interests

def suggest_majors_by_interests(interests_list, max_results=5):
    """
    Gợi ý ngành học dựa trên sở thích của học sinh
    
    Args:
        interests_list (list): Danh sách các sở thích
        max_results (int): Số lượng ngành học tối đa trả về
        
    Returns:
        dict: Từ điển các ngành học được gợi ý với điểm phù hợp
    """
    if not interests_list:
        return {}
    
    # Tính điểm cho từng ngành dựa trên sở thích
    major_scores = {}
    
    for interest in interests_list:
        # Lấy danh sách ngành phù hợp với sở thích
        if interest in STUDENT_STRENGTH_MAPPING:
            related_majors = STUDENT_STRENGTH_MAPPING[interest]
            
            # Áp dụng trọng số nếu có
            if interest in STRENGTH_WEIGHT:
                weights = STRENGTH_WEIGHT[interest]
                for major in related_majors:
                    weight = weights.get(major, 0.5) # Mặc định 0.5 nếu không có trọng số cụ thể
                    major_scores[major] = major_scores.get(major, 0) + weight
            else:
                # Nếu không có trọng số, gán điểm đồng đều cho tất cả ngành liên quan
                for major in related_majors:
                    major_scores[major] = major_scores.get(major, 0) + 0.5
    
    # Kiểm tra xem có lĩnh vực nổi trội không
    field_scores = {}
    for interest in interests_list:
        if interest in INTEREST_FIELD_MAPPING:
            field = INTEREST_FIELD_MAPPING[interest]
            field_scores[field] = field_scores.get(field, 0) + 1
    
    # Tăng điểm cho ngành thuộc lĩnh vực được quan tâm nhiều
    if field_scores:
        dominant_field = max(field_scores.items(), key=lambda x: x[1])[0]
        if dominant_field in FIELD_MAJOR_GROUPS:
            for major in FIELD_MAJOR_GROUPS[dominant_field]:
                major_scores[major] = major_scores.get(major, 0) + 0.5
    
    # Sắp xếp và giới hạn số lượng kết quả
    sorted_majors = sorted(major_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Chỉ trả về top majors với điểm phù hợp
    return {major: score for major, score in sorted_majors[:max_results]}

def normalize_subjects_strengths(text):
    """
    Phân tích văn bản để xác định điểm mạnh về môn học của học sinh
    
    Args:
        text (str): Văn bản mô tả điểm mạnh về học tập
        
    Returns:
        list: Danh sách môn học là điểm mạnh
    """
    if not text:
        return []
    
    text = clean_text(text)
    strong_subjects = []
    
    # Tìm các môn học là điểm mạnh
    subject_patterns = {
        "giỏi toán": ["giỏi toán", "mạnh về toán", "thích toán", "điểm cao toán", "học giỏi toán"],
        "giỏi lý": ["giỏi lý", "mạnh về lý", "thích lý", "học giỏi vật lý", "điểm cao lý"],
        "giỏi hóa": ["giỏi hóa", "mạnh về hóa", "thích hóa", "học giỏi hóa học", "điểm cao hóa"],
        "giỏi sinh": ["giỏi sinh", "mạnh về sinh", "thích sinh", "học giỏi sinh học", "điểm cao sinh"],
        "giỏi tin": ["giỏi tin", "mạnh về tin", "thích tin", "học giỏi tin học", "điểm cao tin"],
        "giỏi anh": ["giỏi anh", "mạnh về anh", "thích tiếng anh", "học giỏi anh văn", "điểm cao anh"],
        "giỏi vẽ": ["giỏi vẽ", "mạnh về vẽ", "thích vẽ", "học giỏi mỹ thuật", "vẽ đẹp"]
    }
    
    for subject, patterns in subject_patterns.items():
        if any(pattern in text for pattern in patterns):
            strong_subjects.append(subject)
    
    return strong_subjects

def suggest_majors_by_academic_strengths(subjects_list, max_results=5):
    """
    Gợi ý ngành học dựa trên điểm mạnh môn học của học sinh
    
    Args:
        subjects_list (list): Danh sách các môn học là điểm mạnh
        max_results (int): Số lượng ngành học tối đa trả về
        
    Returns:
        dict: Từ điển các ngành học được gợi ý với điểm phù hợp
    """
    if not subjects_list:
        return {}
    
    # Tính điểm cho từng ngành dựa trên điểm mạnh môn học
    major_scores = {}
    
    for subject in subjects_list:
        if subject in STUDENT_STRENGTH_MAPPING:
            related_majors = STUDENT_STRENGTH_MAPPING[subject]
            
            # Áp dụng trọng số nếu có
            if subject in STRENGTH_WEIGHT:
                weights = STRENGTH_WEIGHT[subject]
                for major in related_majors:
                    weight = weights.get(major, 0.5)
                    major_scores[major] = major_scores.get(major, 0) + weight
            else:
                # Nếu không có trọng số, gán điểm đồng đều
                for major in related_majors:
                    major_scores[major] = major_scores.get(major, 0) + 0.5
    
    # Kiểm tra các lĩnh vực phù hợp với môn học mạnh
    field_scores = {}
    for subject_key in subjects_list:
        # Lấy tên môn học từ chuỗi "giỏi [môn học]"
        if subject_key.startswith("giỏi "):
            subject = subject_key.split(" ", 1)[1]
            if subject in SUBJECT_FIELD_MAPPING:
                for field in SUBJECT_FIELD_MAPPING[subject]:
                    field_scores[field] = field_scores.get(field, 0) + 1
    
    # Tăng điểm cho ngành thuộc lĩnh vực phù hợp với môn học mạnh
    if field_scores:
        for field, score in field_scores.items():
            if field in FIELD_MAJOR_GROUPS:
                for major in FIELD_MAJOR_GROUPS[field]:
                    major_scores[major] = major_scores.get(major, 0) + 0.3 * score
    
    # Sắp xếp và giới hạn số lượng kết quả
    sorted_majors = sorted(major_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Chỉ trả về top majors với điểm phù hợp
    return {major: score for major, score in sorted_majors[:max_results]}

def normalize_personality_strengths(text):
    """
    Phân tích văn bản để xác định tính cách và kỹ năng của học sinh
    
    Args:
        text (str): Văn bản mô tả tính cách/kỹ năng
        
    Returns:
        list: Danh sách tính cách/kỹ năng được xác định
    """
    if not text:
        return []
    
    text = clean_text(text)
    personality_traits = []
    
    # Danh sách các tính cách và kỹ năng cần tìm
    personality_keywords = [
        "tư duy logic", "tư duy sáng tạo", "thích giải quyết vấn đề",
        "thích thực hành", "thích làm việc nhóm", "thích làm việc độc lập",
        "kỹ năng giao tiếp", "kỹ năng quản lý", "tỉ mỉ", "kiên nhẫn",
        "thích thể hiện bản thân", "thích công nghệ", "thích khám phá",
        "thích tìm tòi", "thích sáng tạo", "thích trải nghiệm", "thích chính xác",
        "thích thực tế", "thích mới mẻ", "thích ổn định", "hướng nội", "hướng ngoại"
    ]
    
    for trait in personality_keywords:
        if trait in text:
            personality_traits.append(trait)
    
    return personality_traits

def comprehensive_major_suggestion(interests, academic_strengths, personality_traits, max_results=5):
    """
    Gợi ý ngành học tổng hợp dựa trên sở thích, điểm mạnh học tập và tính cách
    
    Args:
        interests (list): Danh sách sở thích
        academic_strengths (list): Danh sách điểm mạnh học tập
        personality_traits (list): Danh sách tính cách/kỹ năng
        max_results (int): Số lượng ngành học tối đa trả về
        
    Returns:
        dict: Từ điển các ngành học được gợi ý với điểm phù hợp và giải thích
    """
    # Tính điểm từ mọi nguồn
    all_scores = {}
    
    # 1. Điểm từ sở thích - trọng số 0.4
    if interests:
        interest_scores = suggest_majors_by_interests(interests)
        for major, score in interest_scores.items():
            all_scores[major] = all_scores.get(major, 0) + score * 0.4
    
    # 2. Điểm từ điểm mạnh học tập - trọng số 0.4
    if academic_strengths:
        academic_scores = suggest_majors_by_academic_strengths(academic_strengths)
        for major, score in academic_scores.items():
            all_scores[major] = all_scores.get(major, 0) + score * 0.4
    
    # 3. Điểm từ tính cách - trọng số 0.2
    if personality_traits:
        trait_scores = {}
        for trait in personality_traits:
            if trait in STUDENT_STRENGTH_MAPPING:
                majors = STUDENT_STRENGTH_MAPPING[trait]
                
                if trait in STRENGTH_WEIGHT:
                    weights = STRENGTH_WEIGHT[trait]
                    for major in majors:
                        weight = weights.get(major, 0.5)
                        trait_scores[major] = trait_scores.get(major, 0) + weight
                else:
                    for major in majors:
                        trait_scores[major] = trait_scores.get(major, 0) + 0.5
        
        for major, score in trait_scores.items():
            all_scores[major] = all_scores.get(major, 0) + score * 0.2
    
    # Sắp xếp ngành theo điểm tổng hợp
    sorted_majors = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Tạo kết quả với giải thích
    result = {}
    for major, score in sorted_majors[:max_results]:
        # Tạo giải thích
        explanation = []
        
        # Tìm các điểm phù hợp từ sở thích
        matching_interests = []
        for interest in interests:
            if major in STUDENT_STRENGTH_MAPPING.get(interest, []):
                matching_interests.append(interest)
        
        # Tìm các điểm phù hợp từ điểm mạnh học tập
        matching_subjects = []
        for subject in academic_strengths:
            if major in STUDENT_STRENGTH_MAPPING.get(subject, []):
                matching_subjects.append(subject)
        
        # Tìm các điểm phù hợp từ tính cách
        matching_traits = []
        for trait in personality_traits:
            if major in STUDENT_STRENGTH_MAPPING.get(trait, []):
                matching_traits.append(trait)
        
        # Tạo giải thích dựa trên điểm phù hợp
        if matching_interests:
            explanation.append(f"Phù hợp với sở thích: {', '.join(matching_interests)}")
        
        if matching_subjects:
            explanation.append(f"Phù hợp với điểm mạnh học tập: {', '.join(matching_subjects)}")
        
        if matching_traits:
            explanation.append(f"Phù hợp với tính cách: {', '.join(matching_traits)}")
        
        # Lưu kết quả
        result[major] = {
            "score": round(score, 2),
            "explanation": explanation
        }
    
    return result