<template>
  <!-- Use admin layout when path starts with /admins -->
  <router-view v-if="isAdminPage"/>
  
  <!-- Use regular layout for all other pages -->
  <div v-else id="app">
    <!-- Enhanced Header with better mobile responsiveness -->
    <header class="custom-header navbar navbar-expand-lg">
      <div class="container-fluid px-5vw d-flex align-items-center">
        <!-- Logo and Brand -->
        <router-link 
          to="/" 
          class="navbar-brand d-flex align-items-center text-decoration-none"
          aria-label="DUT Home"
        >
          <img src="/dut_logo.png" alt="DUT Logo" class="header-logo me-2" width="45" height="45" />
          <div class="header-info d-none d-md-flex flex-column">
            <h1 class="header-title mb-0">
              <span class="university-title" style="color: #4da0ff;">ĐẠI HỌC ĐÀ NẴNG</span>
              <span class="school-title text-danger">TRƯỜNG ĐẠI HỌC BÁCH KHOA</span>
            </h1>
            <hr class="hr-custom my-1" />
            <span class="fw-bold header-info-eng" style="color:#0B2942;">
              UNIVERSITY OF SCIENCE AND TECHNOLOGY - UD
            </span>
          </div>
        </router-link>

        <!-- Mobile Menu Button with Improved Accessibility -->
        <button 
          class="navbar-toggler" 
          type="button" 
          aria-controls="navbarNav" 
          aria-expanded="false" 
          aria-label="Toggle navigation"
          @click="toggleMainMenu"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Navigation Menu with Improved Structure -->
        <nav class="collapse navbar-collapse" id="navbarNav" :class="{'show': isMainMenuOpen}">
          <ul class="navbar-nav ms-auto main-menu">
            <!-- Các mục luôn hiển thị -->
            <li class="nav-item menu-item">
              <router-link class="nav-link custom-nav-link" to="/" aria-label="Home" @click="closeMainMenu">
                <i class="bi bi-house-fill me-1"></i> <span>Home</span>
              </router-link>
            </li>
            <li class="nav-item dropdown menu-item" :class="{'open': activeSubmenu === 'tuyensinh'}">
              <a 
                class="nav-link dropdown-toggle custom-dropdown" 
                href="#" 
                role="button" 
                aria-expanded="false" 
                aria-haspopup="true"
                @click.prevent="toggleSubmenu('tuyensinh')"
              >
                <i class="bi bi-mortarboard-fill me-1"></i> <span>Tuyển sinh năm 2025</span>
              </a>
              <ul class="custom-dropdown-menu" :class="{'show-mobile': activeSubmenu === 'tuyensinh'}">
                <li><router-link class="dropdown-item" to="/admission" @click="closeMainMenu">Thông tin tuyển sinh chung</router-link></li>
                <li><router-link class="dropdown-item" to="/major" @click="closeMainMenu">Danh sách ngành tuyển sinh</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/xettuyenthang" @click="closeMainMenu">Xét tuyển thẳng theo quy chế của Bộ GD&ĐT</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/xettuyenrieng" @click="closeMainMenu">Xét tuyển riêng theo đề án tuyển sinh</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/totnghiep_thpt" @click="closeMainMenu">Xét tuyển theo điểm thi tốt nghiệp THPT</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/hocba_thpt" @click="closeMainMenu">Xét tuyển theo điểm học tập cấp THPT</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/danhgianangluc" @click="closeMainMenu">Xét tuyển theo kết quả ĐGNL của ĐHQG TPHCM</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/danhgiatuduy" @click="closeMainMenu">Xét tuyển theo điểm thi ĐGTD của ĐHBK Hà Nội</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item" v-if="isAuthenticated" :class="{'open': activeSubmenu === 'congcu'}">
              <a 
                class="nav-link dropdown-toggle custom-dropdown" 
                href="#" 
                role="button" 
                aria-expanded="false" 
                aria-haspopup="true"
                @click.prevent="toggleSubmenu('congcu')"
              >
                <i class="bi bi-tools me-1"></i> <span>Công cụ</span>
              </a>
              <ul class="custom-dropdown-menu" :class="{'show-mobile': activeSubmenu === 'congcu'}">
                <li><router-link class="dropdown-item" to="/school-priority" @click="closeMainMenu">Tra cứu điểm ưu tiên khu vực</router-link></li>
                <li><router-link class="dropdown-item" to="/calculatescore/xettuyenrieng" @click="closeMainMenu">Tính điểm PT xét tuyển riêng</router-link></li>
                <li><router-link class="dropdown-item" to="/calculatescore/hb" @click="closeMainMenu">Tính điểm xét tuyển học bạ THPT</router-link></li>
                <li><router-link class="dropdown-item" to="/calculatescore/thpt" @click="closeMainMenu">Tính điểm xét tuyển thi THPT</router-link></li>
                <li><router-link class="dropdown-item" to="/calculatescore/convert" @click="closeMainMenu">Quy đổi điểm tương đương</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item" :class="{'open': activeSubmenu === 'thongke'}">
              <a 
                class="nav-link dropdown-toggle custom-dropdown" 
                href="#" 
                role="button" 
                aria-expanded="false" 
                aria-haspopup="true"
                @click.prevent="toggleSubmenu('thongke')"
              >
                <i class="bi bi-calculator-fill me-1"></i> <span>Thống kê</span>
              </a>
              <ul class="custom-dropdown-menu" :class="{'show-mobile': activeSubmenu === 'thongke'}">
                <li><router-link class="dropdown-item" to="/statistics/previous-admission" @click="closeMainMenu">Điểm chuẩn các năm trước</router-link></li>
                <li><router-link class="dropdown-item" to="/statistics/pre-admitted-student" @click="closeMainMenu">Thống kê sinh viên nhập học</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item" :class="{'open': activeSubmenu === 'ctdt'}">
              <a 
                class="nav-link dropdown-toggle custom-dropdown" 
                href="#" 
                role="button" 
                aria-expanded="false" 
                aria-haspopup="true"
                @click.prevent="toggleSubmenu('ctdt')"
              >
                <i class="bi bi-laptop-fill me-1"></i> <span>CTĐT</span>
              </a>
              <ul class="custom-dropdown-menu" :class="{'show-mobile': activeSubmenu === 'ctdt'}">
                <li><router-link class="dropdown-item" to="/ctdt" @click="closeMainMenu">Danh sách chương trình đào tạo</router-link></li>
                <li><router-link class="dropdown-item" to="/ctdt/1" @click="closeMainMenu">Khoa Công nghệ thông tin</router-link></li>
              </ul>
            </li>

            <!-- Nếu đã đăng nhập -->
            <template v-if="isAuthenticated">
              <li class="nav-item dropdown menu-item" :class="{'open': activeSubmenu === 'tuvan'}">
                <a 
                  class="nav-link dropdown-toggle custom-dropdown" 
                  href="#" 
                  role="button" 
                  aria-expanded="false" 
                  aria-haspopup="true"
                  @click.prevent="toggleSubmenu('tuvan')"
                >
                  <i class="bi bi-chat-left-text-fill me-1"></i> <span>Tư vấn</span>
                </a>
                <ul class="custom-dropdown-menu" :class="{'show-mobile': activeSubmenu === 'tuvan'}">
                  <li><router-link class="dropdown-item" to="/qa" @click="closeMainMenu">Q&A</router-link></li>
                  <li><router-link class="dropdown-item" to="/chat" @click="closeMainMenu">
                    <i class="bi bi-chat-dots-fill me-1"></i> Chat với trợ lý
                  </router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown menu-item user-menu" :class="{'open': activeSubmenu === 'taikhoan'}">
                <a 
                  class="nav-link dropdown-toggle custom-dropdown d-flex align-items-center" 
                  href="#" 
                  role="button" 
                  aria-expanded="false" 
                  aria-haspopup="true"
                  @click.prevent="toggleSubmenu('taikhoan')"
                >
                  <i class="bi bi-person-circle me-1"></i>
                  <span class="user-email text-truncate">{{ userEmail }}</span>
                </a>
                <ul class="custom-dropdown-menu dropdown-menu-end" :class="{'show-mobile': activeSubmenu === 'taikhoan'}">
                  
                  <!-- Nếu người dùng có role là admin thì hiện thêm nút quản trị hệ thống -->
                  <li v-if="isAdmin">
                    <router-link class="dropdown-item" to="/admins" @click="closeMainMenu">
                      <i class="bi bi-gear-fill me-1"></i> Quản trị hệ thống
                    </router-link>
                  </li>
                  <li v-else>
                    <router-link class="dropdown-item" to="/profile" @click="closeMainMenu">
                      <i class="bi bi-person-vcard-fill me-1"></i> Thông tin cá nhân
                    </router-link>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                      <i class="bi bi-box-arrow-right me-1"></i> Đăng xuất
                    </a>
                  </li>
                </ul>
              </li>
            </template>

            <!-- Nếu chưa đăng nhập -->
            <template v-else>
              <li class="nav-item dropdown menu-item" :class="{'open': activeSubmenu === 'taikhoan'}">
                <a 
                  class="nav-link dropdown-toggle custom-dropdown" 
                  href="#" 
                  role="button" 
                  aria-expanded="false" 
                  aria-haspopup="true"
                  @click.prevent="toggleSubmenu('taikhoan')"
                >
                  <i class="bi bi-person-circle me-1"></i> <span>Tài khoản</span>
                </a>
                <ul class="custom-dropdown-menu dropdown-menu-end" :class="{'show-mobile': activeSubmenu === 'taikhoan'}">
                  <li>
                    <router-link class="dropdown-item" to="/login" @click="closeMainMenu">
                      <i class="bi bi-box-arrow-in-right me-1"></i> Đăng nhập
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/register" @click="closeMainMenu">
                      <i class="bi bi-person-plus me-1"></i> Đăng ký
                    </router-link>
                  </li>
                </ul>
              </li>
            </template>
          </ul>
        </nav>
      </div>
    </header>
    <router-view/>
    <footer class="custom-footer">
      <div class="container-fluid px-5vw py-4">
        <div class="row">
          <div class="col-lg-4 mb-4 mb-lg-0">
            <div class="d-flex align-items-center mb-3">
              <img src="/dut_logo.png" alt="DUT Logo" class="footer-logo me-3" width="50" height="50" />
              <div class="footer-info">
                <div class="fw-bold" style="color: #4da0ff;">ĐẠI HỌC ĐÀ NẴNG</div>
                <div class="fw-bold text-danger">TRƯỜNG ĐẠI HỌC BÁCH KHOA</div>
              </div>
            </div>
            <p><i class="bi bi-geo-alt-fill me-2"></i> 54 Nguyễn Lương Bằng, Phường Hòa Khánh Bắc, Quận Liên Chiểu, Thành Phố Đà Nẵng</p>
            <p><i class="bi bi-telephone-fill me-2"></i> 0888 477 377 - 0888 377 177 - 0888 577 277</p>
            <p><i class="bi bi-envelope-fill me-2"></i> tuyensinhbkdn@dut.udn.vn</p>
          </div>
          
          <div class="col-lg-4 mb-4 mb-lg-0">
            <h5 class="footer-heading">Liên kết hữu ích</h5>
            <ul class="footer-links">
              <li><a href="https://dut.udn.vn/" target="_blank" rel="noopener">Website chính thức DUT</a></li>
              <li><a href="https://tuyensinh.dut.udn.vn/" target="_blank" rel="noopener">Cổng thông tin tuyển sinh</a></li>
              <li><a href="https://www.facebook.com/DUTpage/" target="_blank" rel="noopener">Facebook tuyển sinh</a></li>
            </ul>
          </div>
          
          <div class="col-lg-4">
            <h5 class="footer-heading">Thống kê truy cập</h5>
            <div class="visitor-stats">
              <p><i class="bi bi-people-fill me-2"></i> Đang truy cập: <span class="fw-bold">{{ currentVisitors }}</span></p>
              <p><i class="bi bi-bar-chart-fill me-2"></i> Tổng lượt truy cập: <span class="fw-bold">{{ totalVisitors }}</span></p>
            </div>
            <div class="social-links mt-3">
              <a href="https://www.facebook.com/bachkhoaDUT" target="_blank" rel="noopener" aria-label="Facebook">
                <i class="bi bi-facebook"></i>
              </a>
              <a href="https://www.youtube.com/@DUTMedia" target="_blank" rel="noopener" aria-label="YouTube">
                <i class="bi bi-youtube"></i>
              </a>
            </div>
          </div>
        </div>
        <hr class="my-4" />
        <div class="text-center">
          <p class="mb-0">&copy; {{ new Date().getFullYear() }} Trường Đại học Bách khoa - Đại học Đà Nẵng. All rights reserved.</p>
        </div>
      </div>
    </footer>
    
    <!-- Backdrop for mobile menu -->
    <div 
      class="menu-backdrop" 
      v-if="isMainMenuOpen || activeSubmenu" 
      @click="closeAllMenus"
    ></div>
  </div>
  
  <!-- Mini Chat Widget Component -->
  <MiniChatWidget v-if="isAuthenticated && !isAdminPage" />
</template>

<script>
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import store from '@/store'
import axios from 'axios'
import config from '@/config/apiConfig'  // nếu bạn đã tách riêng file cấu hình base API
import UserController from '@/controllers/userController'
import MiniChatWidget from '@/components/MiniChatWidget.vue'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

export default {
  components: {
    MiniChatWidget
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isAuthenticated = computed(() => !!store.state.token)
    const userEmail = computed(() => store.state.user.email)
    const isAdmin = ref(false)
    
    // State for mobile menu
    const isMainMenuOpen = ref(false)
    const activeSubmenu = ref(null)
    
    // Check if current page is admin page
    const isAdminPage = computed(() => {
      return route.path.startsWith('/admins')
    })
    
    // Thêm biến để lưu trữ số liệu người truy cập
    const currentVisitors = ref(0)
    const totalVisitors = ref(0)
    let heartbeatInterval = null

    const logout = () => {
      store.clearToken()
      router.push({ name: 'Login' })
    }
    
    // Handle logout with menu closing
    const handleLogout = () => {
      closeAllMenus()
      logout()
    }
    
    // Toggle main mobile menu
    const toggleMainMenu = () => {
      isMainMenuOpen.value = !isMainMenuOpen.value
      if (!isMainMenuOpen.value) {
        // If closing main menu, also close any open submenu
        activeSubmenu.value = null
      }
    }
    
    // Toggle submenu
    const toggleSubmenu = (menuId) => {
      if (window.innerWidth >= 992) {
        // On desktop, do nothing special (hover handled by CSS)
        return
      }
      
      // On mobile
      if (activeSubmenu.value === menuId) {
        // If clicking on the same submenu, close it
        activeSubmenu.value = null
      } else {
        // Otherwise, open this submenu
        activeSubmenu.value = menuId
      }
    }
    
    // Close main menu
    const closeMainMenu = () => {
      isMainMenuOpen.value = false
      activeSubmenu.value = null
    }
    
    // Close all menus
    const closeAllMenus = () => {
      isMainMenuOpen.value = false
      activeSubmenu.value = null
    }

    // Hàm kiểm tra quyền admin
    const checkIsAdmin = async () => {
      if (isAuthenticated.value) {
        try {
          const user = await UserController.getCurrentUser()
          isAdmin.value = user && user.role === 'admin'
        } catch (error) {
          console.error('Error checking admin role:', error)
          isAdmin.value = false
        }
      } else {
        isAdmin.value = false
      }
    }

    // Hàm lấy thông tin người truy cập
    const fetchVisitorStats = async () => {
      if (isAdminPage.value) return // Skip for admin pages
      
      try {
        const response = await axios.get(`${BASE_API_URL}/visitors/stats`, {
          withCredentials: true // Cần thiết để gửi cookie session
        })
        
        if (response.data) {
          currentVisitors.value = response.data.current_visitors
          totalVisitors.value = response.data.total_visitors
        }
      } catch (error) {
        console.error('Error fetching visitor stats:', error)
      }
    }

    // Hàm gửi heartbeat để duy trì session
    const sendHeartbeat = async () => {
      if (isAdminPage.value) return // Skip for admin pages
      
      try {
        await axios.post(`${BASE_API_URL}/visitors/heartbeat`, {}, {
          withCredentials: true
        })
      } catch (error) {
        console.error('Error sending heartbeat:', error)
      }
    }

    onMounted(() => {
      // Only setup these handlers for non-admin pages
      if (!isAdminPage.value) {
        const header = document.querySelector('.custom-header')
        const handleScroll = () => {
          if (window.scrollY > 50) {
            header.classList.add('scrolled')
          } else {
            header.classList.remove('scrolled')
          }
        }
        window.addEventListener('scroll', handleScroll)
        handleScroll()

        // Close menu on escape key
        const handleEscKey = (e) => {
          if (e.key === 'Escape') {
            closeAllMenus()
          }
        }
        window.addEventListener('keydown', handleEscKey)

        // Kiểm tra quyền admin khi component được mount
        checkIsAdmin()

        // Lấy thông tin người truy cập khi trang được tải
        fetchVisitorStats()
        
        // Thiết lập heartbeat mỗi 5 phút để duy trì session và cập nhật số liệu
        heartbeatInterval = setInterval(() => {
          sendHeartbeat()
          fetchVisitorStats()
          if (isAuthenticated.value) {
            checkIsAdmin() // Cập nhật quyền admin định kỳ
          }
        }, 5 * 60 * 1000) // 5 phút

        onBeforeUnmount(() => {
          window.removeEventListener('scroll', handleScroll)
          window.removeEventListener('keydown', handleEscKey)
          // Xóa interval khi component unmount
          if (heartbeatInterval) {
            clearInterval(heartbeatInterval)
          }
        })
      } else {
        // For admin pages, just check admin permissions
        checkIsAdmin()
      }
    })

    // Watch for route changes to close menus
    watch(
      () => route.path,
      () => {
        closeAllMenus()
        if (!isAdminPage.value) {
          checkIsAdmin()
          fetchVisitorStats()
        }
      }
    )
    
    // Close menus when window is resized to desktop size
    watch(
      () => window.innerWidth,
      (newWidth) => {
        if (newWidth >= 992) {
          closeAllMenus()
        }
      }
    )

    return { 
      isAuthenticated, 
      userEmail,
      isAdmin, 
      logout,
      currentVisitors,
      totalVisitors,
      isAdminPage,
      // Menu state and controls
      isMainMenuOpen,
      activeSubmenu,
      toggleMainMenu,
      toggleSubmenu,
      closeMainMenu,
      closeAllMenus,
      handleLogout
    }
  }
}
</script>

<style scoped>
/* Enhanced Header Styles */
.custom-header {
  background-color: #efeff3f3 !important;
  position: sticky;
  top: 0;
  z-index: 1050;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 0.5rem 0;
}

.custom-header.scrolled {
  backdrop-filter: blur(10px);
  background-color: rgba(197, 250, 250, 0.85) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.px-5vw {
  padding-left: 5vw !important;
  padding-right: 5vw !important;
}

.header-logo {
  height: 45px;
  width: 45px;
  object-fit: contain;
  transition: all 0.3s ease;
}

.navbar-brand {
  margin-right: 1.5rem;
  padding: 0;
  max-width: 400px;
}

.header-info {
  line-height: 1.1;
  transition: all 0.3s ease;
}

.header-title {
  display: flex;
  flex-direction: column;
  font-size: 0.75rem;
  font-weight: bold;
  line-height: 1.1;
}

.header-info-eng {
  font-size: 0.55rem;
  white-space: nowrap;
}

.hr-custom {
  border: none;
  border-top: 2px solid #0B2942;
  width: 100%;
  margin: 3px 0;
}

/* Enhanced Menu Styles */
.main-menu {
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.menu-item {
  position: relative;
}

.user-menu {
  max-width: 200px;
}

.user-email {
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.custom-dropdown, .custom-nav-link {
  position: relative;
  padding: 0.6rem 0.8rem !important;
  font-weight: 500;
  color: #0B2942 !important;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.custom-dropdown:hover, .custom-nav-link:hover {
  color: #4da0ff !important;
}

.custom-dropdown::after, .custom-nav-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 4px;
  width: 0;
  height: 3px;
  background-color: #4da0ff;
  transition: width 0.3s ease;
  border-radius: 2px;
}

.custom-dropdown:hover::after, .custom-nav-link:hover::after {
  width: 100%;
}

.custom-dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  min-width: 260px;
  padding: 0.5rem 0;
  margin: 0;
  background-color: #f8f9fa;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Desktop dropdown behavior */
@media (min-width: 992px) {
  .menu-item:hover .custom-dropdown-menu {
    display: block;
  }
}

.custom-dropdown-menu li {
  border-bottom: 1px solid #e9ecef;
}

.custom-dropdown-menu li:last-child {
  border-bottom: none;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.6rem 1rem;
  font-weight: 400;
  color: #212529;
  text-align: left;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.dropdown-item:hover, .dropdown-item:focus {
  color: #0B2942 !important;
  background-color: #e9ecef;
  font-weight: 500;
}

.dropdown-menu-end {
  right: 0;
  left: auto;
}

/* Backdrop for mobile menu */
.menu-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
  backdrop-filter: blur(3px);
  animation: fadeBackdrop 0.3s ease;
}

@keyframes fadeBackdrop {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Enhanced Footer Styles */
.custom-footer {
  background-color: #0B2942;
  color: #fff;
  margin-top: 2rem;
}

.footer-logo {
  height: 50px;
  width: 50px;
  object-fit: contain;
}

.footer-info {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
  font-size: 0.7rem;
}

.footer-heading {
  color: #4da0ff;
  margin-bottom: 1.2rem;
  font-weight: 600;
  position: relative;
}

.footer-heading::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -8px;
  width: 50px;
  height: 2px;
  background-color: #4da0ff;
}

.footer-links {
  list-style: none;
  padding-left: 0;
}

.footer-links li {
  margin-bottom: 0.8rem;
}

.footer-links a {
  color: #e0e0e0;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: #4da0ff;
}

.visitor-stats p {
  margin-bottom: 0.5rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  transition: all 0.3s;
}

.social-icon:hover {
  background-color: #4da0ff;
  color: #fff;
}

/* Enhanced Mobile Menu Styles */
@media (max-width: 991.98px) {
  .px-5vw {
    padding-left: 4vw !important;
    padding-right: 4vw !important;
  }

  .header-logo {
    height: 40px;
    width: 40px;
  }
  
  /* Improved Mobile Navigation */
  #navbarNav {
    position: fixed;
    top: 70px;
    left: -100%;
    width: 280px;
    height: calc(100vh - 70px);
    background-color: #ffffff;
    box-shadow: 5px 0 15px rgba(0, 0, 0, 0.1);
    padding: 1rem;
    margin-top: 0;
    z-index: 1050;
    overflow-y: auto;
    transition: left 0.3s ease;
  }
  
  #navbarNav.show {
    left: 0;
  }
  
  .navbar-nav {
    padding: 0.5rem 0;
  }
  
  .menu-item {
    margin-bottom: 0.5rem;
    width: 100%;
  }
  
  .menu-item.open .custom-dropdown {
    color: #0B2942 !important;
    background-color: rgba(77, 160, 255, 0.1);
    border-radius: 8px;
  }
  
  .custom-dropdown, .custom-nav-link {
    padding: 0.7rem 1rem !important;
    width: 100%;
    border-radius: 8px;
    margin-bottom: 2px;
  }
  
  .custom-dropdown:hover, .custom-nav-link:hover {
    background-color: rgba(77, 160, 255, 0.05);
  }
  
  .custom-dropdown::after, .custom-nav-link::after {
    display: none;
  }
  
  /* Mobile submenu animation */
  .custom-dropdown-menu {
    position: static;
    box-shadow: none;
    border: none;
    border-radius: 0;
    background-color: transparent;
    padding: 0;
    width: 100%;
    max-height: 0;
    overflow: hidden;
    opacity: 0;
    transform: translateX(20px);
    transition: all 0.3s ease;
    margin-left: 1rem;
    display: block;
  }
  
  .custom-dropdown-menu.show-mobile {
    max-height: 1000px;
    opacity: 1;
    transform: translateX(0);
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .dropdown-item {
    padding: 0.7rem 1rem 0.7rem 1.5rem;
    border-left: 2px solid #e9ecef;
    margin-bottom: 2px;
    border-radius: 0 8px 8px 0;
    transition: all 0.2s ease;
  }
  
  .dropdown-item:hover, .dropdown-item:focus {
    border-left-color: #4da0ff;
    background-color: rgba(77, 160, 255, 0.1);
  }
  
  /* Custom hamburger menu */
  .navbar-toggler {
    border: none;
    padding: 0.5rem;
    border-radius: 0.25rem;
    background-color: transparent;
    transition: all 0.3s ease;
    z-index: 1060;
  }
  
  .navbar-toggler:focus {
    outline: none;
    box-shadow: none;
  }
  
  .navbar-toggler:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }
  
  .user-menu {
    max-width: none;
  }
  
  .user-email {
    max-width: none;
  }
}

@media (min-width: 992px) and (max-width: 1199px) {
  .custom-dropdown, .custom-nav-link {
    padding: 0.5rem 0.7rem !important;
    font-size: 0.8rem;
  }
  
  .navbar-brand {
    max-width: 300px;
  }
}

@media (max-width: 767.98px) {
  .px-5vw {
    padding-left: 3vw !important;
    padding-right: 3vw !important;
  }
  
  .header-logo {
    height: 35px;
    width: 35px;
  }
  
  #navbarNav {
    width: 260px;
  }
}

@media (max-width: 575.98px) {
  .px-5vw {
    padding-left: 2vw !important;
    padding-right: 2vw !important;
  }
  
  .header-logo {
    height: 32px;
    width: 32px;
  }
  
  .footer-logo {
    height: 40px;
    width: 40px;
  }
  
  #navbarNav {
    width: 240px;
  }
}
</style>