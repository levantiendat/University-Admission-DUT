<template>
    <div class="container">
      <h2>Tra cứu khu vực ưu tiên của trường THPT</h2>
      <p class="mb-4">Dữ liệu tính đến ngày 30.04.2024</p>
  
      <!-- Thanh tìm kiếm toàn cục -->
      <div class="mb-4 position-relative">
        <label for="globalSearch" class="form-label">
          Tìm kiếm nhanh (theo tên trường, quận/huyện hoặc tỉnh/thành phố)
        </label>
        <input type="text" id="globalSearch" class="form-control" placeholder="Nhập từ khóa..." v-model="globalQuery">
        <div class="list-group" style="position: absolute; width: 100%; top: 100%; z-index: 1000;">
          <a v-for="item in suggestions" :key="item.id" class="list-group-item list-group-item-action"
             href="#" @click.prevent="goToDetail(item)">
            <span v-if="item.type==='cities'">[Tỉnh/TP] {{ item.name }}</span>
            <span v-else-if="item.type==='districts'">[Quận/Huyện] {{ item.name }}</span>
            <span v-else-if="item.type==='schools'">[Trường] {{ item.name }}</span>
          </a>
        </div>
      </div>
  
      <!-- Form tìm kiếm theo dropdown -->
      <form @submit.prevent="searchSchool">
        <div class="mb-3">
          <label for="city" class="form-label">Chọn Tỉnh/Thành phố</label>
          <select class="form-select selectpicker" id="city" v-model="selectedCity" @change="loadDistricts" data-live-search="true" data-width="100%">
            <option value="">-- Chọn Tỉnh/Thành phố --</option>
            <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="district" class="form-label">Chọn Quận/Huyện</label>
          <select class="form-select selectpicker" id="district" v-model="selectedDistrict" @change="loadSchools" :disabled="!districts.length" data-live-search="true" data-width="100%">
            <option value="">-- Chọn Quận/Huyện --</option>
            <option v-for="district in districts" :key="district.id" :value="district.id">{{ district.name }}</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="school" class="form-label">Chọn Trường THPT</label>
          <select class="form-select selectpicker" id="school" v-model="selectedSchool" :disabled="!schools.length" data-live-search="true" data-width="100%">
            <option value="">-- Chọn Trường THPT --</option>
            <option v-for="school in schools" :key="school.id" :value="school.id">{{ school.name }}</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Tra cứu</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import debounce from 'lodash/debounce'
  import config from '@/config/apiConfig';
  const BASE_API_URL = config?.BASE_API_URL ;
  
  export default {
    name: 'Home',
    data() {
      return {
        cities: [],
        districts: [],
        schools: [],
        selectedCity: '',
        selectedDistrict: '',
        selectedSchool: '',
        globalQuery: '',
        suggestions: []
      }
    },
    watch: {
      globalQuery(newQuery) {
        this.debouncedSearchGlobal()
      }
    },
    methods: {
      debouncedSearchGlobal: debounce(function() {
        if (this.globalQuery.length >= 2) {
          axios
            .get(`${BASE_API_URL}/priorities/search?q=${encodeURIComponent(this.globalQuery)}`)
            .then(res => {
              this.suggestions = res.data
            })
            .catch(err => console.error(err))
        } else {
          this.suggestions = []
        }
      }, 300),
      loadCities() {
        axios
          .get(`${BASE_API_URL}/priorities/cities`)
          .then(res => {
            this.cities = res.data;
            this.$nextTick(() => {
              $('.selectpicker').selectpicker('refresh')
            })
          })
          .catch(err => console.error(err))
      },
      loadDistricts() {
        this.selectedDistrict = ''
        this.schools = []
        if (this.selectedCity) {
          axios
            .get(`${BASE_API_URL}/priorities/cities/${this.selectedCity}/districts`)
            .then(res => {
              this.districts = res.data;
              this.$nextTick(() => {
                $('.selectpicker').selectpicker('refresh')
              })
            })
            .catch(err => console.error(err))
        } else {
          this.districts = []
        }
      },
      loadSchools() {
        this.selectedSchool = ''
        if (this.selectedDistrict) {
          axios
            .get(`${BASE_API_URL}/priorities/districts/${this.selectedDistrict}/schools`)
            .then(res => {
              this.schools = res.data;
              this.$nextTick(() => {
                $('.selectpicker').selectpicker('refresh')
              })
            })
            .catch(err => console.error(err))
        } else {
          this.schools = []
        }
      },
      searchSchool() {
        if (this.selectedSchool) {
          this.$router.push(`/school/${this.selectedSchool}`)
        }
      },
      goToDetail(item) {
        if (item.type === 'city') {
          this.$router.push(`/city/${item.id}`)
        } else if (item.type === 'district') {
          this.$router.push(`/district/${item.id}`)
        } else if (item.type === 'school') {
          this.$router.push(`/school/${item.id}`)
        }
      }
    },
    mounted() {
      // Load danh sách tỉnh/thành phố khi component được mount
      this.loadCities()
      this.$nextTick(() => {
        $('.selectpicker').selectpicker()
      })
    }
  }
  </script>
  
  <style scoped>
  .container {
    padding-top: 20px;
  }
  </style>
  