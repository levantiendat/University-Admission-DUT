<template>
  <div class="admin-layout">
    <!-- Admin Header -->
    <header class="admin-header">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col">
            <div class="d-flex align-items-center">
              <h1 class="admin-title">
                <i class="bi bi-gear-fill me-2"></i>Quản trị hệ thống
              </h1>
              <!-- Thêm nút trở về trang chính và nút đăng xuất -->
              <div class="header-actions ms-4">
                <router-link to="/" class="header-action-btn" title="Trở về trang chính">
                  <i class="bi bi-house-door"></i>
                </router-link>
                <button @click="logout" class="header-action-btn ms-3" title="Đăng xuất">
                  <i class="bi bi-box-arrow-right"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="col-auto">
            <div class="dropdown">
              <button class="admin-user-btn" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="bi bi-person-circle me-2"></i>{{ userEmail }}
              </button>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="openProfileSettings">
                    <i class="bi bi-person-gear me-2"></i>Thiết lập tài khoản
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="openChangePassword">
                    <i class="bi bi-key me-2"></i>Đổi mật khẩu
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="admin-container">
      <!-- Admin Sidebar -->
      <aside class="admin-sidebar">
        <div class="admin-logo mb-4">
          <img src="/dut_logo.png" alt="DUT Logo" class="admin-logo-img" />
          <div class="admin-logo-text">
            <div class="admin-logo-title">ĐẠI HỌC ĐÀ NẴNG</div>
            <div class="admin-logo-subtitle">TRƯỜNG ĐẠI HỌC BÁCH KHOA</div>
          </div>
        </div>
        
        <nav class="admin-nav">
          <router-link to="/admins" class="admin-nav-link" exact-active-class="active">
            <i class="bi bi-speedometer2 me-2"></i>Tổng quan
          </router-link>
          
          <!-- User Management -->
          <div class="nav-section">
            <h6 class="nav-section-title">Quản lý người dùng</h6>
            <router-link to="/admins/users" class="admin-nav-link" active-class="active">
              <i class="bi bi-people-fill me-2"></i>Danh sách người dùng
            </router-link>
          </div>
          
          <!-- Academic Management -->
          <div class="nav-section">
            <h6 class="nav-section-title">Quản lý học thuật</h6>
            <router-link to="/admins/faculties" class="admin-nav-link" active-class="active">
              <i class="bi bi-building me-2"></i>Quản lý khoa
            </router-link>
            <router-link to="/admins/majors" class="admin-nav-link" active-class="active">
              <i class="bi bi-book me-2"></i>Quản lý ngành
            </router-link>
          </div>

          <div class="nav-section">
            <h6 class="nav-section-title">Quản lý tuyển sinh</h6>
            <router-link to="/admins/admission-methods" class="admin-nav-link" active-class="active">
              <i class="bi bi-clipboard-check me-2"></i>Phương thức xét tuyển
            </router-link>
            <router-link to="/admins/admission-descriptions" class="admin-nav-link" active-class="active">
              <i class="bi bi-award me-2"></i>Lĩnh vực/môn học xét tuyển Thẳng / Riêng
            </router-link>
            <router-link to="/admins/convert-points" class="admin-nav-link" active-class="active">
              <i class="bi bi-calculator me-2"></i>Quy đổi điểm
            </router-link>
          </div>

          <div class="nav-section">
            <h6 class="nav-section-title">Quản lý môn thi và tổ hợp</h6>
            <router-link to="/admins/subjects" class="admin-nav-link" active-class="active">
              <i class="bi bi-journal-text me-2"></i>Quản lý môn thi
            </router-link>
            <router-link to="/admins/subject-groups" class="admin-nav-link" active-class="active">
              <i class="bi bi-diagram-3 me-2"></i>Quản lý tổ hợp môn thi
            </router-link>
          </div>

          <div class="nav-section">
            <h6 class="nav-section-title">Điểm chuẩn</h6>
            <router-link to="/admins/previous-admissions" class="admin-nav-link" active-class="active">
              <i class="bi bi-bar-chart-line me-2"></i>Điểm chuẩn các năm trước
            </router-link>
          </div>
          
          <div class="nav-section">
            <h6 class="nav-section-title">Quản lý chương trình đào tạo</h6>
            <router-link to="/admins/major-courses" class="admin-nav-link" active-class="active">
              <i class="bi bi-mortarboard-fill me-2"></i>Khung chương trình đào tạo
            </router-link>
            <router-link to="/admins/courses" class="admin-nav-link" active-class="active">
              <i class="bi bi-journals me-2"></i>Lớp học phần
            </router-link>
          </div>
          
          <div class="nav-section">
            <h6 class="nav-section-title">Quản lý khu vực ưu tiên</h6>
            <router-link to="/admins/school-priorities" class="admin-nav-link" active-class="active">
              <i class="bi bi-geo-alt-fill me-2"></i>Khu vực ưu tiên
            </router-link>
          </div>

          <div class="nav-section">
            <h6 class="nav-section-title">Quản lý hỏi đáp</h6>
            <router-link to="/admins/qna" class="admin-nav-link" active-class="active">
              <i class="bi bi-chat-left-dots me-2"></i>Câu hỏi và phản hồi
            </router-link>
          </div>
        </nav>
      </aside>

      <!-- Admin Content -->
      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import store from '@/store'
import UserController from '@/controllers/userController'

export default {
  name: 'AdminLayout',
  setup() {
    const router = useRouter()
    const userEmail = ref('')

    const logout = () => {
      store.clearToken()
      router.push({ name: 'Login' })
    }
    
    // Lấy thông tin email của người dùng hiện tại
    const getCurrentUserEmail = async () => {
      try {
        const user = await UserController.getCurrentUser()
        if (user) {
          userEmail.value = user.email
        }
      } catch (error) {
        console.error('Error getting current user:', error)
      }
    }

    onMounted(() => {
      getCurrentUserEmail()
    })

    return {
      userEmail,
      logout
    }
  }
}
</script>

<style scoped>
/* Full page layout */
.admin-layout {
  min-height: 100vh;
  background-color: #f0f4f8;
  display: flex;
  flex-direction: column;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.admin-header {
  background-color: #0B2942;
  color: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1030;
  height: 70px;
}

.admin-title {
  font-size: 1.5rem;
  margin: 0;
  color: #fff;
}

/* New styles for header action buttons */
.header-actions {
  display: flex;
  align-items: center;
}

.header-action-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  width: 40px;
  height: 40px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s;
  text-decoration: none;
}

.header-action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  transform: translateY(-2px);
}

/* Rest of existing styles */
.admin-user-btn {
  background: none;
  border: none;
  color: #fff;
  display: flex;
  align-items: center;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.admin-user-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.admin-container {
  display: flex;
  flex-grow: 1;
  margin-top: 70px;
}

.admin-sidebar {
  width: 280px;
  background-color: #0B2942;
  color: #fff;
  padding: 2rem 1rem;
  position: fixed;
  top: 70px;
  bottom: 0;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.admin-logo {
  display: flex;
  align-items: center;
  padding: 0 1rem;
}

.admin-logo-img {
  width: 50px;
  height: auto;
  margin-right: 10px;
}

.admin-logo-text {
  display: flex;
  flex-direction: column;
}

.admin-logo-title {
  font-size: 0.8rem;
  font-weight: bold;
  color: #4da0ff;
}

.admin-logo-subtitle {
  font-size: 0.8rem;
  font-weight: bold;
  color: #ff4d4d;
}

.admin-nav {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
}

.nav-section {
  margin-top: 1.5rem;
}

.nav-section-title {
  color: #8395a7;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05rem;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 0.5rem;
}

.admin-nav-link {
  color: #e0e0e0;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  transition: all 0.3s;
}

.admin-nav-link:hover, .admin-nav-link.active {
  background-color: #4da0ff;
  color: #fff;
}

.admin-content {
  flex-grow: 1;
  padding: 2rem;
  margin-left: 280px;
  transition: margin-left 0.3s;
  overflow-y: auto;
}

.dropdown-menu {
  background-color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  margin-top: 8px;
}

.dropdown-item {
  padding: 0.75rem 1.5rem;
  color: #333;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background-color: #f0f4f8;
  color: #0B2942;
}

/* Mobile responsive */
@media (max-width: 992px) {
  .admin-sidebar {
    transform: translateX(-100%);
    z-index: 1040;
  }

  .admin-sidebar.show {
    transform: translateX(0);
  }

  .admin-content {
    margin-left: 0;
  }
}
</style>