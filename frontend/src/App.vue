<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg custom-header">
      <div class="container-fluid px-5vw d-flex align-items-center">
        <router-link 
          to="/" 
          class="d-flex align-items-center text-decoration-none text-dark"
        >
          <img src="/dut_logo.png" alt="DUT Logo" class="header-logo me-3" />
          <div class="header-info">
            <div class="fw-bold" style="color: #4da0ff;">ĐẠI HỌC ĐÀ NẴNG</div>
            <div class="fw-bold text-danger">TRƯỜNG ĐẠI HỌC BÁCH KHOA</div>
            <hr class="hr-custom my-1" />
            <div class="fw-bold header-info-eng" style="color:#0B2942;">
              UNIVERSITY OF SCIENCE AND TECHNOLOGY - UD
            </div>
          </div>
        </router-link>

        <button 
          class="navbar-toggler ms-auto" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav" 
          aria-controls="navbarNav" 
          aria-expanded="false" 
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse ms-auto" id="navbarNav">
          <ul class="navbar-nav ms-auto main-menu">
            <!-- Các mục luôn hiển thị -->
            <li class="nav-item dropdown menu-item">
              <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                <i class="bi bi-house-fill me-1"></i> Home
              </a>
              <ul class="custom-dropdown-menu">
                <li><router-link class="dropdown-item" to="/">Giới thiệu</router-link></li>
                <li><router-link class="dropdown-item" to="/">Liên hệ</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item">
              <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                <i class="bi bi-mortarboard-fill me-1"></i> Tuyển sinh năm 2025
              </a>
              <ul class="custom-dropdown-menu">
                <li><router-link class="dropdown-item" to="/admission">Thông tin tuyển sinh chung</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/xettuyenthang">Xét tuyển thẳng theo quy chế của Bộ Giáo dục và đào tạo</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/xettuyenrieng">Xét tuyển riêng theo đề án tuyển sinh</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/totnghiep_thpt">Xét tuyển theo điểm thi tốt nghiệp THPT</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/hocba_thpt">Xét tuyển theo điểm học tập cấp THPT</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/danhgianangluc">Xét tuyển theo kết quả kỳ thi Đánh Giá Năng Lực của ĐHQG TPHCM</router-link></li>
                <li><router-link class="dropdown-item" to="/admission/danhgiatuduy">Xét tuyển theo điểm thi kỳ thi Đánh Giá Tư Duy của ĐHBK Hà Nội</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item">
              <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                <i class="bi bi-house-fill me-1"></i> Công cụ hỗ trợ
              </a>
              <ul class="custom-dropdown-menu">
                <li><router-link class="dropdown-item" to="/school-priority">Tra cứu điểm ưu tiên khu vực</router-link></li>
                <li><router-link class="dropdown-item" to="/point-count">Tính điểm phương thức xét tuyển riêng</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item">
              <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                <i class="bi bi-calculator-fill me-1"></i> Thống kê
              </a>
              <ul class="custom-dropdown-menu">
                <li><router-link class="dropdown-item" to="/statistics/previous-admission">Điểm chuẩn các năm trước</router-link></li>
                <li><router-link class="dropdown-item" to="/statistics/pre-admitted-student">Thống kê sinh viên nhập học các năm trước</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item">
              <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                <i class="bi bi-laptop-fill me-1"></i> Chương trình đào tạo
              </a>
              <ul class="custom-dropdown-menu">
                <li><router-link class="dropdown-item" to="/ctdt">Khoa Công nghệ thông tin</router-link></li>
              </ul>
            </li>

            <!-- Nếu đã đăng nhập -->
            <template v-if="isAuthenticated">
              <li class="nav-item dropdown menu-item">
                <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                  <i class="bi bi-chat-left-text-fill me-1"></i> Tư vấn tuyển sinh
                </a>
                <ul class="custom-dropdown-menu">
                  <li><router-link class="dropdown-item" to="/qa">Q&A</router-link></li>
                </ul>
              </li>
              <li class="nav-item dropdown menu-item">
                <a class="nav-link dropdown-toggle custom-dropdown d-flex align-items-center" href="#" role="button">
                  <i class="bi bi-person-circle me-1"></i><span>{{ userEmail }}</span>
                </a>
                <ul class="custom-dropdown-menu dropdown-menu-end">
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="logout">
                      <i class="bi bi-box-arrow-right me-1"></i> Đăng xuất
                    </a>
                  </li>
                </ul>
              </li>
            </template>

            <!-- Nếu chưa đăng nhập -->
            <template v-else>
              <li class="nav-item dropdown menu-item">
                <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                  <i class="bi bi-person-circle me-1"></i> Tài khoản
                </a>
                <ul class="custom-dropdown-menu dropdown-menu-end">
                  <li>
                    <router-link class="dropdown-item" to="/login">
                      <i class="bi bi-box-arrow-in-right me-1"></i> Đăng nhập
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/register">
                      <i class="bi bi-person-plus me-1"></i> Đăng ký
                    </router-link>
                  </li>
                </ul>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
    <router-view/>
    <footer class="custom-footer">
      <div class="container-fluid px-5vw py-4">
        <div class="row">
          <div class="col-lg-4 mb-4 mb-lg-0">
            <div class="d-flex align-items-center mb-3">
              <img src="/dut_logo.png" alt="DUT Logo" class="footer-logo me-3" />
              <div class="footer-info">
                <div class="fw-bold" style="color: #4da0ff;">ĐẠI HỌC ĐÀ NẴNG</div>
                <div class="fw-bold text-danger">TRƯỜNG ĐẠI HỌC BÁCH KHOA</div>
              </div>
            </div>
            <p><i class="bi bi-geo-alt-fill me-2"></i> 54 Nguyễn Lương Bằng, Liên Chiểu, Đà Nẵng</p>
            <p><i class="bi bi-telephone-fill me-2"></i> (0236) 3842 308</p>
            <p><i class="bi bi-envelope-fill me-2"></i> tuyensinh@dut.udn.vn</p>
          </div>
          
          <div class="col-lg-4 mb-4 mb-lg-0">
            <h5 class="footer-heading">Liên kết hữu ích</h5>
            <ul class="footer-links">
              <li><a href="https://dut.udn.vn/" target="_blank">Website chính thức DUT</a></li>
              <li><a href="https://tuyensinh.dut.udn.vn/" target="_blank">Cổng thông tin tuyển sinh</a></li>
              <li><a href="https://www.facebook.com/DUTpage/" target="_blank">Facebook tuyển sinh</a></li>
            </ul>
          </div>
          
          <div class="col-lg-4">
            <h5 class="footer-heading">Thống kê truy cập</h5>
            <div class="visitor-stats">
              <p><i class="bi bi-people-fill me-2"></i> Đang truy cập: <span class="fw-bold">{{ currentVisitors }}</span></p>
              <p><i class="bi bi-bar-chart-fill me-2"></i> Tổng lượt truy cập: <span class="fw-bold">{{ totalVisitors }}</span></p>
            </div>
            <div class="social-links mt-3">
              <a href="https://www.facebook.com/bachkhoaDUT" target="_blank" class="social-icon">
                <i class="bi bi-facebook"></i>
              </a>
              <a href="https://www.youtube.com/@DUTMedia" target="_blank" class="social-icon">
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
  </div>
</template>

<script>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import store from '@/store'
import axios from 'axios'
import config from '@/config/apiConfig'  // nếu bạn đã tách riêng file cấu hình base API

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

export default {
  setup() {
    const router = useRouter()
    const isAuthenticated = computed(() => !!store.state.token)
    const userEmail = computed(() => store.state.user.email)
    
    // Thêm biến để lưu trữ số liệu người truy cập
    const currentVisitors = ref(0)
    const totalVisitors = ref(0)
    let heartbeatInterval = null

    const logout = () => {
      store.clearToken()
      router.push({ name: 'Login' })
    }

    // Hàm lấy thông tin người truy cập
    const fetchVisitorStats = async () => {
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
      try {
        await axios.post(`${BASE_API_URL}/visitors/heartbeat`, {}, {
          withCredentials: true
        })
      } catch (error) {
        console.error('Error sending heartbeat:', error)
      }
    }

    onMounted(() => {
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

      // Lấy thông tin người truy cập khi trang được tải
      fetchVisitorStats()
      
      // Thiết lập heartbeat mỗi 5 phút để duy trì session và cập nhật số liệu
      heartbeatInterval = setInterval(() => {
        sendHeartbeat()
        fetchVisitorStats()
      }, 5 * 60 * 1000) // 5 phút

      onBeforeUnmount(() => {
        window.removeEventListener('scroll', handleScroll)
        // Xóa interval khi component unmount
        if (heartbeatInterval) {
          clearInterval(heartbeatInterval)
        }
      })
    })

    return { 
      isAuthenticated, 
      userEmail, 
      logout,
      currentVisitors,
      totalVisitors
    }
  }
}
</script>

<style scoped>
.custom-header {
  background-color: #efeff38f !important;
  position: sticky;
  top: 0;
  z-index: 1050;
  transition: all 0.3s ease;
}

.custom-header.scrolled {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.8) !important;
  border-radius: 20px 20px 20px 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  top: 10px;
  margin-left: 3%;
  margin-right: 3%;
}

.px-5vw {
  padding-left: 5vw !important;
  padding-right: 5vw !important;
}

.header-logo {
  height: 60px;
  width: auto;
}

.header-info {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
  font-size: 0.7rem;
}

.header-info-eng {
  font-size: 0.5rem;
}

.hr-custom {
  border: none;
  border-top: 2px solid #0B2942;
  width: 100%;
  margin: 3px 0;
}

.main-menu {
  display: flex;
  align-items: center;
}

.menu-item {
  position: relative;
  margin: 0 2px;
}

.custom-dropdown, .custom-nav-link {
  position: relative;
  padding-bottom: 0.5rem !important;
  cursor: pointer;
}

.custom-dropdown:hover, .custom-nav-link:hover {
  color: #4da0ff !important;
}

.custom-dropdown::after, .custom-nav-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0;
  height: 3px;
  background-color: #0B2942;
  transition: width 0.3s ease;
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
  min-width: 250px;
  padding: 0.5rem 0;
  margin: 0;
  background-color: #f5f5f5;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 0 0 0.25rem 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.menu-item:hover .custom-dropdown-menu {
  display: block;
}

.custom-dropdown-menu li {
  border-bottom: 1px solid #e0e0e0;
}

.custom-dropdown-menu li:last-child {
  border-bottom: none;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.75rem 1.5rem;
  font-weight: 400;
  color: #212529;
  text-align: left;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.2s ease;
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
.custom-footer {
  background-color: #0B2942;
  color: #fff;
  margin-top: 2rem;
}

.footer-logo {
  height: 50px;
  width: auto;
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
</style>
