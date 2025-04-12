<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg custom-header">
      <div class="container-fluid px-7vw d-flex align-items-center">
        <router-link 
          to="/" 
          class="d-flex align-items-center text-decoration-none text-dark"
        >
          <img src="/dut_logo.jpg" alt="DUT Logo" class="header-logo me-3" />
          <div class="header-info">
            <div class="fw-bold" style="color: #4da0ff;">ĐẠI HỌC ĐÀ NẴNG</div>
            <div class="fw-bold text-danger">TRƯỜNG ĐẠI HỌC BÁCH KHOA</div>
            <hr class="hr-custom my-1" />
            <div class="fw-bold" style="color:#0B2942;">
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
                <i class="bi bi-house-fill me-1"></i> School Priority
              </a>
              <ul class="custom-dropdown-menu">
                <li><router-link class="dropdown-item" to="/school-priority">Tra cứu điểm ưu tiên khu vực</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown menu-item">
              <a class="nav-link dropdown-toggle custom-dropdown" href="#" role="button">
                <i class="bi bi-calculator-fill me-1"></i> Point Count
              </a>
              <ul class="custom-dropdown-menu">
                <li><router-link class="dropdown-item" to="/point-count">Tính điểm phương thức xét tuyển riêng</router-link></li>
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
  </div>
</template>

<script>
import { computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import store from '@/store'

export default {
  setup() {
    const router = useRouter()
    const isAuthenticated = computed(() => !!store.state.token)
    const userEmail = computed(() => store.state.user.email)

    const logout = () => {
      store.clearToken()
      router.push({ name: 'Login' })
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

      onBeforeUnmount(() => {
        window.removeEventListener('scroll', handleScroll)
      })
    })

    return { isAuthenticated, userEmail, logout }
  }
}
</script>

<style scoped>
.custom-header {
  background-color: #f0f0f0 !important;
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

.px-7vw {
  padding-left: 7vw !important;
  padding-right: 7vw !important;
}

.header-logo {
  height: 60px;
  width: auto;
}

.header-info {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
  font-size: 0.9rem;
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

</style>
