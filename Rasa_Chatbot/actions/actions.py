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
            "dgtd": "Đánh giá tư duy",
            "học bạ": "Xét điểm học bạ"
        }

        major_mapping = {
            # Công nghệ thông tin
            "cntt đặc thù": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "cntt htdn": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "công nghệ thông tin đặc thù": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "công nghệ thông tin hợp tác doanh nghiệp": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "công nghệ thông tin đặc thù - hợp tác doanh nghiệp": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "cntt": "Công nghệ thông tin",
            "công nghệ thông tin": "Công nghệ thông tin",

            "cntt nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "cntt tiếng nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "cntt nn nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "công nghệ thông tin ngoại ngữ nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "công nghệ thông tin nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "công nghệ thông tin tiếng nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            
            "cntt ai": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt khdl": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt khdl & ttnt": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt ttnt": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "công nghệ thông tin trí tuệ nhân tạo": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "công nghệ thông tin khoa học dữ liệu": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "công nghệ thông tin khoa học dữ liệu và trí tuệ nhân tạo": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt đặc thù khdl": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            
            # Kỹ thuật máy tính
            "ktmt": "Kỹ thuật máy tính",
            "kỹ thuật máy tính": "Kỹ thuật máy tính",
            
            # Công nghệ sinh học
            "cnsh": "Công nghệ sinh học",
            "công nghệ sinh học": "Công nghệ sinh học",
            "cnsh y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "cnsh yd": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "công nghệ sinh học y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "công nghệ sinh học chuyên ngành y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "sinh học y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            
            # Công nghệ kỹ thuật vật liệu xây dựng
            "cnkt vlxd": "Công nghệ kỹ thuật vật liệu xây dựng",
            "công nghệ kỹ thuật vật liệu xây dựng": "Công nghệ kỹ thuật vật liệu xây dựng",
            "vật liệu xây dựng": "Công nghệ kỹ thuật vật liệu xây dựng",
            
            # Công nghệ chế tạo máy
            "cnctm": "Công nghệ chế tạo máy",
            "công nghệ chế tạo máy": "Công nghệ chế tạo máy",
            "chế tạo máy": "Công nghệ chế tạo máy",
            
            # Quản lý công nghiệp
            "qlcn": "Quản lý công nghiệp",
            "quản lý công nghiệp": "Quản lý công nghiệp",
            
            # Công nghệ dầu khí và khai thác dầu
            "cndk&ktd": "Công nghệ dầu khí và khai thác dầu",
            "cndk": "Công nghệ dầu khí và khai thác dầu",
            "công nghệ dầu khí": "Công nghệ dầu khí và khai thác dầu",
            "công nghệ dầu khí và khai thác dầu": "Công nghệ dầu khí và khai thác dầu",
            "dầu khí và khai thác dầu": "Công nghệ dầu khí và khai thác dầu",
            "khai thác dầu": "Công nghệ dầu khí và khai thác dầu",
            
            # Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)
            "pfiev": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "kỹ sư chất lượng cao việt - pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "ctđt kỹ sư clc việt - pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "kỹ sư việt pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "chương trình việt pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            
            # Kỹ thuật Cơ khí
            "ktck": "Kỹ thuật Cơ khí",
            "kỹ thuật cơ khí": "Kỹ thuật Cơ khí",
            "cơ khí": "Kỹ thuật Cơ khí",
            
            "ktck ckđl": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            "cơ khí động lực": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            "ktck chuyên ngành cơ khí động lực": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            "kỹ thuật cơ khí động lực": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            
            "ktck ckhk": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            "kỹ thuật cơ khí hàng không": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            "cơ khí hàng không": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            "ktck chuyên ngành ckhk": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            
            # Kỹ thuật Cơ điện tử
            "ktcđt": "Kỹ thuật Cơ điện tử",
            "kỹ thuật cơ điện tử": "Kỹ thuật Cơ điện tử",
            "cơ điện tử": "Kỹ thuật Cơ điện tử",
            "cdt": "Kỹ thuật Cơ điện tử",
            
            # Kỹ thuật nhiệt
            "ktn": "Kỹ thuật nhiệt",
            "kỹ thuật nhiệt": "Kỹ thuật nhiệt",
            "kỹ thuật nhiệt lạnh": "Kỹ thuật nhiệt",
            
            "ktn qlnl": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "kỹ thuật nhiệt quản lý năng lượng": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "ktn chuyên ngành qlnl": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "kỹ thuật nhiệt qlnl": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "quản lý năng lượng": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            
            # Kỹ thuật Tàu thủy
            "kttt": "Kỹ thuật Tàu thủy",
            "kỹ thuật tàu thủy": "Kỹ thuật Tàu thủy",
            "tàu thủy": "Kỹ thuật Tàu thủy",
            
            # Kỹ thuật Điện
            "ktđ": "Kỹ thuật Điện",
            "kỹ thuật điện": "Kỹ thuật Điện",
            "điện": "Kỹ thuật Điện",
            
            # Kỹ thuật điện tử - viễn thông
            "ktđt-vt": "Kỹ thuật điện tử - viễn thông",
            "ktđtvt": "Kỹ thuật điện tử - viễn thông",
            "kỹ thuật điện tử - viễn thông": "Kỹ thuật điện tử - viễn thông",
            "ktđt viễn thông": "Kỹ thuật điện tử - viễn thông",
            "kỹ thuật điện tử viễn thông": "Kỹ thuật điện tử - viễn thông",
            "điện tử viễn thông": "Kỹ thuật điện tử - viễn thông",
            "đtvt": "Kỹ thuật điện tử - viễn thông",
            
            # Kỹ thuật Điều khiển và Tự động hóa
            "ktđk&tđh": "Kỹ thuật Điều khiển và Tự động hóa",
            "ktđktđh": "Kỹ thuật Điều khiển và Tự động hóa",
            "kỹ thuật điều khiển và tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "ktđk và tđh": "Kỹ thuật Điều khiển và Tự động hóa",
            "kỹ thuật điều khiển tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "điều khiển tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "điều khiển và tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            
            # Kỹ thuật hóa học
            "kthh": "Kỹ thuật hóa học",
            "kỹ thuật hóa học": "Kỹ thuật hóa học",
            "hóa học": "Kỹ thuật hóa học",
            
            # Kỹ thuật môi trường
            "ktmt": "Kỹ thuật môi trường",
            "kỹ thuật môi trường": "Kỹ thuật môi trường",
            "môi trường": "Kỹ thuật môi trường",
            
            # Kỹ thuật hệ thống công nghiệp
            "kthtcn": "Kỹ thuật hệ thống công nghiệp",
            "kỹ thuật hệ thống công nghiệp": "Kỹ thuật hệ thống công nghiệp",
            "hệ thống công nghiệp": "Kỹ thuật hệ thống công nghiệp",
            
            # Chương trình tiên tiến Việt-Mỹ
            "cttt ktđtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "chương trình tiên tiến kỹ thuật điện tử viễn thông": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "cttt việt-mỹ ktđtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "chương trình tiên tiến ktđtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "tiên tiến điện tử viễn thông": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "cttt đtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            
            "cttt htn&iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "chương trình tiên tiến hệ thống nhúng và iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "cttt việt-mỹ htn và iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "chương trình tiên tiến hệ thống nhúng": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "tiên tiến hệ thống nhúng": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "cttt htn": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "hệ thống nhúng và iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "hệ thống nhúng": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            
            # Công nghệ thực phẩm
            "cntp": "Công nghệ thực phẩm",
            "công nghệ thực phẩm": "Công nghệ thực phẩm",
            "thực phẩm": "Công nghệ thực phẩm",
            
            # Kiến trúc
            "kt": "Kiến trúc",
            "kiến trúc": "Kiến trúc",
            
            # Kỹ thuật xây dựng
            "ktxd xddd&cn": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "kỹ thuật xây dựng dân dụng và công nghiệp": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "ktxd chuyên ngành xddd&cn": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "xây dựng dân dụng và công nghiệp": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "xd dân dụng": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "xd công nghiệp": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "kỹ thuật xây dựng dân dụng": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            
            "ktxd thxd": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "kỹ thuật xây dựng tin học xây dựng": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "ktxd chuyên ngành thxd": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "tin học xây dựng": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "thxd": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            
            "ktxd đttm": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "kỹ thuật xây dựng đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "ktxd qlxd đttm": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "kỹ thuật và quản lý xây dựng đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "xây dựng đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            
            "ktxd mhtt&ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "kỹ thuật xây dựng mô hình thông tin và ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "ktxd chuyên ngành mhtt và ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "kỹ thuật xây dựng mhtt và ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "mô hình thông tin trong xây dựng": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "mhtt và ttnt trong xây dựng": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "trí tuệ nhân tạo trong xây dựng": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            
            # Kỹ thuật xây dựng công trình thủy
            "ktxdctt": "Kỹ thuật xây dựng công trình thủy",
            "kỹ thuật xây dựng công trình thủy": "Kỹ thuật xây dựng công trình thủy",
            "xây dựng công trình thủy": "Kỹ thuật xây dựng công trình thủy",
            "công trình thủy": "Kỹ thuật xây dựng công trình thủy",
            
            # Kỹ thuật xây dựng công trình giao thông
            "ktxdctgt": "Kỹ thuật xây dựng công trình giao thông",
            "kỹ thuật xây dựng công trình giao thông": "Kỹ thuật xây dựng công trình giao thông",
            "xây dựng công trình giao thông": "Kỹ thuật xây dựng công trình giao thông",
            "công trình giao thông": "Kỹ thuật xây dựng công trình giao thông",
            "cầu đường": "Kỹ thuật xây dựng công trình giao thông",
            
            "ktxdctgt đstđc": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "xây dựng đường sắt tốc độ cao": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "ktxdctgt chuyên ngành đstđc": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "xây dựng đường sắt đô thị": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "đường sắt tốc độ cao": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "đường sắt đô thị": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            
            # Kinh tế xây dựng
            "ktxd": "Kinh tế xây dựng",
            "kinh tế xây dựng": "Kinh tế xây dựng",
            
            # Kỹ thuật cơ sở hạ tầng
            "ktcsht": "Kỹ thuật cơ sở hạ tầng",
            "kỹ thuật cơ sở hạ tầng": "Kỹ thuật cơ sở hạ tầng",
            "cơ sở hạ tầng": "Kỹ thuật cơ sở hạ tầng",
            "hạ tầng": "Kỹ thuật cơ sở hạ tầng",
            
            # Quản lý tài nguyên và môi trường
            "qltn&mt": "Quản lý tài nguyên và môi trường",
            "quản lý tài nguyên và môi trường": "Quản lý tài nguyên và môi trường",
            "qltnmt": "Quản lý tài nguyên và môi trường",
            "tài nguyên và môi trường": "Quản lý tài nguyên và môi trường",
            "tài nguyên môi trường": "Quản lý tài nguyên và môi trường"
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
            "tài nguyên": ["tài nguyên", "tnmt"]
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
                "điểm thi tốt nghiệp thpt": ["thi thpt", "điểm thi", "tốt nghiệp thpt", "thpt", "tn"],
                "đánh giá năng lực": ["năng lực", "dgnl", "đgnl", "vact", "apt", "bài test năng lực"],
                "đánh giá tư duy": ["tư duy", "dgtd", "tsa", "bài test tư duy"],
                "xét điểm học bạ": ["học bạ", "xét học bạ", "điểm học bạ", "tbhb", "xhb", "học bạ thpt"],
                "xét tuyển riêng": ["tuyển riêng", "xét riêng", "riêng", "phỏng vấn"]
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
        
        # Ghi log kết quả chuẩn hóa để debug (tùy chọn)
        # logging.debug(f"Normalized major: {major_keyword}, Normalized method: {method_keyword}")

        # Truy vấn và xử lý kết quả như cũ
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
            "cntt đặc thù": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "cntt htdn": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "công nghệ thông tin đặc thù": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "công nghệ thông tin hợp tác doanh nghiệp": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "công nghệ thông tin đặc thù - hợp tác doanh nghiệp": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp)",
            "cntt": "Công nghệ thông tin",
            "công nghệ thông tin": "Công nghệ thông tin",

            "cntt nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "cntt tiếng nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "cntt nn nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "công nghệ thông tin ngoại ngữ nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "công nghệ thông tin nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            "công nghệ thông tin tiếng nhật": "Công nghệ thông tin (ngoại ngữ Nhật)",
            
            "cntt ai": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt khdl": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt khdl & ttnt": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt ttnt": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "công nghệ thông tin trí tuệ nhân tạo": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "công nghệ thông tin khoa học dữ liệu": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "công nghệ thông tin khoa học dữ liệu và trí tuệ nhân tạo": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            "cntt đặc thù khdl": "Công nghệ thông tin (Đặc thù - Hợp tác doanh nghiệp), chuyên ngành Khoa học dữ liệu và Trí tuệ nhân tạo",
            
            # Kỹ thuật máy tính
            "ktmt": "Kỹ thuật máy tính",
            "kỹ thuật máy tính": "Kỹ thuật máy tính",
            
            # Công nghệ sinh học
            "cnsh": "Công nghệ sinh học",
            "công nghệ sinh học": "Công nghệ sinh học",
            "cnsh y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "cnsh yd": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "công nghệ sinh học y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "công nghệ sinh học chuyên ngành y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            "sinh học y dược": "Công nghệ sinh học, chuyên ngành Công nghệ sinh học Y Dược",
            
            # Công nghệ kỹ thuật vật liệu xây dựng
            "cnkt vlxd": "Công nghệ kỹ thuật vật liệu xây dựng",
            "công nghệ kỹ thuật vật liệu xây dựng": "Công nghệ kỹ thuật vật liệu xây dựng",
            "vật liệu xây dựng": "Công nghệ kỹ thuật vật liệu xây dựng",
            
            # Công nghệ chế tạo máy
            "cnctm": "Công nghệ chế tạo máy",
            "công nghệ chế tạo máy": "Công nghệ chế tạo máy",
            "chế tạo máy": "Công nghệ chế tạo máy",
            
            # Quản lý công nghiệp
            "qlcn": "Quản lý công nghiệp",
            "quản lý công nghiệp": "Quản lý công nghiệp",
            
            # Công nghệ dầu khí và khai thác dầu
            "cndk&ktd": "Công nghệ dầu khí và khai thác dầu",
            "cndk": "Công nghệ dầu khí và khai thác dầu",
            "công nghệ dầu khí": "Công nghệ dầu khí và khai thác dầu",
            "công nghệ dầu khí và khai thác dầu": "Công nghệ dầu khí và khai thác dầu",
            "dầu khí và khai thác dầu": "Công nghệ dầu khí và khai thác dầu",
            "khai thác dầu": "Công nghệ dầu khí và khai thác dầu",
            
            # Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)
            "pfiev": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "kỹ sư chất lượng cao việt - pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "ctđt kỹ sư clc việt - pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "kỹ sư việt pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            "chương trình việt pháp": "Chương trình đào tạo kỹ sư chất lượng cao Việt - Pháp (PFIEV)",
            
            # Kỹ thuật Cơ khí
            "ktck": "Kỹ thuật Cơ khí",
            "kỹ thuật cơ khí": "Kỹ thuật Cơ khí",
            "cơ khí": "Kỹ thuật Cơ khí",
            
            "ktck ckđl": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            "cơ khí động lực": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            "ktck chuyên ngành cơ khí động lực": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            "kỹ thuật cơ khí động lực": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí động lực",
            
            "ktck ckhk": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            "kỹ thuật cơ khí hàng không": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            "cơ khí hàng không": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            "ktck chuyên ngành ckhk": "Kỹ thuật Cơ khí, chuyên ngành Cơ khí hàng không",
            
            # Kỹ thuật Cơ điện tử
            "ktcđt": "Kỹ thuật Cơ điện tử",
            "kỹ thuật cơ điện tử": "Kỹ thuật Cơ điện tử",
            "cơ điện tử": "Kỹ thuật Cơ điện tử",
            "cdt": "Kỹ thuật Cơ điện tử",
            
            # Kỹ thuật nhiệt
            "ktn": "Kỹ thuật nhiệt",
            "kỹ thuật nhiệt": "Kỹ thuật nhiệt",
            "kỹ thuật nhiệt lạnh": "Kỹ thuật nhiệt",
            
            "ktn qlnl": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "kỹ thuật nhiệt quản lý năng lượng": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "ktn chuyên ngành qlnl": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "kỹ thuật nhiệt qlnl": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            "quản lý năng lượng": "Kỹ thuật Nhiệt, Chuyên ngành Quản lý năng lượng",
            
            # Kỹ thuật Tàu thủy
            "kttt": "Kỹ thuật Tàu thủy",
            "kỹ thuật tàu thủy": "Kỹ thuật Tàu thủy",
            "tàu thủy": "Kỹ thuật Tàu thủy",
            
            # Kỹ thuật Điện
            "ktđ": "Kỹ thuật Điện",
            "kỹ thuật điện": "Kỹ thuật Điện",
            "điện": "Kỹ thuật Điện",
            
            # Kỹ thuật điện tử - viễn thông
            "ktđt-vt": "Kỹ thuật điện tử - viễn thông",
            "ktđtvt": "Kỹ thuật điện tử - viễn thông",
            "kỹ thuật điện tử - viễn thông": "Kỹ thuật điện tử - viễn thông",
            "ktđt viễn thông": "Kỹ thuật điện tử - viễn thông",
            "kỹ thuật điện tử viễn thông": "Kỹ thuật điện tử - viễn thông",
            "điện tử viễn thông": "Kỹ thuật điện tử - viễn thông",
            "đtvt": "Kỹ thuật điện tử - viễn thông",
            
            # Kỹ thuật Điều khiển và Tự động hóa
            "ktđk&tđh": "Kỹ thuật Điều khiển và Tự động hóa",
            "ktđktđh": "Kỹ thuật Điều khiển và Tự động hóa",
            "kỹ thuật điều khiển và tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "ktđk và tđh": "Kỹ thuật Điều khiển và Tự động hóa",
            "kỹ thuật điều khiển tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "điều khiển tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            "điều khiển và tự động hóa": "Kỹ thuật Điều khiển và Tự động hóa",
            
            # Kỹ thuật hóa học
            "kthh": "Kỹ thuật hóa học",
            "kỹ thuật hóa học": "Kỹ thuật hóa học",
            "hóa học": "Kỹ thuật hóa học",
            
            # Kỹ thuật môi trường
            "ktmt": "Kỹ thuật môi trường",
            "kỹ thuật môi trường": "Kỹ thuật môi trường",
            "môi trường": "Kỹ thuật môi trường",
            
            # Kỹ thuật hệ thống công nghiệp
            "kthtcn": "Kỹ thuật hệ thống công nghiệp",
            "kỹ thuật hệ thống công nghiệp": "Kỹ thuật hệ thống công nghiệp",
            "hệ thống công nghiệp": "Kỹ thuật hệ thống công nghiệp",
            
            # Chương trình tiên tiến Việt-Mỹ
            "cttt ktđtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "chương trình tiên tiến kỹ thuật điện tử viễn thông": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "cttt việt-mỹ ktđtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "chương trình tiên tiến ktđtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "tiên tiến điện tử viễn thông": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            "cttt đtvt": "Chương trình tiên tiến Việt-Mỹ ngành Kỹ thuật Điện tử viễn thông",
            
            "cttt htn&iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "chương trình tiên tiến hệ thống nhúng và iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "cttt việt-mỹ htn và iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "chương trình tiên tiến hệ thống nhúng": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "tiên tiến hệ thống nhúng": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "cttt htn": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "hệ thống nhúng và iot": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            "hệ thống nhúng": "Chương trình tiên tiến Việt-Mỹ ngành Hệ thống Nhúng và IoT",
            
            # Công nghệ thực phẩm
            "cntp": "Công nghệ thực phẩm",
            "công nghệ thực phẩm": "Công nghệ thực phẩm",
            "thực phẩm": "Công nghệ thực phẩm",
            
            # Kiến trúc
            "kt": "Kiến trúc",
            "kiến trúc": "Kiến trúc",
            
            # Kỹ thuật xây dựng
            "ktxd xddd&cn": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "kỹ thuật xây dựng dân dụng và công nghiệp": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "ktxd chuyên ngành xddd&cn": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "xây dựng dân dụng và công nghiệp": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "xd dân dụng": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "xd công nghiệp": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            "kỹ thuật xây dựng dân dụng": "Kỹ thuật xây dựng, chuyên ngành Xây dựng dân dụng và công nghiệp",
            
            "ktxd thxd": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "kỹ thuật xây dựng tin học xây dựng": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "ktxd chuyên ngành thxd": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "tin học xây dựng": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            "thxd": "Kỹ thuật xây dựng, chuyên ngành Tin học xây dựng",
            
            "ktxd đttm": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "kỹ thuật xây dựng đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "ktxd qlxd đttm": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "kỹ thuật và quản lý xây dựng đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "xây dựng đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            "đô thị thông minh": "Kỹ thuật xây dựng, chuyên ngành Kỹ thuật và quản lý xây dựng đô thị thông minh",
            
            "ktxd mhtt&ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "kỹ thuật xây dựng mô hình thông tin và ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "ktxd chuyên ngành mhtt và ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "kỹ thuật xây dựng mhtt và ttnt": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "mô hình thông tin trong xây dựng": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "mhtt và ttnt trong xây dựng": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            "trí tuệ nhân tạo trong xây dựng": "Kỹ thuật xây dựng, chuyên ngành Mô hình thông tin và trí tuệ nhân tạo trong xây dựng",
            
            # Kỹ thuật xây dựng công trình thủy
            "ktxdctt": "Kỹ thuật xây dựng công trình thủy",
            "kỹ thuật xây dựng công trình thủy": "Kỹ thuật xây dựng công trình thủy",
            "xây dựng công trình thủy": "Kỹ thuật xây dựng công trình thủy",
            "công trình thủy": "Kỹ thuật xây dựng công trình thủy",
            
            # Kỹ thuật xây dựng công trình giao thông
            "ktxdctgt": "Kỹ thuật xây dựng công trình giao thông",
            "kỹ thuật xây dựng công trình giao thông": "Kỹ thuật xây dựng công trình giao thông",
            "xây dựng công trình giao thông": "Kỹ thuật xây dựng công trình giao thông",
            "công trình giao thông": "Kỹ thuật xây dựng công trình giao thông",
            "cầu đường": "Kỹ thuật xây dựng công trình giao thông",
            
            "ktxdctgt đstđc": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "xây dựng đường sắt tốc độ cao": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "ktxdctgt chuyên ngành đstđc": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "xây dựng đường sắt đô thị": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "đường sắt tốc độ cao": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            "đường sắt đô thị": "Kỹ thuật xây dựng công trình giao thông, Chuyên ngành xây dựng đường sắt tốc độ cao và đường sắt đô thị",
            
            # Kinh tế xây dựng
            "ktxd": "Kinh tế xây dựng",
            "kinh tế xây dựng": "Kinh tế xây dựng",
            
            # Kỹ thuật cơ sở hạ tầng
            "ktcsht": "Kỹ thuật cơ sở hạ tầng",
            "kỹ thuật cơ sở hạ tầng": "Kỹ thuật cơ sở hạ tầng",
            "cơ sở hạ tầng": "Kỹ thuật cơ sở hạ tầng",
            "hạ tầng": "Kỹ thuật cơ sở hạ tầng",
            
            # Quản lý tài nguyên và môi trường
            "qltn&mt": "Quản lý tài nguyên và môi trường",
            "quản lý tài nguyên và môi trường": "Quản lý tài nguyên và môi trường",
            "qltnmt": "Quản lý tài nguyên và môi trường",
            "tài nguyên và môi trường": "Quản lý tài nguyên và môi trường",
            "tài nguyên môi trường": "Quản lý tài nguyên và môi trường"
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
            "tài nguyên": ["tài nguyên", "tnmt"]
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
                message = f"📚 **Tổ hợp môn xét tuyển của ngành {major_keyword}**:\n\n"
                for idx, combo in enumerate(combinations, 1):
                    message += f"{idx}. {combo['subject_combination']}\n"
                message += "\n💡 *Bạn có thể tham khảo điểm chuẩn của ngành này theo từng năm và phương thức xét tuyển.*"
            else:
                message = f"❗ Không tìm thấy thông tin về tổ hợp môn xét tuyển cho ngành **{major_keyword}**.\n\nVui lòng kiểm tra lại tên ngành hoặc liên hệ với nhà trường để biết thêm thông tin."
        else:
            message = "❓ Vui lòng cho biết tên ngành cụ thể bạn muốn tìm hiểu về tổ hợp môn xét tuyển.\n\nVí dụ: *\"Tổ hợp môn xét tuyển ngành Công nghệ thông tin là gì?\"*"

        dispatcher.utter_message(text=message)
        return []