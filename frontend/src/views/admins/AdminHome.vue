<template>
    <div class="admin-home">
      <div class="admin-page-header">
        <h2 class="admin-page-title">Dashboard</h2>
        <p class="admin-page-description">Chào mừng đến với hệ thống quản trị tuyển sinh</p>
      </div>
  
      <div class="row mt-4">
        <div class="col-md-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon">
              <i class="bi bi-people-fill"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ userCount }}</h3>
              <p class="admin-stat-label">Người dùng</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-success">
              <i class="bi bi-mortarboard-fill"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ currentVisitors }}</h3>
              <p class="admin-stat-label">Đang truy cập</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="admin-stat-card">
            <div class="admin-stat-icon bg-warning">
              <i class="bi bi-bar-chart-fill"></i>
            </div>
            <div class="admin-stat-content">
              <h3 class="admin-stat-value">{{ totalVisitors }}</h3>
              <p class="admin-stat-label">Tổng lượt truy cập</p>
            </div>
          </div>
        </div>
      </div>
  
      <div class="row mt-4">
        <div class="col-12">
          <div class="admin-card">
            <h3 class="admin-card-title">Chức năng quản trị</h3>
            <div class="admin-actions">
              <router-link to="/admins/users" class="admin-action-btn">
                <i class="bi bi-people-fill me-2"></i>
                Quản lý người dùng
              </router-link>
              
              <router-link to="/admins/users/create" class="admin-action-btn">
                <i class="bi bi-person-plus-fill me-2"></i>
                Thêm người dùng mới
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import UserController from '@/controllers/admins/UserController'
  import axios from 'axios'
  import config from '@/config/apiConfig'
  
  const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'
  
  export default {
    name: 'AdminHome',
    setup() {
      const userCount = ref(0)
      const currentVisitors = ref(0)
      const totalVisitors = ref(0)
  
      // Hàm lấy số lượng người dùng
      const fetchUserCount = async () => {
        try {
          const users = await UserController.getAllUsers()
          userCount.value = users.length
        } catch (error) {
          console.error('Error fetching user count:', error)
        }
      }
  
      // Hàm lấy thông tin người truy cập
      const fetchVisitorStats = async () => {
        try {
          const response = await axios.get(`${BASE_API_URL}/visitors/stats`, {
            withCredentials: true
          })
          
          if (response.data) {
            currentVisitors.value = response.data.current_visitors
            totalVisitors.value = response.data.total_visitors
          }
        } catch (error) {
          console.error('Error fetching visitor stats:', error)
        }
      }
  
      onMounted(() => {
        fetchUserCount()
        fetchVisitorStats()
      })
  
      return {
        userCount,
        currentVisitors,
        totalVisitors
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-page-header {
    margin-bottom: 2rem;
  }
  
  .admin-page-title {
    font-size: 1.75rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .admin-page-description {
    color: #6c757d;
    font-size: 0.95rem;
  }
  
  .admin-stat-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    display: flex;
    align-items: center;
    height: 100%;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .admin-stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  }
  
  .admin-stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #4da0ff;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
    color: #fff;
    font-size: 1.75rem;
  }
  
  .admin-stat-content {
    flex: 1;
  }
  
  .admin-stat-value {
    font-size: 2rem;
    font-weight: 600;
    margin: 0;
    color: #0B2942;
  }
  
  .admin-stat-label {
    font-size: 0.9rem;
    color: #6c757d;
    margin-top: 0.25rem;
    margin-bottom: 0;
  }
  
  .admin-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .admin-card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .admin-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .admin-action-btn {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
  }
  
  .admin-action-btn:hover {
    background-color: #4da0ff;
  }
  
  .bg-success {
    background-color: #28a745 !important;
  }
  
  .bg-warning {
    background-color: #ffc107 !important;
  }
  
  @media (max-width: 768px) {
    .admin-stat-card {
      margin-bottom: 1rem;
    }
  }
  </style>