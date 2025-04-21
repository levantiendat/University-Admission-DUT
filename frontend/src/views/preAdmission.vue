<template>
  <div class="pre-admission-container">
    <div class="header-section">
      <div class="container">
        <h1 class="main-title">Điểm Chuẩn Các Năm Trước</h1>
        <p class="subtitle">Tham khảo điểm chuẩn các năm để chuẩn bị tốt nhất cho kỳ thi sắp tới</p>
        
        <div class="view-controls">
          <div class="display-type">
            <button 
              :class="['btn', viewMode === 'table' ? 'btn-primary' : 'btn-outline-primary']" 
              @click="setViewMode('table')"
            >
              <i class="fas fa-table"></i> Xem dạng bảng
            </button>
            <button 
              :class="['btn', viewMode === 'chart' ? 'btn-primary' : 'btn-outline-primary']" 
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
      <div v-else-if="viewMode === 'table'" class="table-container">
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
                <th rowspan="2" class="align-middle">Chỉ tiêu</th>
                <th rowspan="2" class="align-middle">Khoa</th>
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
                <td>{{ major.seats }}</td>
                <td>{{ major.faculty.name }}</td>
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
      
      <!-- CHART VIEW -->
      <div v-else-if="viewMode === 'chart'" class="chart-container">
        <!-- Major Chart View -->
        <div v-if="chartViewType === 'major'" class="major-charts">
          <div class="filters mb-4">
            <div class="row">
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
              <div class="col-md-12 mt-3">
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
            <h3 class="chart-title">
              Biểu đồ điểm chuẩn ngành {{ getMajorById(selectedMajorForChart)?.name }}
              <template v-if="selectedMethodForChart !== 'all'">
                - {{ getMethodById(selectedMethodForChart)?.name }}
              </template>
              <template v-if="showAllYears">
                (Tất cả các năm)
              </template>
            </h3>
            
            <!-- Display option: Show all years together -->
            <div v-if="showAllYears" class="all-years-view">
              <div v-if="selectedMethodForChart === 'all'" class="method-charts">
                <div v-for="method in displayedMethods" 
                     :key="`major-chart-all-${method.id}`" 
                     class="method-chart-container mb-5">
                  <h4>{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h4>
                  <canvas :ref="`majorChartAllYears${method.id}`"></canvas>
                </div>
              </div>
              <div v-else>
                <canvas ref="singleMethodAllYearsChart"></canvas>
              </div>
            </div>
            
            <!-- Regular single/multi method chart view -->
            <div v-else>
              <!-- Multiple charts for each method -->
              <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                <div v-for="method in displayedMethods" 
                     :key="`major-chart-${method.id}`" 
                     class="method-chart-container mb-4">
                  <h4>{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h4>
                  <canvas :ref="`majorChart${method.id}`"></canvas>
                </div>
              </div>
              <!-- Single chart for selected method -->
              <div v-else>
                <canvas ref="singleMethodChart"></canvas>
              </div>
            </div>
          </div>
          <div v-else class="no-data-message">
            <p>Vui lòng chọn ngành để xem biểu đồ</p>
          </div>
        </div>
        
        <!-- Faculty Chart View -->
        <div v-else-if="chartViewType === 'faculty'" class="faculty-charts">
          <div class="filters mb-4">
            <div class="row">
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
              <div class="col-md-12 mt-3">
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
            <h3 class="chart-title">
              Biểu đồ điểm chuẩn {{ showAllYears ? 'tất cả các năm' : `năm ${selectedYearForChart}` }} - 
              {{ getFacultyById(selectedFacultyForChart)?.name }}
              <template v-if="selectedMethodForChart !== 'all'">
                - {{ getMethodById(selectedMethodForChart)?.name }}
              </template>
            </h3>
            
            <!-- All years view -->
            <div v-if="showAllYears" class="all-years-view">
              <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                <div v-for="method in displayedMethods" 
                     :key="`faculty-chart-all-years-${method.id}`" 
                     class="method-chart-container mb-4">
                  <h4>{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h4>
                  <canvas :ref="`facultyChartAllYears${method.id}`"></canvas>
                </div>
              </div>
              <div v-else>
                <canvas ref="singleFacultyMethodAllYearsChart"></canvas>
              </div>
            </div>
            <!-- Regular chart view -->
            <div v-else>
              <!-- Multiple charts for each method -->
              <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                <div v-for="method in displayedMethods" 
                     :key="`faculty-chart-${method.id}`" 
                     class="method-chart-container mb-4">
                  <h4>{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h4>
                  <canvas :ref="`facultyChart${method.id}`"></canvas>
                </div>
              </div>
              <!-- Single chart for selected method -->
              <div v-else>
                <canvas ref="singleFacultyMethodChart"></canvas>
              </div>
            </div>
          </div>
          <div v-else class="no-data-message">
            <p>Vui lòng chọn khoa để xem biểu đồ</p>
          </div>
        </div>
        
        <!-- University Chart View -->
        <div v-else-if="chartViewType === 'university'" class="university-charts">
          <div class="filters mb-4">
            <div class="row">
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
              <div class="col-md-12 mt-3">
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
            <h3 class="chart-title">
              Biểu đồ điểm chuẩn toàn trường {{ showAllYears ? 'tất cả các năm' : `năm ${selectedYearForChart}` }}
              <template v-if="selectedMethodForChart !== 'all'">
                - {{ getMethodById(selectedMethodForChart)?.name }}
              </template>
            </h3>
            
            <!-- All years view -->
            <div v-if="showAllYears" class="all-years-view">
              <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                <div v-for="method in displayedMethods" 
                     :key="`university-chart-all-years-${method.id}`" 
                     class="method-chart-container mb-4">
                  <h4>{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h4>
                  <canvas :ref="`universityChartAllYears${method.id}`"></canvas>
                </div>
              </div>
              <div v-else>
                <canvas ref="singleUniversityMethodAllYearsChart"></canvas>
              </div>
            </div>
            
            <!-- Regular chart view -->
            <div v-else>
              <!-- Multiple charts for each method -->
              <div v-if="selectedMethodForChart === 'all'" class="method-charts vertical-charts">
                <div v-for="method in displayedMethods" 
                     :key="`university-chart-${method.id}`" 
                     class="method-chart-container mb-4">
                  <h4>{{ method.name }} (thang {{ getMaxScoreForMethod(method.id) }} điểm)</h4>
                  <canvas :ref="`universityChart${method.id}`"></canvas>
                </div>
              </div>
              <!-- Single chart for selected method -->
              <div v-else>
                <canvas ref="singleUniversityMethodChart"></canvas>
              </div>
            </div>
          </div>
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
      currentUser: 'levantiendatcode',
      currentDate: '2025-04-20 23:44:11',
      chartHeight: '60vh' // Stored chart height value
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
    window.addEventListener('resize', this.adjustChartSizes)
  },
  beforeDestroy() {
    // Cleanup resize listener when component is destroyed
    window.removeEventListener('resize', this.adjustChartSizes)
  },
  watch: {
    viewMode() {
      // Xử lý khi chuyển đổi giữa các chế độ xem
      if (this.viewMode === 'chart') {
        this.$nextTick(() => {
          this.renderCharts()
          this.adjustChartSizes() // Adjust chart sizes after rendering
        })
      }
    },
    chartViewType() {
      // Xử lý khi chuyển đổi giữa các loại biểu đồ
      if (this.viewMode === 'chart') {
        this.$nextTick(() => {
          this.renderCharts()
          this.adjustChartSizes() // Adjust chart sizes after rendering
        })
      }
    },
    selectedMajorForChart() {
      // Render lại biểu đồ khi chọn ngành khác
      if (this.viewMode === 'chart' && this.chartViewType === 'major') {
        this.$nextTick(() => {
          this.renderMajorChart()
          this.adjustChartSizes() // Adjust chart sizes after rendering
        })
      }
    },
    selectedFacultyForChart() {
      // Render lại biểu đồ khi chọn khoa khác
      if (this.viewMode === 'chart' && this.chartViewType === 'faculty') {
        this.$nextTick(() => {
          this.renderFacultyChart()
          this.adjustChartSizes() // Adjust chart sizes after rendering
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
          this.adjustChartSizes() // Adjust chart sizes after rendering
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
          this.adjustChartSizes() // Adjust chart sizes after rendering
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
          this.adjustChartSizes() // Adjust chart sizes after rendering
        })
      }
    }
  },
  methods: {
    // Adjust chart sizes to ensure they don't exceed 60% of viewport height
    adjustChartSizes() {
      this.$nextTick(() => {
        // Calculate the maximum height (60% of viewport height)
        const maxHeight = window.innerHeight * 0.6
        
        // Get all chart containers
        const chartContainers = document.querySelectorAll('.chart-container')
        
        chartContainers.forEach(container => {
          // Set height to 60% of viewport height
          container.style.height = `${maxHeight}px`
          container.style.maxHeight = '60vh'
          
          // For single method charts, ensure they have proper width
          if (container.classList.contains('single-method-chart')) {
            container.style.width = '100%'
          }
          
          // Force chart resize if it exists
          const chartId = container.getAttribute('data-chart-id')
          if (chartId && this.charts[chartId]) {
            this.charts[chartId].resize()
          }
        })
      })
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
      // Cải thiện màu sắc để tươi tắn hơn
      const colors = {
        2: 'rgba(52, 152, 219, 0.8)',  // Xanh dương tươi sáng
        3: 'rgba(241, 196, 15, 0.8)',   // Vàng tươi sáng
        4: 'rgba(46, 204, 113, 0.8)',   // Xanh lá tươi sáng
        5: 'rgba(142, 68, 173, 0.8)',   // Tím tươi sáng
        6: 'rgba(230, 126, 34, 0.8)'    // Cam tươi sáng
      }
      
      return colors[methodId] || 'rgba(201, 203, 207, 0.8)'
    },
    getMethodBorderColor(methodId) {
      // Màu viền đậm hơn cho các cột
      const colors = {
        2: 'rgba(41, 128, 185, 1)',    // Xanh dương đậm
        3: 'rgba(243, 156, 18, 1)',    // Vàng đậm
        4: 'rgba(39, 174, 96, 1)',     // Xanh lá đậm
        5: 'rgba(142, 68, 173, 1)',    // Tím đậm
        6: 'rgba(211, 84, 0, 1)'       // Cam đậm
      }
      
      return colors[methodId] || 'rgba(150, 150, 150, 1)'
    },
    getMethodById(methodId) {
      return this.admissionMethods.find(m => m.id === parseInt(methodId))
    },
    getCurrentDateTime() {
      return this.currentDate
    },
    // Hủy tất cả các biểu đồ hiện có
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
      
      // Render biểu đồ mới dựa trên loại hiện tại
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
      
      // Nếu hiển thị tất cả các năm
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
      
      // Nếu chọn tất cả phương thức, tạo biểu đồ riêng cho từng phương thức
      if (this.selectedMethodForChart === 'all') {
        this.displayedMethods.forEach(method => {
          this.renderSingleMethodMajorChart(majorData, method)
        })
      } else {
        // Nếu chọn một phương thức cụ thể, chỉ hiển thị biểu đồ cho phương thức đó
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
      
      // Chuẩn bị dữ liệu cho biểu đồ
      const years = new Set()
      Object.keys(methodData.years).forEach(year => {
        years.add(parseInt(year))
      })
      
      const sortedYears = Array.from(years).sort()
      
      // Tạo nhãn kết hợp giữa năm và phương thức
      const labels = []
      const datasets = []
      const colors = []
      
      // Tạo một cột cho mỗi năm
      sortedYears.forEach(year => {
        labels.push(`Năm ${year}`)
        const score = methodData.years[year] || 0
        datasets.push(score)
        colors.push(this.getMethodColor(methodId))
      })
      
      // Nếu không có dữ liệu cho bất kỳ năm nào, bỏ qua
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
      
      // Tạo biểu đồ
      const refName = isSingleMethod ? 'singleMethodAllYearsChart' : `majorChartAllYears${methodId}`
      const ctx = this.$refs[refName]?.[isSingleMethod ? 0 : this.$refs[refName].length - 1]?.getContext('2d')
      
      if (ctx) {
        // Add chart container class and data attribute
        const chartContainer = ctx.canvas.parentNode
        chartContainer.classList.add('chart-container')
        if (isSingleMethod) {
          chartContainer.classList.add('single-method-chart')
        }
        chartContainer.setAttribute('data-chart-id', refName)
        
        // Create chart with responsive and maintainAspectRatio: false
        this.charts[refName] = new Chart(ctx, {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false, // Essential for controlling size
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
            },
            // Add onResize callback to ensure chart fits within 60% of viewport height
            onResize: (chart, size) => {
              const maxHeight = window.innerHeight * 0.6
              chart.canvas.parentNode.style.height = `${maxHeight}px`
            }
          }
        })
        
        // Set initial height for the chart container
        const maxHeight = window.innerHeight * 0.6
        chartContainer.style.height = `${maxHeight}px`
        chartContainer.style.maxHeight = '60vh'
      }
    },
    renderSingleMethodMajorChart(majorData, method, isSingleMethod = false) {
      const methodId = method.id
      const methodData = majorData.admissionScores.find(m => m.methodId === methodId)
      if (!methodData) return
      
      // Chuẩn bị dữ liệu cho biểu đồ
      const years = new Set()
      Object.keys(methodData.years).forEach(year => {
        years.add(parseInt(year))
      })
      
      const sortedYears = Array.from(years).sort()
      const data = sortedYears.map(year => methodData.years[year] || null)
      
      // Kiểm tra nếu không có dữ liệu nào cho phương thức này
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
      
      // Tạo biểu đồ
      const refName = isSingleMethod ? 'singleMethodChart' : `majorChart${methodId}`
      const ctx = this.$refs[refName]?.[isSingleMethod ? 0 : this.$refs[refName].length - 1]?.getContext('2d')
      
      if (ctx) {
        // Add chart container class and data attribute
        const chartContainer = ctx.canvas.parentNode
        chartContainer.classList.add('chart-container')
        if (isSingleMethod) {
          chartContainer.classList.add('single-method-chart')
        }
        chartContainer.setAttribute('data-chart-id', refName)
        
        this.charts[refName] = new Chart(ctx, {
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
            },
            // Add onResize callback to ensure chart fits within 60% of viewport height
            onResize: (chart, size) => {
              const maxHeight = window.innerHeight * 0.6
              chart.canvas.parentNode.style.height = `${maxHeight}px`
            }
          }
        })
        
        // Set initial height for the chart container
        const maxHeight = window.innerHeight * 0.6
        chartContainer.style.height = `${maxHeight}px`
        chartContainer.style.maxHeight = '60vh'
      }
    },
    renderFacultyChart() {
      if (!this.selectedFacultyForChart || !this.selectedYearForChart) return
      
      const faculty = this.getFacultyById(this.selectedFacultyForChart)
      if (!faculty) return
      
      // Lọc các ngành thuộc khoa đã chọn
      const majors = this.majorsBySelectedFaculty
      if (majors.length === 0) return
      
      this.destroyAllCharts()
      
      // Nếu hiển thị tất cả các năm
      if (this.showAllYears) {
        if (this.selectedMethodForChart === 'all') {
          this.displayedMethods.forEach(method => {
            this.renderAllYearsFacultyChart(majors, faculty, method)
          })
        } else {
          const method = this.getMethodById(this.selectedMethodForChart)
          if (method) {
            this.renderAllYearsFacultyChart(majors, faculty, method, true)
          }
        }
        return
      }
      
      // Nếu chọn tất cả phương thức, tạo biểu đồ riêng cho từng phương thức
      if (this.selectedMethodForChart === 'all') {
        this.displayedMethods.forEach(method => {
          this.renderSingleMethodFacultyChart(majors, faculty, method)
        })
      } else {
        // Nếu chọn một phương thức cụ thể, chỉ hiển thị biểu đồ cho phương thức đó
        const method = this.getMethodById(this.selectedMethodForChart)
        if (method) {
          this.renderSingleMethodFacultyChart(majors, faculty, method, true)
        }
      }
    },
    renderAllYearsFacultyChart(majors, faculty, method, isSingleMethod = false) {
      const methodId = method.id
      
      // Tạo thành 2 cột cho mỗi ngành - mỗi năm 1 cột
      const labels = []
      const datasets = []
      const colors = []
      const years = [...this.availableYears].sort()
      
      // Thêm dữ liệu cho từng ngành và từng năm
      majors.forEach(major => {
        const majorName = major.name
        
        years.forEach(year => {
          labels.push(`${majorName} (${year})`)
          
          const methodData = major.admissionScores.find(m => m.methodId === methodId)
          const score = methodData && methodData.years[year] ? methodData.years[year] : 0
          
          datasets.push(score)
          colors.push(year === Math.min(...years) ? 
                     this.getMethodColor(methodId).replace('0.8', '0.6') : 
                     this.getMethodColor(methodId))
        })
      })
      
      // Nếu không có dữ liệu cho bất kỳ ngành nào, bỏ qua
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
      
      // Tạo biểu đồ
      const refName = isSingleMethod ? 'singleFacultyMethodAllYearsChart' : `facultyChartAllYears${methodId}`
      const ctx = this.$refs[refName]?.[isSingleMethod ? 0 : this.$refs[refName].length - 1]?.getContext('2d')
      
      if (ctx) {
        // Add chart container class and data attribute
        const chartContainer = ctx.canvas.parentNode
        chartContainer.classList.add('chart-container')
        if (isSingleMethod) {
          chartContainer.classList.add('single-method-chart')
        }
        chartContainer.setAttribute('data-chart-id', refName)
        
        this.charts[refName] = new Chart(ctx, {
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
                  text: 'Ngành theo năm'
                },
                ticks: {
                  autoSkip: false,
                  maxRotation: 90,
                  minRotation: 45,
                  font: {
                    size: 10
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
                text: `Điểm chuẩn ${faculty.name} qua các năm`,
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
            },
            // Add onResize callback to ensure chart fits within 60% of viewport height
            onResize: (chart, size) => {
              const maxHeight = window.innerHeight * 0.6
              chart.canvas.parentNode.style.height = `${maxHeight}px`
            }
          }
        })
        
        // Set initial height for the chart container
        const maxHeight = window.innerHeight * 0.6
        chartContainer.style.height = `${maxHeight}px`
        chartContainer.style.maxHeight = '60vh'
      }
    },
    renderSingleMethodFacultyChart(majors, faculty, method, isSingleMethod = false) {
      const methodId = method.id
      
      // Lấy điểm của các ngành cho phương thức này
      const data = majors.map(major => {
        const methodData = major.admissionScores.find(m => m.methodId === methodId)
        return methodData && methodData.years[this.selectedYearForChart] 
          ? methodData.years[this.selectedYearForChart] 
          : null
      })
      
      // Kiểm tra nếu không có dữ liệu nào cho phương thức này
      if (data.every(score => score === null)) return
      
      const chartData = {
        labels: majors.map(major => major.name),
        datasets: [{
          label: method.name,
          data: data,
          backgroundColor: this.getMethodColor(methodId),
          borderColor: this.getMethodBorderColor(methodId),
          borderWidth: 2
        }]
      }
      
      // Tạo biểu đồ
      const refName = isSingleMethod ? 'singleFacultyMethodChart' : `facultyChart${methodId}`
      const ctx = this.$refs[refName]?.[isSingleMethod ? 0 : this.$refs[refName].length - 1]?.getContext('2d')
      
      if (ctx) {
        // Add chart container class and data attribute
        const chartContainer = ctx.canvas.parentNode
        chartContainer.classList.add('chart-container')
        if (isSingleMethod) {
          chartContainer.classList.add('single-method-chart')
        }
        chartContainer.setAttribute('data-chart-id', refName)
        
        this.charts[refName] = new Chart(ctx, {
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
                  autoSkip: false,
                  maxRotation: 90,
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
                text: isSingleMethod ? 
                  `Điểm chuẩn năm ${this.selectedYearForChart} - ${faculty.name}` :
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
            },
            // Add onResize callback to ensure chart fits within 60% of viewport height
            onResize: (chart, size) => {
              const maxHeight = window.innerHeight * 0.6
              chart.canvas.parentNode.style.height = `${maxHeight}px`
            }
          }
        })
        
        // Set initial height for the chart container
        const maxHeight = window.innerHeight * 0.6
        chartContainer.style.height = `${maxHeight}px`
        chartContainer.style.maxHeight = '60vh'
      }
    },
    renderUniversityChart() {
      if (!this.selectedYearForChart) return
      
      this.destroyAllCharts()
      
      // Nếu hiển thị tất cả các năm
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
        return
      }
      
      // Nếu chọn tất cả phương thức, tạo biểu đồ riêng cho từng phương thức
      if (this.selectedMethodForChart === 'all') {
        this.displayedMethods.forEach(method => {
          this.renderSingleMethodUniversityChart(method)
        })
      } else {
        // Nếu chọn một phương thức cụ thể, chỉ hiển thị biểu đồ cho phương thức đó
        const method = this.getMethodById(this.selectedMethodForChart)
        if (method) {
          this.renderSingleMethodUniversityChart(method, true)
        }
      }
    },
    renderAllYearsUniversityChart(method, isSingleMethod = false) {
      const methodId = method.id
      const years = [...this.availableYears].sort()
      
      const labels = []
      const datasets = []
      const colors = []
      
      // Tạo thành 2 cột cho mỗi ngành - mỗi năm 1 cột
      this.combinedData.forEach(major => {
        const majorName = major.name
        
        years.forEach(year => {
          const methodData = major.admissionScores.find(m => m.methodId === methodId)
          if (methodData && methodData.years[year]) {
            labels.push(`${majorName} (${year})`)
            datasets.push(methodData.years[year])
            colors.push(year === Math.min(...years) ? 
                       this.getMethodColor(methodId).replace('0.8', '0.6') : 
                       this.getMethodColor(methodId))
          }
        })
      })
      
      if (datasets.length === 0) return
      
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
      
      // Tạo biểu đồ
      const refName = isSingleMethod ? 'singleUniversityMethodAllYearsChart' : `universityChartAllYears${methodId}`
      const ctx = this.$refs[refName]?.[isSingleMethod ? 0 : this.$refs[refName].length - 1]?.getContext('2d')
      
      if (ctx) {
        // Add chart container class and data attribute
        const chartContainer = ctx.canvas.parentNode
        chartContainer.classList.add('chart-container')
        if (isSingleMethod) {
          chartContainer.classList.add('single-method-chart')
        }
        chartContainer.setAttribute('data-chart-id', refName)
        
        this.charts[refName] = new Chart(ctx, {
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
                  text: 'Ngành theo năm'
                },
                ticks: {
                  autoSkip: false,
                  maxRotation: 90,
                  minRotation: 45,
                  font: {
                    size: 10
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
                text: `Điểm chuẩn toàn trường qua các năm`,
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
            },
            // Add onResize callback to ensure chart fits within 60% of viewport height
            onResize: (chart, size) => {
              const maxHeight = window.innerHeight * 0.6
              chart.canvas.parentNode.style.height = `${maxHeight}px`
            }
          }
        })
        
        // Set initial height for the chart container
        const maxHeight = window.innerHeight * 0.6
        chartContainer.style.height = `${maxHeight}px`
        chartContainer.style.maxHeight = '60vh'
      }
    },
    renderSingleMethodUniversityChart(method, isSingleMethod = false) {
      const methodId = method.id
      
      // Lọc các ngành có điểm cho phương thức này
      const majorsWithData = this.combinedData.filter(major => {
        const methodData = major.admissionScores.find(m => m.methodId === methodId)
        return methodData && methodData.years[this.selectedYearForChart]
      })
      
      if (majorsWithData.length === 0) return
      
      const data = majorsWithData.map(major => {
        const methodData = major.admissionScores.find(m => m.methodId === methodId)
        return methodData.years[this.selectedYearForChart]
      })
      
      const chartData = {
        labels: majorsWithData.map(major => major.name),
        datasets: [{
          label: method.name,
          data: data,
          backgroundColor: this.getMethodColor(methodId),
          borderColor: this.getMethodBorderColor(methodId),
          borderWidth: 2
        }]
      }
      
      // Tạo biểu đồ
      const refName = isSingleMethod ? 'singleUniversityMethodChart' : `universityChart${methodId}`
      const ctx = this.$refs[refName]?.[isSingleMethod ? 0 : this.$refs[refName].length - 1]?.getContext('2d')
      
      if (ctx) {
        // Add chart container class and data attribute
        const chartContainer = ctx.canvas.parentNode
        chartContainer.classList.add('chart-container')
        if (isSingleMethod) {
          chartContainer.classList.add('single-method-chart')
        }
        chartContainer.setAttribute('data-chart-id', refName)
        
        this.charts[refName] = new Chart(ctx, {
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
                  autoSkip: false,
                  maxRotation: 90,
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
                text: isSingleMethod ? 
                  `Điểm chuẩn toàn trường năm ${this.selectedYearForChart}` :
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
            },
            // Add onResize callback to ensure chart fits within 60% of viewport height
            onResize: (chart, size) => {
              const maxHeight = window.innerHeight * 0.6
              chart.canvas.parentNode.style.height = `${maxHeight}px`
            }
          }
        })
        
        // Set initial height for the chart container
        const maxHeight = window.innerHeight * 0.6
        chartContainer.style.height = `${maxHeight}px`
        chartContainer.style.maxHeight = '60vh'
      }
    }
  }
}
</script>

<style scoped>
.pre-admission-container {
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header Section */
.header-section {
  background: linear-gradient(135deg, #003366 0%, #006699 100%);
  color: white;
  padding: 2.5rem 0 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  opacity: 0.9;
  font-weight: 300;
}

/* View Controls */
.view-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1.5rem 0 0.5rem;
  flex-wrap: wrap;
}

.display-type, .chart-type {
  margin: 0.5rem 0;
}

/* Content Section */
.content-section {
  flex: 1;
  padding: 2rem 0;
  background-color: #f8f9fa;
}

.loading-container, .error-container, .no-data-message {
  text-align: center;
  padding: 2rem;
  margin: 2rem 0;
}

/* Table Styles */
.filters {
  background-color: #fff;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

.table {
  width: 100%;
  margin-bottom: 0;
  border-collapse: collapse;
}

.table th, .table td {
  vertical-align: middle;
  text-align: center;
  border: 1px solid #dee2e6;
}

.table th {
  font-weight: 600;
  background-color: #004d80;
  color: white;
}

.method-header {
  background-color: #004d80 !important;
  color: white;
}

.year-header {
  background-color: #0096c7 !important;
}

.score-highlight {
  font-weight: bold;
  color: #007bff;
}

/* Chart Styles */
.chart-container {
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chart-wrapper {
  margin-top: 1.5rem;
}

.chart-title {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
  font-weight: 600;
}

.method-charts {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

/* Chuyển sang hiển thị dọc thay vì ma trận */
.vertical-charts {
  flex-direction: column;
}

/* Cải thiện container biểu đồ */
.method-chart-container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
  width: 100%;
}

.method-chart-container:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.method-chart-container h4 {
  text-align: center;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #333;
}

/* Sửa lại hiển thị xem tất cả các năm */
.all-years-view {
  width: 100%;
}

@media (max-width: 768px) {
  .method-chart-container {
    width: 100%;
    margin: 0 0 1.5rem 0;
  }
}
</style>