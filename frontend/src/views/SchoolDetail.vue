<template>
    <div class="container py-4">
      <h2 class="mb-4 text-center">Chi tiết Trường</h2>
      <div class="card school-card">
        <div class="school-card-header">
          <h4>{{ school.name }}</h4>
        </div>
        <div class="school-card-body">
          <div class="school-detail-item">
            <strong>Khu vực ưu tiên:</strong>
            <span class="badge bg-info text-dark">{{ school.priority_area }}</span>
          </div>
          <div class="school-detail-item">
            <strong>Địa chỉ:</strong> {{ school.address }}
          </div>
          <div class="school-detail-item" v-if="school.district_name">
            <strong>Quận/Huyện:</strong> {{ school.district_name }}
          </div class="school-detail-item">
          <div class="school-detail-item" v-if="school.city_name">
            <strong>Tỉnh/Thành phố:</strong> {{ school.city_name }}
          </div class="school-detail-item">
        </div>
        <div class="school-card-footer">
          <router-link to="/" class="btn btn-outline-primary btn-back">Quay lại</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import config from '@/config/apiConfig';
  const BASE_API_URL = config?.BASE_API_URL;
  export default {
    name: 'SchoolDetail',
    data() {
      return {
        school: {}
      }
    },
    mounted() {
      const schoolId = this.$route.params.school_id
      axios.get(`${BASE_API_URL}/priorities/schools/${schoolId}`)
        .then(res => {
          this.school = res.data
        })
        .catch(err => console.error(err))
    }
  }
  </script>
  
  <style scoped>
  .school-card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
  }
  .school-card-header {
    background: linear-gradient(135deg, #001f3f, #003366);
    color: #ffffff;
    padding: 1rem 1.5rem;
  }
  .school-card-body {
    padding: 1.5rem;
    background-color: #ffffff;
    color: #001f3f;
    font-size: 1.1rem;
  }
  .school-detail-item {
    margin-bottom: 0.75rem;
  }
  .school-detail-item strong {
    width: 160px;
    display: inline-block;
  }
  .school-card-footer {
    background-color: #f8f9fa;
    padding: 1rem 1.5rem;
    text-align: right;
  }
  .btn-back:hover {
    background-color: #003366;
    transform: translateY(-2px);
  }
  </style>
  