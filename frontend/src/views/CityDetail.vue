<template>
    <div class="city-detail">
      <!-- Header với banner hoặc màu nền -->
      <section
        class="city-header py-5 text-white text-center"
        :style="{
          background: city.banner ? 'url(' + city.banner + ') center/cover' : '#001f3f'
        }"
      >
        <div class="container">
          <h1 class="display-4">{{ city.name }}</h1>
          <p class="lead">Khám phá danh sách các trường học hàng đầu tại {{ city.name }}</p>
        </div>
      </section>
  
      <!-- Danh sách trường -->
      <section class="school-list py-5">
        <div class="container">
          <div v-if="schools.length" class="row">
            <div class="col-md-6 col-lg-4 mb-4" v-for="school in schools" :key="school.id">
              <div class="card school-card h-100">
                <div class="card-body">
                  <h5 class="card-title">
                    <router-link :to="`/school/${school.id}`" class="stretched-link text-dark">
                      {{ school.name }}
                    </router-link>
                  </h5>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center">
            <p>Không có trường nào trong tỉnh/thành phố này.</p>
          </div>
          <div class="text-center mt-4">
            <router-link to="/" class="btn btn-outline-primary">Quay lại</router-link>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import config from '@/config/apiConfig';
  const BASE_API_URL = config?.BASE_API_URL ;
  export default {
    name: 'CityDetail',
    data() {
      return {
        city: {},
        schools: []
      }
    },
    mounted() {
      const cityId = this.$route.params.city_id
      axios.get(`${BASE_API_URL}/priorities/cities/{city_id}/${cityId}`)
        .then(res => {
          this.city = res.data
        })
        .catch(err => console.error(err))
      axios.get(`${BASE_API_URL}/priorities/cities/${cityId}/schools`)
        .then(res => {
          this.schools = res.data
        })
        .catch(err => console.error(err))
    }
  }
  </script>
  
  <style scoped>
  .city-header {
    background: #001f3f;
    color: #fff;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
  }
  
  .city-header h1 {
    font-weight: 700;
  }
  
  .school-card {
    border: none;
    border-radius: 10px;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .school-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  }
  </style>
  