<template>
  <div class="container modern-container bg-light rounded-4 shadow-sm p-4">
    <h2 class="main-header text-primary">🎓 Tra cứu khu vực ưu tiên của trường THPT</h2>
    <p class="text-muted mb-4">Dữ liệu tính đến ngày 30.04.2024</p>

    <!-- Thanh tìm kiếm toàn cục -->
    <div class="mb-4 position-relative">
      <label for="globalSearch" class="form-label fw-semibold">🔍 Tìm kiếm nhanh</label>
      <input type="text" id="globalSearch" class="form-control rounded-3 shadow-sm" placeholder="Nhập từ khóa..." v-model="globalQuery" />
      <div class="list-group shadow-sm mt-1 position-absolute w-100 z-3">
        <a
          v-for="item in suggestions"
          :key="item.id"
          class="list-group-item list-group-item-action"
          href="#"
          @click.prevent="goToDetail(item)"
        >
          <span v-if="item.type === 'cities'">[Tỉnh/TP] {{ item.name }}</span>
          <span v-else-if="item.type === 'districts'">[Quận/Huyện] {{ item.name }}</span>
          <span v-else-if="item.type === 'schools'">[Trường] {{ item.name }}</span>
        </a>
      </div>
    </div>

    <!-- Form tìm kiếm theo dropdown -->
    <form @submit.prevent="searchSchool">
      <div class="mb-3">
        <label for="city" class="form-label fw-semibold">🏙️ Chọn Tỉnh/Thành phố</label>
        <select class="form-select selectpicker" id="city" v-model="selectedCity" @change="loadDistricts" data-live-search="true" data-width="100%">
            <option value="">-- Chọn Tỉnh/Thành phố --</option>
            <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="district" class="form-label fw-semibold">🏞️ Chọn Quận/Huyện</label>
        <select class="form-select selectpicker" id="district" v-model="selectedDistrict" @change="loadSchools" :disabled="!districts.length" data-live-search="true" data-width="100%">
          <option value="">-- Chọn Quận/Huyện --</option>
          <option v-for="district in districts" :key="district.id" :value="district.id">{{ district.name }}</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="school" class="form-label fw-semibold">🏫 Chọn Trường THPT</label>
        <select class="form-select selectpicker" id="school" v-model="selectedSchool" :disabled="!schools.length" data-live-search="true" data-width="100%">
          <option value="">-- Chọn Trường THPT --</option>
          <option v-for="school in schools" :key="school.id" :value="school.id">{{ school.name }}</option>
        </select>
      </div>

      <button type="submit" class="btn modern-btn rounded-3 px-4 py-2 fw-bold">🔎 Tra cứu</button>
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
        cities: [],
        districts: [],
        schools: [],
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
              this.cities = res.data.cities;
              this.districts = res.data.districts;
              this.schools = res.data.schools;

              const citySuggestions = this.cities.map(item => ({
                id: item.id,
                name: item.name,
                type: 'cities'
              }));
              const districtSuggestions = this.districts.map(item => ({
                id: item.id,
                name: item.name,
                type: 'districts'
              }));
              const schoolSuggestions = this.schools.map(item => ({
                id: item.id,
                name: item.name,
                type: 'schools'
              }));

              this.suggestions = [...citySuggestions, ...districtSuggestions, ...schoolSuggestions];
              })
          .catch(err => console.error(err));
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

.main-header {
  font-size: 1.8rem;
  font-weight: 700;
  color: #003366;
}

.bg-light {
  background-color: #f5f5f5 !important;
}

.modern-btn {
  background-color: #7e57c2;
  color: white;
  border: none;
  transition: 0.3s ease;
}

.modern-btn:hover {
  background-color: #6741b0;
  color: #fff;
}

.form-control,
.form-select {
  border-radius: 0.75rem;
  border: 1px solid #ccc;
}

label.form-label {
  color: #003366;
  font-weight: 600;
}

.list-group-item {
  border-radius: 0.5rem !important;
  margin-bottom: 2px;
}
</style>
  