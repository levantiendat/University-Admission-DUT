<template>
  <div class="pre-admission-container">
    <!-- SEO-friendly header section -->
    <div class="header-section">
      <div class="container">
        <h1 class="main-title">Điểm Chuẩn Các Năm Trước</h1>
        <meta name="description" content="Tham khảo điểm chuẩn các năm trường Đại học Bách khoa Đà Nẵng để chuẩn bị tốt nhất cho kỳ thi sắp tới">
        <p class="subtitle">Tham khảo điểm chuẩn các năm để chuẩn bị tốt nhất cho kỳ thi sắp tới</p>
        
        <div class="view-controls">
          <div class="display-type">
            <button 
              :class="['btn', viewMode === 'table' ? 'btn-success' : 'btn-outline-success']" 
              @click="setViewMode('table')"
            >
              <i class="fas fa-table"></i> Xem dạng bảng
            </button>
            <button 
              :class="['btn', viewMode === 'chart' ? 'btn-success' : 'btn-outline-success']" 
              @click="setViewMode('chart')"
            >
              <i class="fas fa-chart-bar"></i> Xem dạng biểu đồ
            </button>
          </div>
          
          <div v-if="viewMode === 'chart'" class="chart-type">
            <div class="btn-group">
              <button 
                :class="['btn', chartViewType === 'major' ? 'btn-success' : 'btn-outline-success']"
                @click="setChartViewType('major')"
              >
                Theo ngành
              </button>
              <button 
                :class="['btn', chartViewType === 'faculty' ? 'btn-success' : 'btn-outline-success']"
                @click="setChartViewType('faculty')"
              >
                Theo khoa
              </button>
              <button 
                :class="['btn', chartViewType === 'university' ? 'btn-success' : 'btn-outline-success']"
                @click="setChartViewType('university')"
              >
                Toàn trường
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="content-section container">
      <!-- Loading indicator -->
      <div v-if="loading" class="loading-container">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Đang tải...</span>
        </div>
        <p>Đang tải dữ liệu...</p>
      </div>
      
      <!-- Error message -->
      <div v-else-if="error" class="error-container alert alert-danger">
        <p><strong>Có lỗi xảy ra:</strong> {{ error }}</p>
        <button class="btn btn-outline-danger" @click="fetchData">
          <i class="fas fa-sync-alt"></i> Thử lại
        </button>
      </div>
      
      <!-- TABLE VIEW -->
      <div v-else-if="viewMode === 'table'" class="table-container no-copy">
        <div class="filters mb-4">
          <div class="row">
            <div class="col-md-4">
              <div class="form-group">
                <label for="faculty-filter">Lọc theo khoa:</label>
                <select id="faculty-filter" class="form-select" v-model="selectedFaculty">
                  <option value="">Tất cả các khoa</option>
                  <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                    {{ faculty.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="search-filter">Tìm kiếm ngành:</label>
                <input
                  type="text"
                  id="search-filter"
                  class="form-control"
                  v-model="searchTerm"
                  placeholder="Nhập tên hoặc mã ngành..."
                />
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="year-filter">Hiển thị năm:</label>
                <div class="d-flex">
                  <div class="form-check me-3" v-for="year in availableYears" :key="year">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      :id="`year-${year}`"
                      :value="year"
                      v-model="selectedYears"
                    />
                    <label class="form-check-label" :for="`year-${year}`">{{ year }}</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="table-responsive">
          <table class="table table-striped table-hover table-bordered">
            <thead>
              <tr class="bg-primary text-white">
                <th rowspan="2" class="align-middle">STT</th>
                <th rowspan="2" class="align-middle">Ngành</th>
                <th rowspan="2" class="align-middle">Mã ngành</th>
                <!-- Header for each admission method -->
                <th v-for="method in displayedMethods" :key="`header-${method.id}`" 
                    :colspan="selectedYears.length" 
                    class="text-center method-header">
                  {{ method.name }} ({{ getMaxScoreForMethod(method.id) }} điểm)
                </th>
              </tr>
              <tr class="bg-info text-white">
                <!-- Header for each year under each method -->
                <template v-for="method in displayedMethods" :key="`years-${method.id}`">
                  <th v-for="year in selectedYears" :key="`year-${method.id}-${year}`" class="text-center year-header">
                    {{ year }}
                  </th>
                </template>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(major, index) in filteredMajors" :key="major.id">
                <td>{{ index + 1 }}</td>
                <td>{{ major.name }}</td>
                <td>{{ major.major_code }}</td>
                <!-- Data for each admission method and year -->
                <template v-for="method in displayedMethods" :key="`data-method-${method.id}`">
                  <td v-for="year in selectedYears" :key="`data-${method.id}-${year}`" class="text-center">
                    <span :class="{'score-highlight': hasScore(major, method.id, year)}">
                      {{ getScoreForMethodAndYear(major, method.id, year) }}
                    </span>
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- CHART VIEW with scrolling container -->
      <div v-else-if="viewMode === 'chart'" class="charts-outer-container">
        <div class="charts-scrollable-container" ref="chartsContainer">
          <!-- Major Chart View -->
          <div v-if="chartViewType === 'major'" class="major-charts">
            <div class="filters mb-3">
              <div class="row g-2">
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="chart-major-select">Chọn ngành:</label>
                    <select id="chart-major-select" class="form-select" v-model="selectedMajorForChart">
                      <option v-for="major in combinedData" :key="major.id" :value="major.id">
                        {{ major.name }} ({{ major.major_code }})
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="chart-method-select">Chọn phương thức xét tuyển:</label>
                    <select id="chart-method-select" class="form-select" v-model="selectedMethodForChart">
                      <option value="all">Tất cả phương thức</option>
                      <option v-for="method in admissionMethods" :key="method.id" :value="method.id">
                        {{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-12 mt-2">
                  <div class="form-group">
                    <label for="chart-years-option">Hiển thị năm:</label>
                    <div class="btn-group">
                      <button 
                        :class="['btn', showAllYears ? 'btn-outline-primary' : 'btn-primary']" 
                        @click="showAllYears = false"
                      >
                        Theo từng năm
                      </button>
                      <button 
                        :class="['btn', showAllYears ? 'btn-primary' : 'btn-outline-primary']" 
                        @click="showAllYears = true"
                      >
                        Tất cả các năm
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="selectedMajorForChart" class="chart-wrapper">
              <h2 class="chart-title h5">
                Biểu đồ điểm chuẩn ngành {{ getMajorById(selectedMajorForChart)?.name }}
                <template v-if="selectedMethodForChart !== 'all'">
                  - {{ getMethodById(selectedMethodForChart)?.name }}
                </template>
                <template v-if="showAllYears">
                  (Tất cả các năm)
                </template>
              </h2>
              
              <!-- Display option: Show all years together -->
              <div v-if="showAllYears" class="all-years-view">
                <div v-if="selectedMethodForChart === 'all'" class="method-charts">
                  <div v-for="method in displayedMethods" 
                       :key="`major-chart-all-${method.id}`" 
                       class="method-chart-container mb-4">
                    <h3 class="h6">{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h3>
                    <div class="chart-box">
                      <canvas :id="`majorChartAllYears${method.id}`"></canvas>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <div class="chart-box">
                    <canvas id="singleMethodAllYearsChart"></canvas>
                  </div>
                </div>
              </div>
              
              <!-- Regular single/multi method chart view -->
              <div v-else>
                <!-- Multiple charts for each method -->
                <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                  <div v-for="method in displayedMethods" 
                       :key="`major-chart-${method.id}`" 
                       class="method-chart-container mb-4">
                    <h3 class="h6">{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h3>
                    <div class="chart-box">
                      <canvas :id="`majorChart${method.id}`"></canvas>
                    </div>
                  </div>
                </div>
                <!-- Single chart for selected method -->
                <div v-else>
                  <div class="chart-box">
                    <canvas id="singleMethodChart"></canvas>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="no-data-message">
              <p>Vui lòng chọn ngành để xem biểu đồ</p>
            </div>
          </div>
          
          <!-- Faculty Chart View -->
          <div v-else-if="chartViewType === 'faculty'" class="faculty-charts">
            <div class="filters mb-3">
              <div class="row g-2">
                <div class="col-md-4">
                  <div class="form-group">
                    <label for="chart-faculty-select">Chọn khoa:</label>
                    <select id="chart-faculty-select" class="form-select" v-model="selectedFacultyForChart">
                      <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                        {{ faculty.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label for="chart-year-select">Chọn năm:</label>
                    <select id="chart-year-select" class="form-select" v-model="selectedYearForChart">
                      <option v-for="year in availableYears" :key="year" :value="year">
                        {{ year }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label for="chart-faculty-method-select">Chọn phương thức xét tuyển:</label>
                    <select id="chart-faculty-method-select" class="form-select" v-model="selectedMethodForChart">
                      <option value="all">Tất cả phương thức</option>
                      <option v-for="method in admissionMethods" :key="method.id" :value="method.id">
                        {{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-12 mt-2">
                  <div class="form-group">
                    <label for="chart-years-option">Hiển thị năm:</label>
                    <div class="btn-group">
                      <button 
                        :class="['btn', showAllYears ? 'btn-outline-primary' : 'btn-primary']" 
                        @click="showAllYears = false"
                      >
                        Chỉ năm {{ selectedYearForChart }}
                      </button>
                      <button 
                        :class="['btn', showAllYears ? 'btn-primary' : 'btn-outline-primary']" 
                        @click="showAllYears = true"
                      >
                        Tất cả các năm
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="selectedFacultyForChart" class="chart-wrapper">
              <h2 class="chart-title h5">
                Biểu đồ điểm chuẩn {{ showAllYears ? 'tất cả các năm' : `năm ${selectedYearForChart}` }} - 
                {{ getFacultyById(selectedFacultyForChart)?.name }}
                <template v-if="selectedMethodForChart !== 'all'">
                  - {{ getMethodById(selectedMethodForChart)?.name }}
                </template>
              </h2>
              
              <!-- All years view -->
              <div v-if="showAllYears" class="all-years-view">
                <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                  <div v-for="method in displayedMethods" 
                       :key="`faculty-chart-all-years-${method.id}`" 
                       class="method-chart-container mb-4">
                    <h3 class="h6">{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h3>
                    <div class="chart-box">
                      <canvas :id="`facultyChartAllYears${method.id}`"></canvas>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <div class="chart-box">
                    <canvas id="singleFacultyMethodAllYearsChart"></canvas>
                  </div>
                </div>
              </div>
              <!-- Regular chart view -->
              <div v-else>
                <!-- Multiple charts for each method -->
                <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                  <div v-for="method in displayedMethods" 
                       :key="`faculty-chart-${method.id}`" 
                       class="method-chart-container mb-4">
                    <h3 class="h6">{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h3>
                    <div class="chart-box">
                      <canvas :id="`facultyChart${method.id}`"></canvas>
                    </div>
                  </div>
                </div>
                <!-- Single chart for selected method -->
                <div v-else>
                  <div class="chart-box">
                    <canvas id="singleFacultyMethodChart"></canvas>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="no-data-message">
              <p>Vui lòng chọn khoa để xem biểu đồ</p>
            </div>
          </div>
          
          <!-- University Chart View -->
          <div v-else-if="chartViewType === 'university'" class="university-charts">
            <div class="filters mb-3">
              <div class="row g-2">
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="university-chart-year-select">Chọn năm:</label>
                    <select id="university-chart-year-select" class="form-select" v-model="selectedYearForChart">
                      <option v-for="year in availableYears" :key="year" :value="year">
                        {{ year }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="chart-university-method-select">Chọn phương thức xét tuyển:</label>
                    <select id="chart-university-method-select" class="form-select" v-model="selectedMethodForChart">
                      <option value="all">Tất cả phương thức</option>
                      <option v-for="method in admissionMethods" :key="method.id" :value="method.id">
                        {{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-12 mt-2">
                  <div class="form-group">
                    <label for="chart-years-option">Hiển thị năm:</label>
                    <div class="btn-group">
                      <button 
                        :class="['btn', showAllYears ? 'btn-outline-primary' : 'btn-primary']" 
                        @click="showAllYears = false"
                      >
                        Chỉ năm {{ selectedYearForChart }}
                      </button>
                      <button 
                        :class="['btn', showAllYears ? 'btn-primary' : 'btn-outline-primary']" 
                        @click="showAllYears = true"
                      >
                        Tất cả các năm
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="chart-wrapper">
              <h2 class="chart-title h5">
                Biểu đồ điểm chuẩn toàn trường {{ showAllYears ? 'tất cả các năm' : `năm ${selectedYearForChart}` }}
                <template v-if="selectedMethodForChart !== 'all'">
                  - {{ getMethodById(selectedMethodForChart)?.name }}
                </template>
              </h2>
              
              <!-- All years view -->
              <div v-if="showAllYears" class="all-years-view">
                <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                  <div v-for="method in displayedMethods" 
                       :key="`university-chart-all-years-${method.id}`" 
                       class="method-chart-container mb-4">
                    <h3 class="h6">{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h3>
                    <div class="chart-box">
                      <canvas :id="`universityChartAllYears${method.id}`"></canvas>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <div class="chart-box">
                    <canvas id="singleUniversityMethodAllYearsChart"></canvas>
                  </div>
                </div>
              </div>
              
              <!-- Regular chart view -->
              <div v-else>
                <!-- Multiple charts for each method -->
                <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                  <div v-for="method in displayedMethods" 
                       :key="`university-chart-${method.id}`" 
                       class="method-chart-container mb-4">
                    <h3 class="h6">{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h3>
                    <div class="chart-box">
                      <canvas :id="`universityChart${method.id}`"></canvas>
                    </div>
                  </div>
                </div>
                <!-- Single chart for selected method -->
                <div v-else>
                  <div class="chart-box">
                    <canvas id="singleUniversityMethodChart"></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Spacer element to ensure scrolling works properly -->
          <div class="chart-footer-spacer"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import preAdmissionController from '@/controllers/preAdmissionController'
import Chart from 'chart.js/auto'

export default {
  name: 'PreAdmissionView',
  data() {
    return {
      combinedData: [],
      admissionMethods: [],
      loading: true,
      error: null,
      viewMode: 'table',  // 'table' or 'chart'
      chartViewType: 'major', // 'major', 'faculty', or 'university'
      selectedFaculty: '',
      searchTerm: '',
      availableYears: [],
      selectedYears: [],
      selectedMajorForChart: null,
      selectedFacultyForChart: null,
      selectedYearForChart: null,
      selectedMethodForChart: 'all', // 'all' or method id
      showAllYears: false, // New flag for showing all years
      charts: {},
      currentUser: 'levantiendatBạn',
      currentDate: '2025-05-08 17:35:59',
      isScrolledToBottom: false
    }
  },
  computed: {
    faculties() {
      // Tạo danh sách các khoa duy nhất
      const facultyMap = {}
      this.combinedData.forEach(major => {
        if (major.faculty.id && !facultyMap[major.faculty.id]) {
          facultyMap[major.faculty.id] = {
            id: major.faculty.id,
            name: major.faculty.name,
            code: major.faculty.code
          }
        }
      })
      return Object.values(facultyMap)
    },
    filteredMajors() {
      return this.combinedData.filter(major => {
        // Lọc theo khoa
        if (this.selectedFaculty && major.faculty.id !== parseInt(this.selectedFaculty)) {
          return false
        }
        
        // Lọc theo từ khóa tìm kiếm
        if (this.searchTerm) {
          const searchLower = this.searchTerm.toLowerCase()
          return major.name.toLowerCase().includes(searchLower) ||
                 major.major_code.toLowerCase().includes(searchLower)
        }
        
        return true
      })
    },
    displayedMethods() {
      // Lọc các phương thức xét tuyển 2-6
      return this.admissionMethods.filter(method => 
        method.id >= 2 && method.id <= 6
      )
    },
    // Danh sách các ngành theo khoa đã chọn
    majorsBySelectedFaculty() {
      if (!this.selectedFacultyForChart) return []
      
      return this.combinedData.filter(
        major => major.faculty.id === parseInt(this.selectedFacultyForChart)
      )
    }
  },
  async mounted() {
    await this.fetchData()
    // Khởi tạo giá trị mặc định
    if (this.availableYears.length > 0) {
      this.selectedYears = [...this.availableYears]
      this.selectedYearForChart = Math.max(...this.availableYears)
    }
    if (this.combinedData.length > 0) {
      this.selectedMajorForChart = this.combinedData[0].id
    }
    if (this.faculties.length > 0) {
      this.selectedFacultyForChart = this.faculties[0].id
    }
    
    // Add resize event listener
    window.addEventListener('resize', this.handleResize)
    
    // Add scroll event listener for chart container
    this.setupScrollListener()
    
    // Add schema.org structured data for SEO
    this.addStructuredData()
  },
  beforeDestroy() {
    // Cleanup event listeners
    window.removeEventListener('resize', this.handleResize)
    
    const chartsContainer = this.$refs.chartsContainer
    if (chartsContainer) {
      chartsContainer.removeEventListener('scroll', this.handleScroll)
    }
    
    // Destroy all charts to prevent memory leaks
    this.destroyAllCharts()
  },
  watch: {
    viewMode() {
      // Xử lý khi chuyển đổi giữa các chế độ xem
      if (this.viewMode === 'chart') {
        this.$nextTick(() => {
          this.setupScrollListener()
          this.renderCharts()
        })
      }
    },
    chartViewType() {
      // Xử lý khi chuyển đổi giữa các loại biểu đồ
      if (this.viewMode === 'chart') {
        this.$nextTick(() => {
          this.renderCharts()
        })
      }
    },
    selectedMajorForChart() {
      // Render lại biểu đồ khi chọn ngành khác
      if (this.viewMode === 'chart' && this.chartViewType === 'major') {
        this.$nextTick(() => {
          this.renderMajorChart()
        })
      }
    },
    selectedFacultyForChart() {
      // Render lại biểu đồ khi chọn khoa khác
      if (this.viewMode === 'chart' && this.chartViewType === 'faculty') {
        this.$nextTick(() => {
          this.renderFacultyChart()
        })
      }
    },
    selectedYearForChart() {
      // Render lại biểu đồ khi chọn năm khác
      if (this.viewMode === 'chart' && (this.chartViewType === 'faculty' || this.chartViewType === 'university')) {
        this.$nextTick(() => {
          if (this.chartViewType === 'faculty') {
            this.renderFacultyChart()
          } else {
            this.renderUniversityChart()
          }
        })
      }
    },
    selectedMethodForChart() {
      // Render lại biểu đồ khi chọn phương thức xét tuyển khác
      if (this.viewMode === 'chart') {
        this.$nextTick(() => {
          if (this.chartViewType === 'major') {
            this.renderMajorChart()
          } else if (this.chartViewType === 'faculty') {
            this.renderFacultyChart()
          } else {
            this.renderUniversityChart()
          }
        })
      }
    },
    showAllYears() {
      // Render lại biểu đồ khi thay đổi chế độ xem năm
      if (this.viewMode === 'chart') {
        this.$nextTick(() => {
          if (this.chartViewType === 'major') {
            this.renderMajorChart()
          } else if (this.chartViewType === 'faculty') {
            this.renderFacultyChart()
          } else {
            this.renderUniversityChart()
          }
        })
      }
    }
  },
  methods: {
    // SEO Enhancement
    addStructuredData() {
      const structuredData = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Điểm Chuẩn Đại Học Bách Khoa Đà Nẵng Các Năm",
        "description": "Dữ liệu điểm chuẩn đại học theo từng phương thức xét tuyển qua các năm của trường Đại học Bách khoa Đà Nẵng",
        "keywords": ["điểm chuẩn", "đại học bách khoa đà nẵng", "tuyển sinh", "xét tuyển"],
        "temporalCoverage": "2018-2023"
      }
      
      // Add structured data to page head
      const script = document.createElement('script')
      script.type = 'application/ld+json'
      script.text = JSON.stringify(structuredData)
      document.head.appendChild(script)
      
      // Update meta title and description
      document.title = "Điểm Chuẩn Các Năm - Đại Học Bách Khoa Đà Nẵng"
      
      // Update meta description
      let metaDescription = document.querySelector('meta[name="description"]')
      if (!metaDescription) {
        metaDescription = document.createElement('meta')
        metaDescription.name = "description"
        document.head.appendChild(metaDescription)
      }
      metaDescription.content = "Tra cứu điểm chuẩn các ngành, khoa của Đại Học Bách Khoa Đà Nẵng qua các năm và theo từng phương thức xét tuyển."
    },
    
    // Scroll handling
    setupScrollListener() {
      this.$nextTick(() => {
        const chartsContainer = this.$refs.chartsContainer
        if (chartsContainer) {
          chartsContainer.addEventListener('scroll', this.handleScroll)
          
          // Initially hide footer
          const footer = document.querySelector('footer')
          if (footer) {
            footer.style.display = 'none'
          }
        }
      })
    },
    
    handleScroll(event) {
      const container = event.target
      const isAtBottom = container.scrollHeight - container.scrollTop - 20 <= container.clientHeight
      
      // Show footer only when scrolled to the bottom
      const footer = document.querySelector('footer')
      if (footer) {
        if (isAtBottom) {
          footer.style.display = 'block'
          footer.style.opacity = '1'
          footer.style.transition = 'opacity 0.3s ease'
        } else {
          footer.style.opacity = '0'
          setTimeout(() => {
            if (!this.isScrolledToBottom) {
              footer.style.display = 'none'
            }
          }, 300)
        }
      }
      
      // Store the scroll state
      this.isScrolledToBottom = isAtBottom
    },
    
    // Window resize handler
    handleResize() {
      if (this.viewMode === 'chart') {
        this.$nextTick(() => {
          Object.values(this.charts).forEach(chart => {
            if (chart) {
              chart.resize()
            }
          })
        })
      }
    },
    
    async fetchData() {
      this.loading = true
      this.error = null
      
      try {
        // Lấy dữ liệu từ controller
        const result = await preAdmissionController.getAllData()
        
        // Cập nhật dữ liệu
        this.combinedData = result.combinedData
        this.admissionMethods = result.admissionMethods
        
        // Xác định các năm có sẵn trong dữ liệu
        const years = new Set()
        this.combinedData.forEach(major => {
          major.admissionScores.forEach(method => {
            Object.keys(method.years).forEach(year => {
              years.add(parseInt(year))
            })
          })
        })
        
        this.availableYears = Array.from(years).sort()
        
        // Mặc định chọn tất cả các năm
        if (this.availableYears.length > 0) {
          this.selectedYears = [...this.availableYears]
          this.selectedYearForChart = Math.max(...this.availableYears)
        }
        
      } catch (err) {
        this.error = `Không thể tải dữ liệu: ${err.message}`
        console.error('Fetch data error:', err)
      } finally {
        this.loading = false
      }
    },
    
    setViewMode(mode) {
      this.viewMode = mode
      
      // If switching to chart mode, ensure footer is initially hidden
      if (mode === 'chart') {
        const footer = document.querySelector('footer')
        if (footer) {
          footer.style.display = 'none'
        }
      } else {
        // If not in chart mode, ensure footer is visible
        const footer = document.querySelector('footer')
        if (footer) {
          footer.style.display = 'block'
          footer.style.opacity = '1'
        }
      }
    },
    
    setChartViewType(type) {
      this.chartViewType = type
    },
    
    getScoreForMethodAndYear(major, methodId, year) {
      const methodData = major.admissionScores.find(m => m.methodId === methodId)
      if (!methodData || !methodData.years[year]) return '—'
      return methodData.years[year]
    },
    
    hasScore(major, methodId, year) {
      const methodData = major.admissionScores.find(m => m.methodId === methodId)
      return methodData && methodData.years[year] ? true : false
    },
    
    getMajorById(majorId) {
      return this.combinedData.find(major => major.id === majorId)
    },
    
    getFacultyById(facultyId) {
      return this.faculties.find(faculty => faculty.id === facultyId)
    },
    
    getMaxScoreForMethod(methodId) {
      return preAdmissionController.getMaxScoreForMethod(methodId)
    },
    
    getMethodColor(methodId) {
      // Improved color palette for better visibility and accessibility
      const colors = {
        2: 'rgba(52, 152, 219, 0.8)',  // Bright blue
        3: 'rgba(241, 196, 15, 0.8)',   // Bright yellow
        4: 'rgba(46, 204, 113, 0.8)',   // Bright green
        5: 'rgba(142, 68, 173, 0.8)',   // Bright purple
        6: 'rgba(230, 126, 34, 0.8)'    // Bright orange
      }
      
      return colors[methodId] || 'rgba(201, 203, 207, 0.8)'
    },
    
    getMethodBorderColor(methodId) {
      // Darker border colors for better contrast
      const colors = {
        2: 'rgba(41, 128, 185, 1)',    // Dark blue
        3: 'rgba(243, 156, 18, 1)',    // Dark yellow
        4: 'rgba(39, 174, 96, 1)',     // Dark green
        5: 'rgba(142, 68, 173, 1)',    // Dark purple
        6: 'rgba(211, 84, 0, 1)'       // Dark orange
      }
      
      return colors[methodId] || 'rgba(150, 150, 150, 1)'
    },
    
    getMethodById(methodId) {
      return this.admissionMethods.find(m => m.id === parseInt(methodId))
    },
    
    getCurrentDateTime() {
      return this.currentDate
    },
    
    // Destroy all existing charts
    destroyAllCharts() {
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.destroy()
        }
      })
      this.charts = {}
    },
    
    renderCharts() {
      this.destroyAllCharts()
      
      // Render new charts based on current view type
      if (this.chartViewType === 'major') {
        this.renderMajorChart()
      } else if (this.chartViewType === 'faculty') {
        this.renderFacultyChart()
      } else if (this.chartViewType === 'university') {
        this.renderUniversityChart()
      }
    },
    
    renderMajorChart() {
      if (!this.selectedMajorForChart) return
      
      const majorData = this.getMajorById(this.selectedMajorForChart)
      if (!majorData) return
      
      this.destroyAllCharts()
      
      // If showing all years
      if (this.showAllYears) {
        if (this.selectedMethodForChart === 'all') {
          this.displayedMethods.forEach(method => {
            this.renderAllYearsMajorChart(majorData, method)
          })
        } else {
          const method = this.getMethodById(this.selectedMethodForChart)
          if (method) {
            this.renderAllYearsMajorChart(majorData, method, true)
          }
        }
        return
      }
      
      // If all methods selected, create separate chart for each method
      if (this.selectedMethodForChart === 'all') {
        this.displayedMethods.forEach(method => {
          this.renderSingleMethodMajorChart(majorData, method)
        })
      } else {
        // If specific method selected, only show chart for that method
        const method = this.getMethodById(this.selectedMethodForChart)
        if (method) {
          this.renderSingleMethodMajorChart(majorData, method, true)
        }
      }
    },
    
    renderAllYearsMajorChart(majorData, method, isSingleMethod = false) {
      const methodId = method.id
      const methodData = majorData.admissionScores.find(m => m.methodId === methodId)
      if (!methodData) return
      
      // Prepare data for chart
      const years = new Set()
      Object.keys(methodData.years).forEach(year => {
        years.add(parseInt(year))
      })
      
      const sortedYears = Array.from(years).sort()
      
      // Create labels for combined year and method
      const labels = []
      const datasets = []
      const colors = []
      
      // Create one column for each year
      sortedYears.forEach(year => {
        labels.push(`Năm ${year}`)
        const score = methodData.years[year] || 0
        datasets.push(score)
        colors.push(this.getMethodColor(methodId))
      })
      
      // Skip if no data for any year
      if (datasets.every(score => score === 0)) return
      
      const chartData = {
        labels: labels,
        datasets: [{
          label: method.name,
          data: datasets,
          backgroundColor: colors,
          borderColor: this.getMethodBorderColor(methodId),
          borderWidth: 2
        }]
      }
      
      // Create chart with ID-based targeting
      const chartId = isSingleMethod ? 'singleMethodAllYearsChart' : `majorChartAllYears${methodId}`
      const canvas = document.getElementById(chartId)
      
      if (canvas) {
        // Create chart
        this.charts[chartId] = new Chart(canvas, {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                max: this.getMaxScoreForMethod(methodId),
                title: {
                  display: true,
                  text: 'Điểm'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Năm'
                },
                ticks: {
                  color: '#333',
                  font: {
                    weight: 'bold'
                  }
                }
              }
            },
            plugins: {
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: `Điểm chuẩn ${majorData.name} qua các năm`,
                font: {
                  size: 16,
                  weight: 'bold'
                }
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    return `Điểm: ${context.raw}`
                  }
                }
              }
            }
          }
        })
      }
    },
    
    renderSingleMethodMajorChart(majorData, method, isSingleMethod = false) {
      const methodId = method.id
      const methodData = majorData.admissionScores.find(m => m.methodId === methodId)
      if (!methodData) return
      
      // Prepare data for chart
      const years = new Set()
      Object.keys(methodData.years).forEach(year => {
        years.add(parseInt(year))
      })
      
      const sortedYears = Array.from(years).sort()
      const data = sortedYears.map(year => methodData.years[year] || null)
      
      // Skip if no data for this method
      if (data.every(score => score === null)) return
      
      const chartData = {
        labels: sortedYears.map(year => year.toString()),
        datasets: [{
          label: method.name,
          data: data,
          backgroundColor: this.getMethodColor(methodId),
          borderColor: this.getMethodBorderColor(methodId),
          borderWidth: 2
        }]
      }
      
      // Create chart with ID-based targeting
      const chartId = isSingleMethod ? 'singleMethodChart' : `majorChart${methodId}`
      const canvas = document.getElementById(chartId)
      
      if (canvas) {
        this.charts[chartId] = new Chart(canvas, {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                max: this.getMaxScoreForMethod(methodId),
                title: {
                  display: true,
                  text: 'Điểm'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Năm'
                }
              }
            },
            plugins: {
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: isSingleMethod ? 
                  `Điểm chuẩn qua các năm - ${majorData.name}` : 
                  ``,
                font: {
                  size: isSingleMethod ? 16 : 14,
                  weight: 'bold'
                }
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    return `Điểm: ${context.raw}`
                  }
                }
              }
            }
          }
        })
      }
    },
    
    renderFacultyChart() {
      if (!this.selectedFacultyForChart) return
      
      this.destroyAllCharts()
      
      const faculty = this.getFacultyById(this.selectedFacultyForChart)
      if (!faculty) return
      
      const majors = this.majorsBySelectedFaculty
      
      if (this.showAllYears) {
        if (this.selectedMethodForChart === 'all') {
          this.displayedMethods.forEach(method => {
            this.renderAllYearsFacultyChart(faculty, majors, method)
          })
        } else {
          const method = this.getMethodById(this.selectedMethodForChart)
          if (method) {
            this.renderAllYearsFacultyChart(faculty, majors, method, true)
          }
        }
      } else {
        if (this.selectedMethodForChart === 'all') {
          this.displayedMethods.forEach(method => {
            this.renderSingleYearFacultyChart(faculty, majors, method, this.selectedYearForChart)
          })
        } else {
          const method = this.getMethodById(this.selectedMethodForChart)
          if (method) {
            this.renderSingleYearFacultyChart(faculty, majors, method, this.selectedYearForChart, true)
          }
        }
      }
    },
    
    renderAllYearsFacultyChart(faculty, majors, method, isSingleMethod = false) {
      const methodId = method.id
      
      // Collect years data
      const allYears = new Set()
      majors.forEach(major => {
        const methodData = major.admissionScores.find(m => m.methodId === methodId)
        if (methodData) {
          Object.keys(methodData.years).forEach(year => {
            allYears.add(parseInt(year))
          })
        }
      })
      
      const sortedYears = Array.from(allYears).sort()
      
      // Skip if no years data found
      if (sortedYears.length === 0) return
      
      // Create datasets for each year
      const datasets = []
      
      sortedYears.forEach((year, index) => {
        const yearData = {
          label: `Năm ${year}`,
          data: [],
          backgroundColor: this.getYearColor(index),
          borderColor: this.getYearBorderColor(index),
          borderWidth: 1
        }
        
        // Collect scores for each major in this year
        majors.forEach(major => {
          const methodData = major.admissionScores.find(m => m.methodId === methodId)
          yearData.data.push(methodData && methodData.years[year] ? methodData.years[year] : null)
        })
        
        datasets.push(yearData)
      })
      
      const chartData = {
        labels: majors.map(m => m.name),
        datasets: datasets
      }
      
      // Create chart
      const chartId = isSingleMethod ? 'singleFacultyMethodAllYearsChart' : `facultyChartAllYears${methodId}`
      const canvas = document.getElementById(chartId)
      
      if (canvas) {
        this.charts[chartId] = new Chart(canvas, {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                max: this.getMaxScoreForMethod(methodId),
                title: {
                  display: true,
                  text: 'Điểm'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Ngành'
                },
                ticks: {
                  maxRotation: 45,
                  minRotation: 45
                }
              }
            },
            plugins: {
              title: {
                display: true,
                text: `Điểm chuẩn ${method.name} các ngành khoa ${faculty.name} qua các năm`,
                font: {
                  size: 14,
                  weight: 'bold'
                }
              }
            }
          }
        })
      }
    },
    
    renderSingleYearFacultyChart(faculty, majors, method, year, isSingleMethod = false) {
      const methodId = method.id
      
      // Collect data for the selected year
      const data = []
      const colors = []
      
      majors.forEach(major => {
        const methodData = major.admissionScores.find(m => m.methodId === methodId)
        const score = methodData && methodData.years[year] ? methodData.years[year] : null
        data.push(score)
        colors.push(this.getMethodColor(methodId))
      })
      
      // Skip if no data for this year/method
      if (data.every(score => score === null)) return
      
      const chartData = {
        labels: majors.map(m => m.name),
        datasets: [{
          label: `${method.name} năm ${year}`,
          data: data,
          backgroundColor: colors,
          borderColor: this.getMethodBorderColor(methodId),
          borderWidth: 2
        }]
      }
      
      // Create chart
      const chartId = isSingleMethod ? 'singleFacultyMethodChart' : `facultyChart${methodId}`
      const canvas = document.getElementById(chartId)
      
      if (canvas) {
        this.charts[chartId] = new Chart(canvas, {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: majors.length > 5 ? 'y' : 'x', // Use horizontal bar for many majors
            scales: {
              y: {
                beginAtZero: true,
                max: this.getMaxScoreForMethod(methodId),
                title: {
                  display: true,
                  text: majors.length > 5 ? 'Ngành' : 'Điểm'
                }
              },
              x: {
                beginAtZero: majors.length > 5,
                max: majors.length > 5 ? this.getMaxScoreForMethod(methodId) : undefined,
                title: {
                  display: true,
                  text: majors.length > 5 ? 'Điểm' : 'Ngành'
                },
                ticks: {
                  maxRotation: 45,
                  minRotation: 45
                }
              }
            },
            plugins: {
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: `Điểm chuẩn ${method.name} các ngành khoa ${faculty.name} năm ${year}`,
                font: {
                  size: 14,
                  weight: 'bold'
                }
              }
            }
          }
        })
      }
    },
    
    renderUniversityChart() {
      this.destroyAllCharts()
      
      if (this.showAllYears) {
        if (this.selectedMethodForChart === 'all') {
          this.displayedMethods.forEach(method => {
            this.renderAllYearsUniversityChart(method)
          })
        } else {
          const method = this.getMethodById(this.selectedMethodForChart)
          if (method) {
            this.renderAllYearsUniversityChart(method, true)
          }
        }
      } else {
        if (this.selectedMethodForChart === 'all') {
          this.displayedMethods.forEach(method => {
            this.renderSingleYearUniversityChart(method, this.selectedYearForChart)
          })
        } else {
          const method = this.getMethodById(this.selectedMethodForChart)
          if (method) {
            this.renderSingleYearUniversityChart(method, this.selectedYearForChart, true)
          }
        }
      }
    },
    
    renderAllYearsUniversityChart(method, isSingleMethod = false) {
      const methodId = method.id
      
      // Group by faculty to make chart more readable
      const faculties = this.faculties
      const facultyData = {}
      
      // Initialize data structure
      faculties.forEach(faculty => {
        facultyData[faculty.id] = {
          name: faculty.name,
          years: {}
        }
      })
      
      // Collect all years
      const allYears = new Set()
      
      // Calculate average scores by faculty for each year
      this.combinedData.forEach(major => {
        const facultyId = major.faculty.id
        if (facultyId && facultyData[facultyId]) {
          const methodData = major.admissionScores.find(m => m.methodId === methodId)
          if (methodData) {
            Object.keys(methodData.years).forEach(year => {
              const yearInt = parseInt(year)
              allYears.add(yearInt)
              
              if (!facultyData[facultyId].years[yearInt]) {
                facultyData[facultyId].years[yearInt] = {
                  sum: 0,
                  count: 0
                }
              }
              
              const score = methodData.years[year]
              if (score) {
                facultyData[facultyId].years[yearInt].sum += score
                facultyData[facultyId].years[yearInt].count += 1
              }
            })
          }
        }
      })
      
      const sortedYears = Array.from(allYears).sort()
      
      // Skip if no data
      if (sortedYears.length === 0) return
      
      // Create datasets for each year
      const datasets = []
      
      sortedYears.forEach((year, index) => {
        const yearData = {
          label: `Năm ${year}`,
          data: [],
          backgroundColor: this.getYearColor(index),
          borderColor: this.getYearBorderColor(index),
          borderWidth: 1
        }
        
        // Calculate average for each faculty in this year
        faculties.forEach(faculty => {
          const facultyYearData = facultyData[faculty.id]?.years[year]
          yearData.data.push(
            facultyYearData && facultyYearData.count > 0 
              ? Math.round((facultyYearData.sum / facultyYearData.count) * 100) / 100
              : null
          )
        })
        
        datasets.push(yearData)
      })
      
      const chartData = {
        labels: faculties.map(f => f.name),
        datasets: datasets
      }
      
      // Create chart
      const chartId = isSingleMethod ? 'singleUniversityMethodAllYearsChart' : `universityChartAllYears${methodId}`
      const canvas = document.getElementById(chartId)
      
      if (canvas) {
        this.charts[chartId] = new Chart(canvas, {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                max: this.getMaxScoreForMethod(methodId),
                title: {
                  display: true,
                  text: 'Điểm trung bình'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Khoa'
                },
                ticks: {
                  maxRotation: 45,
                  minRotation: 45
                }
              }
            },
            plugins: {
              title: {
                display: true,
                text: `Điểm chuẩn trung bình ${method.name} theo khoa qua các năm`,
                font: {
                  size: 14,
                  weight: 'bold'
                }
              }
            }
          }
        })
      }
    },
    
    renderSingleYearUniversityChart(method, year, isSingleMethod = false) {
      const methodId = method.id
      
      // Group faculties to make chart more readable
      const faculties = this.faculties
      const facultyScores = {}
      
      // Initialize
      faculties.forEach(faculty => {
        facultyScores[faculty.id] = {
          name: faculty.name,
          sum: 0,
          count: 0
        }
      })
      
      // Calculate average for each faculty in this year
      this.combinedData.forEach(major => {
        const facultyId = major.faculty.id
        if (facultyId && facultyScores[facultyId]) {
          const methodData = major.admissionScores.find(m => m.methodId === methodId)
          if (methodData && methodData.years[year]) {
            facultyScores[facultyId].sum += methodData.years[year]
            facultyScores[facultyId].count += 1
          }
        }
      })
      
      // Prepare chart data
      const data = []
      const labels = []
      const colors = []
      
      faculties.forEach(faculty => {
        const facultyData = facultyScores[faculty.id]
        if (facultyData.count > 0) {
          labels.push(faculty.name)
          data.push(Math.round((facultyData.sum / facultyData.count) * 100) / 100)
          colors.push(this.getMethodColor(methodId))
        }
      })
      
      // Skip if no data
      if (data.length === 0) return
      
      const chartData = {
        labels: labels,
        datasets: [{
          label: `${method.name} năm ${year}`,
          data: data,
          backgroundColor: colors,
          borderColor: this.getMethodBorderColor(methodId),
          borderWidth: 2
        }]
      }
      
      // Create chart
      const chartId = isSingleMethod ? 'singleUniversityMethodChart' : `universityChart${methodId}`
      const canvas = document.getElementById(chartId)
      
      if (canvas) {
        this.charts[chartId] = new Chart(canvas, {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                max: this.getMaxScoreForMethod(methodId),
                title: {
                  display: true,
                  text: 'Điểm trung bình'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Khoa'
                },
                ticks: {
                  maxRotation: 45,
                  minRotation: 45
                }
              }
            },
            plugins: {
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: `Điểm chuẩn trung bình ${method.name} theo khoa năm ${year}`,
                font: {
                  size: 14,
                  weight: 'bold'
                }
              }
            }
          }
        })
      }
    },
    
    // Helper function to generate colors for years
    getYearColor(index) {
      const colors = [
        'rgba(52, 152, 219, 0.7)',  // Blue
        'rgba(46, 204, 113, 0.7)',  // Green
        'rgba(155, 89, 182, 0.7)',  // Purple
        'rgba(52, 73, 94, 0.7)',    // Dark Blue
        'rgba(241, 196, 15, 0.7)',  // Yellow
        'rgba(230, 126, 34, 0.7)',  // Orange
        'rgba(231, 76, 60, 0.7)'    // Red
      ]
      return colors[index % colors.length]
    },
    
    getYearBorderColor(index) {
      const colors = [
        'rgba(41, 128, 185, 1)',    // Blue
        'rgba(39, 174, 96, 1)',     // Green
        'rgba(142, 68, 173, 1)',    // Purple
        'rgba(44, 62, 80, 1)',      // Dark Blue
        'rgba(243, 156, 18, 1)',    // Yellow
        'rgba(211, 84, 0, 1)',      // Orange
        'rgba(192, 57, 43, 1)'      // Red
      ]
      return colors[index % colors.length]
    }
  }
}
</script>

<style scoped>
/* SEO-friendly and compact styles */
.pre-admission-container {
  font-size: 0.95rem;
  line-height: 1.4;
}

.header-section {
  background: linear-gradient(135deg,#2a8eec , #6d4d08, #0820f3);
  padding: 1rem 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.main-title {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #bfc794;
}

.subtitle {
  color: #eff2f5;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.view-controls {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

/* Table styles - kept as in original */
.table-container {
  margin-bottom: 2rem;
}

.score-highlight {
  font-weight: 600;
  color: #dc3545;
}

/* Chart container with scrolling functionality */
.charts-outer-container {
  position: relative;
  width: 100%;
}

.charts-scrollable-container {
  height: calc(100vh - 200px); /* Adjust based on your header height */
  overflow-y: auto;
  padding-bottom: 30px; /* Space for content below */
  scrollbar-width: thin;
  scrollbar-color: #6c757d #f1f1f1;
}

.charts-scrollable-container::-webkit-scrollbar {
  width: 8px;
}

.charts-scrollable-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.charts-scrollable-container::-webkit-scrollbar-thumb {
  background-color: #6c757d;
  border-radius: 4px;
}

/* Chart styles */
.chart-wrapper {
  margin-bottom: 2rem;
}

.chart-title {
  color: #343a40;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.chart-box {
  height: 400px;
  position: relative;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #fff;
  border: 1px solid #e9ecef;
  border-radius: 0.25rem;
}

.method-chart-container {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.25rem;
}

.method-chart-container h3 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
  color: #495057;
}

.filters {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

/* Footer spacer to ensure scrolling before footer appears */
.chart-footer-spacer {
  height: 30px;
  width: 100%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .main-title {
    font-size: 1.5rem;
  }
  
  .chart-box {
    height: 300px; /* Smaller height on mobile */
  }
  
  .charts-scrollable-container {
    height: calc(100vh - 180px);
  }
  
  .method-chart-container {
    padding: 0.75rem;
  }
}

/* Accessibility improvements */
.btn:focus, .form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Print styles */
@media print {
  .charts-scrollable-container {
    height: auto;
    overflow: visible;
  }
  
  .chart-box {
    break-inside: avoid;
    page-break-inside: avoid;
    margin-bottom: 1cm;
  }
}

/* Styles cho bảng dữ liệu điểm chuẩn - Phong cách du lịch giáo dục */
.table-responsive {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.table {
  font-family: 'Quicksand', 'Segoe UI', sans-serif;
  background-color: #ffffff;
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
}

/* Thiết kế tiêu đề chính */
.table thead tr:first-child th {
  background: linear-gradient(135deg, #1a6fc4, #0d4e8d);
  color: #ffffff;
  padding: 15px 10px;
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.5px;
  text-shadow: 0px 1px 2px rgba(0, 0, 0, 0.3);
  border: none;
}

/* Thiết kế tiêu đề năm */
.table thead tr.bg-info th {
  background: linear-gradient(135deg, #ffd146, #ffbd00) !important;
  color: #2d3748 !important;
  font-weight: bold;
  padding: 10px 8px;
  font-size: 0.9rem;
  border: none;
  position: relative;
}

/* Hiệu ứng gợn sóng cho tiêu đề năm */
.table thead tr.bg-info th::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, 
    rgba(255,255,255,0.1) 25%, 
    transparent 25%, 
    transparent 50%, 
    rgba(255,255,255,0.1) 50%, 
    rgba(255,255,255,0.1) 75%, 
    transparent 75%, 
    transparent);
  background-size: 6px 6px;
}

/* Tiêu đề phương thức */
.method-header {
  position: relative;
  overflow: hidden;
}

.method-header::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: rgba(255, 255, 255, 0.5);
}

/* Định dạng các hàng trong bảng */
.table tbody tr {
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.table tbody tr:hover {
  background-color: rgba(232, 244, 253, 0.7) !important;
  border-left: 3px solid #1a6fc4;
  transform: translateX(2px);
}

/* Định dạng các ô trong bảng */
.table tbody td {
  padding: 12px 10px;
  vertical-align: middle;
  border-bottom: 1px solid #e2e8f0;
  border-right: 1px solid #e2e8f0;
  font-size: 0.95rem;
}

/* Kiểu cho cột STT */
.table tbody td:first-child {
  font-weight: bold;
  background-color: #f8fafc;
  text-align: center;
}

/* Kiểu cho cột tên ngành */
.table tbody td:nth-child(2) {
  min-width: 200px;
  font-weight: 500;
  color: #1a6fc4;
}

/* Kiểu cho cột mã ngành */
.table tbody td:nth-child(3) {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #2d3748;
  background-color: #f8fafc;
  text-align: center;
}

/* Định dạng điểm số */
.score-highlight {
  font-weight: bold;
  color: #1334f3;
  font-size: 1.05rem;
  background: linear-gradient(to bottom, #fff176, #ffd54f);
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Thêm hiệu ứng khung nổi cho điểm */
.table tbody td:nth-child(n+4):hover {
  background-color: #ebf8ff;
}

/* Thêm biểu tượng cho những bản ghi không có điểm */
.table td span:empty::before {
  content: "—";
  color: #a0aec0;
}

/* Bổ sung hiệu ứng màu sắc xen kẽ theo ngành */
.table tbody tr:nth-child(4n+1),
.table tbody tr:nth-child(4n+2) {
  background-color: #ffffff;
}

.table tbody tr:nth-child(4n+3),
.table tbody tr:nth-child(4n+4) {
  background-color: #f7fafc;
}

/* Thêm biểu tượng cho phần lọc */
.filters {
  background: linear-gradient(to right, #e6f2ff, #ffffff);
  border-left: 5px solid #1a6fc4;
  border-radius: 0 8px 8px 0;
}

/* Làm đẹp cho các phần tử lọc */
.form-select, .form-control {
  border-radius: 6px;
  border: 1px solid #cbd5e0;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  font-family: 'Quicksand', 'Segoe UI', sans-serif;
  transition: all 0.3s ease;
}

.form-select:focus, .form-control:focus {
  border-color: #1a6fc4;
  box-shadow: 0 0 0 3px rgba(26, 111, 196, 0.2);
}

/* Định dạng nhãn Form */
.form-group label {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

/* Thiết kế responsive */
@media (max-width: 992px) {
  .table {
    font-size: 0.9rem;
  }
  
  .table thead tr:first-child th {
    padding: 10px 5px;
    font-size: 0.9rem;
  }
  
  .score-highlight {
    padding: 2px 4px;
    font-size: 0.95rem;
  }
}

/* Thêm animation cho điểm nổi bật khi hover */
.score-highlight {
  transition: all 0.2s ease;
}

.score-highlight:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
</style>