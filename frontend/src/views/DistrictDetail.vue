<template>
    <div class="container py-4">
      <div class="mb-4 text-center">
        <h2 class="fw-bold text-primary">
          Trường THPT trong Quận/Huyện: {{ district }}<span v-if="city"> - {{ city }}</span>
        </h2>
        <p class="text-muted">
          Khám phá các trường THPT hàng đầu tại khu vực {{ district }}<span v-if="city"> - {{ city }}</span>.
        </p>
      </div>
      
      <!-- Thanh tìm kiếm -->
      <div class="mb-4">
        <input type="text" class="form-control search-input" placeholder="Tìm kiếm trường..." v-model="query">
      </div>
      
      <!-- Danh sách trường -->
      <div class="row g-4">
        <div class="col-sm-6 col-md-4 col-lg-3 school-item" v-for="school in filteredSchools" :key="school.id">
          <div class="card h-100">
            <div class="card-body d-flex flex-column justify-content-center text-center">
              <h5 class="card-title mb-0">
                <router-link :to="`/school/${school.id}`" class="stretched-link text-decoration-none text-dark">
                  {{ school.name }}
                </router-link>
              </h5>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Nút quay lại -->
      <div class="text-center mt-4">
        <router-link to="/" class="btn btn-outline-primary px-4 py-2">Quay lại</router-link>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import config from '@/config/apiConfig';
  const BASE_API_URL = config?.BASE_API_URL ;
  export default {
    name: 'DistrictDetail',
    data() {
      return {
        district: "",
        city: "",
        schools: [],
        query: ''
      }
    },
    computed: {
      filteredSchools() {
        return this.schools.filter(s => s.name.toLowerCase().includes(this.query.toLowerCase()))
      }
    },
    mounted() {
      const districtId = this.$route.params.district_id
      axios.get(`${BASE_API_URL}/priorities/districts/${districtId}`)
        .then(res => {
          this.district = res.data.name
          this.city = res.data.city_name
        })
        .catch(err => console.error(err))
      axios.get(`${BASE_API_URL}/priorities/districts/${districtId}/schools`)
        .then(res => {
          this.schools = res.data
        })
        .catch(err => console.error(err))
    }
  }
  </script>
  
  <style scoped>
  body {
    background-color: #f8f9fa;
    color: #001f3f;
  }
  .search-input {
    border-radius: 5px;
    border: 1px solid #ced4da;
    padding: 0.5rem;
  }
  .card {
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  }
  .card:hover {
    transform: translateY(-5px);
  }
  </style>
  