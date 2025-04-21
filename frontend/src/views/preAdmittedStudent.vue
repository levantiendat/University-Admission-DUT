<template>
    <div class="pre-admitted-container">
      <div class="header-section">
        <div class="container">
          <h1 class="main-title">Thống Kê Sinh Viên Trúng Tuyển</h1>
          <p class="subtitle">Phân tích dữ liệu sinh viên trúng tuyển các năm 2023, 2024 để có cái nhìn tổng quan về xu hướng tuyển sinh</p>
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
  
        <!-- Main content when data is loaded -->
        <div v-else class="statistics-container">
          <!-- Filter options -->
          <div class="filters mb-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title mb-3">Tùy chọn hiển thị</h5>
                
                <div class="row">
                  <div class="col-md-4">
                    <div class="form-group mb-3">
                      <label for="statType" class="form-label">Loại thống kê:</label>
                      <select id="statType" class="form-select" v-model="selectedStatType">
                        <option value="gender">Theo giới tính</option>
                        <option value="city">Theo thành phố</option>
                        <option value="method">Theo phương thức xét tuyển</option>
                        <option value="scoreRange">Theo khoảng điểm xét tuyển</option>
                      </select>
                    </div>
                  </div>
  
                  <div class="col-md-4">
                    <div class="form-group mb-3">
                      <label for="chartType" class="form-label">Dạng biểu đồ:</label>
                      <select id="chartType" class="form-select" v-model="selectedChartType" 
                              :disabled="selectedStatType === 'gender' || selectedStatType === 'scoreRange'">
                        <option value="pie">Biểu đồ tròn (Pie chart)</option>
                        <option value="bar">Biểu đồ cột (Bar chart)</option>
                      </select>
                    </div>
                  </div>
  
                  <div class="col-md-4">
                    <div class="form-group mb-3">
                      <label for="year" class="form-label">Năm:</label>
                      <select id="year" class="form-select" v-model="selectedYear">
                        <option v-for="year in availableYears" :key="year" :value="year">
                          {{ year }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
  
                <div class="row">
                  <div class="col-md-4">
                    <div class="form-group mb-3">
                      <label for="targetType" class="form-label">Phạm vi thống kê:</label>
                      <select id="targetType" class="form-select" v-model="selectedTargetType">
                        <option value="university">Toàn trường</option>
                        <option value="faculty">Theo khoa</option>
                        <option value="major">Theo ngành</option>
                      </select>
                    </div>
                  </div>
  
                  <div class="col-md-4" v-if="selectedTargetType === 'faculty'">
                    <div class="form-group mb-3">
                      <label for="faculty" class="form-label">Chọn khoa:</label>
                      <select id="faculty" class="form-select" v-model="selectedFaculty">
                        <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                          {{ faculty.name }}
                        </option>
                      </select>
                    </div>
                  </div>
  
                  <div class="col-md-4" v-if="selectedTargetType === 'major'">
                    <div class="form-group mb-3">
                      <label for="faculty-for-major" class="form-label">Chọn khoa:</label>
                      <select id="faculty-for-major" class="form-select" v-model="selectedFacultyForMajor">
                        <option value="">Tất cả các khoa</option>
                        <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                          {{ faculty.name }}
                        </option>
                      </select>
                    </div>
                  </div>
  
                  <div class="col-md-4" v-if="selectedTargetType === 'major'">
                    <div class="form-group mb-3">
                      <label for="major" class="form-label">Chọn ngành:</label>
                      <select id="major" class="form-select" v-model="selectedMajor">
                        <option v-for="major in filteredMajors" :key="major.id" :value="major.id">
                          {{ major.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Chart display -->
          <div class="chart-container">
            <div class="card">
              <div class="card-body">
                <h3 class="chart-title">{{ chartTitle }}</h3>
                
                <div class="chart-wrapper" v-if="hasData">
                  <canvas ref="chartElement"></canvas>
                </div>
                
                <div v-else class="no-data-message text-center py-5">
                  <i class="fas fa-chart-pie fa-3x mb-3 text-muted"></i>
                  <h4>Không có dữ liệu</h4>
                  <p>Không tìm thấy dữ liệu thống kê phù hợp với các điều kiện đã chọn.</p>
                </div>
  
                <!-- Summary stats below chart -->
                <div class="stats-summary mt-4" v-if="hasData">
                  <div class="card bg-light">
                    <div class="card-body">
                      <h5 class="card-title">Thông tin tổng hợp</h5>
                      <ul class="list-group list-group-flush">
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          Tổng số sinh viên:
                          <span class="badge bg-primary rounded-pill">{{ totalStudents }}</span>
                        </li>
                        <li v-if="selectedStatType === 'gender'" class="list-group-item d-flex justify-content-between align-items-center">
                          Tỷ lệ Nam/Nữ:
                          <span class="badge bg-info rounded-pill">{{ genderRatio }}</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          {{ getTopItemText }}
                          <span class="badge bg-success rounded-pill">{{ topItemValue }}</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import preAdmittedStudentController from '@/controllers/preAdmittedStudentController'
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'PreAdmittedStudentView',
    data() {
      return {
        // Dữ liệu từ API
        faculties: [],
        majors: [],
        cities: [],
        admissionMethods: [],
        stats: {
          gender: [],
          city: [],
          method: [],
          scoreRange: []
        },
        availableYears: [],
        
        // Trạng thái UI
        loading: true,
        error: null,
        
        // Tùy chọn hiển thị
        selectedStatType: 'gender',
        selectedChartType: 'pie',
        selectedYear: null,
        selectedTargetType: 'university',
        selectedFaculty: null,
        selectedFacultyForMajor: '',
        selectedMajor: null,
        
        // Chart object
        chart: null,
        
        // Dữ liệu hiện tại
        currentDate: '2025-04-21 00:49:35',
        currentUser: 'levantiendatCác'
      }
    },
    computed: {
      filteredMajors() {
        if (!this.majors || this.majors.length === 0) return []
        
        if (this.selectedFacultyForMajor) {
          return this.majors.filter(major => major.faculty_id === parseInt(this.selectedFacultyForMajor))
        }
        
        return this.majors
      },
      chartTitle() {
        let targetName = ''
        if (this.selectedTargetType === 'major' && this.selectedMajor) {
          const major = this.majors.find(m => m.id === parseInt(this.selectedMajor))
          targetName = major ? major.name : 'Ngành không xác định'
        } else if (this.selectedTargetType === 'faculty' && this.selectedFaculty) {
          const faculty = this.faculties.find(f => f.id === parseInt(this.selectedFaculty))
          targetName = faculty ? faculty.name : 'Khoa không xác định'
        } else {
          targetName = 'Toàn trường'
        }
        
        return preAdmittedStudentController.getChartTitle(
          this.selectedStatType,
          this.selectedTargetType,
          targetName,
          this.selectedYear
        )
      },
      chartData() {
        // Điều kiện lọc dữ liệu
        const conditions = {
          year: this.selectedYear
        }
        
        // Xác định major_id dựa trên phạm vi thống kê
        if (this.selectedTargetType === 'major' && this.selectedMajor) {
          conditions.majorId = parseInt(this.selectedMajor)
        } else if (this.selectedTargetType === 'faculty' && this.selectedFaculty) {
          conditions.facultyId = parseInt(this.selectedFaculty)
          conditions.majorsInFaculty = preAdmittedStudentController.getMajorIdsByFaculty(
            this.majors,
            this.selectedFaculty
          )
        }
        
        // Lấy dữ liệu thống kê dựa trên loại đã chọn
        switch (this.selectedStatType) {
          case 'gender':
            return preAdmittedStudentController.prepareGenderStatsData(
              this.stats.gender,
              conditions,
              this.majors
            )
          case 'city':
            return preAdmittedStudentController.prepareCityStatsData(
              this.stats.city,
              conditions,
              this.cities,
              10 // Hiển thị top 10 thành phố
            )
          case 'method':
            return preAdmittedStudentController.prepareMethodStatsData(
              this.stats.method,
              conditions,
              this.admissionMethods
            )
          case 'scoreRange':
            return preAdmittedStudentController.prepareScoreRangeStatsData(
              this.stats.scoreRange,
              conditions
            )
          default:
            return null
        }
      },
      hasData() {
        return this.chartData !== null && 
               this.chartData.datasets[0].data.length > 0 &&
               !this.chartData.datasets[0].data.every(val => val === 0)
      },
      
      // Tính toán tổng số sinh viên
      totalStudents() {
        if (!this.hasData) return 0
        return this.chartData.datasets[0].data.reduce((sum, val) => sum + val, 0)
      },
      
      // Tính toán tỷ lệ nam/nữ
      genderRatio() {
        if (!this.hasData || this.selectedStatType !== 'gender') return 'N/A'
        
        const maleCount = this.chartData.datasets[0].data[0] || 0
        const femaleCount = this.chartData.datasets[0].data[1] || 0
        
        if (femaleCount === 0) return 'N/A'
        
        const ratio = (maleCount / femaleCount).toFixed(2)
        return `${ratio}:1`
      },
      
      // Xác định item có giá trị cao nhất
      getTopItemText() {
        switch (this.selectedStatType) {
          case 'gender':
            return 'Giới tính chiếm đa số:'
          case 'city':
            return 'Thành phố có nhiều sinh viên nhất:'
          case 'method':
            return 'Phương thức xét tuyển phổ biến nhất:'
          case 'scoreRange':
            return 'Khoảng điểm phổ biến nhất:'
          default:
            return 'Giá trị phổ biến nhất:'
        }
      },
      
      // Lấy giá trị cao nhất
      topItemValue() {
        if (!this.hasData) return 'N/A'
        
        const data = this.chartData.datasets[0].data
        const labels = this.chartData.labels
        
        let maxIndex = 0
        let maxValue = data[0]
        
        for (let i = 1; i < data.length; i++) {
          if (data[i] > maxValue) {
            maxValue = data[i]
            maxIndex = i
          }
        }
        
        return `${labels[maxIndex]} (${maxValue} sinh viên)`
      }
    },
    watch: {
      selectedStatType() {
        // Đặt lại loại biểu đồ khi thay đổi loại thống kê
        if (this.selectedStatType === 'gender') {
          this.selectedChartType = 'pie'
        } else if (this.selectedStatType === 'scoreRange') {
          this.selectedChartType = 'bar'
        }
        
        this.renderChart()
      },
      selectedChartType() {
        this.renderChart()
      },
      selectedYear() {
        this.renderChart()
      },
      selectedTargetType() {
        // Reset selected faculty and major when changing scope
        if (this.selectedTargetType !== 'faculty') {
          this.selectedFaculty = null
        }
        if (this.selectedTargetType !== 'major') {
          this.selectedMajor = null
          this.selectedFacultyForMajor = ''
        }
        this.renderChart()
      },
      selectedFaculty() {
        this.renderChart()
      },
      selectedFacultyForMajor() {
        // Khi chọn khoa mới cho ngành, đặt lại ngành đã chọn nếu ngành đó không thuộc khoa này
        if (this.selectedFacultyForMajor && this.selectedMajor) {
          const major = this.majors.find(m => m.id === parseInt(this.selectedMajor))
          if (major && major.faculty_id !== parseInt(this.selectedFacultyForMajor)) {
            this.selectedMajor = null
          }
        }
        
        // Nếu danh sách ngành được lọc có ngành, chọn ngành đầu tiên
        this.$nextTick(() => {
          if (this.filteredMajors.length > 0 && !this.selectedMajor) {
            this.selectedMajor = this.filteredMajors[0].id
          }
        })
      },
      selectedMajor() {
        this.renderChart()
      }
    },
    async mounted() {
      await this.fetchData()
    },
    methods: {
      async fetchData() {
        this.loading = true
        this.error = null
        
        try {
          // Lấy tất cả dữ liệu từ controller
          const data = await preAdmittedStudentController.getAllData()
          
          // Cập nhật state
          this.faculties = data.faculties
          this.majors = data.majors
          this.cities = data.cities
          this.admissionMethods = data.admissionMethods
          this.stats = data.stats
          this.availableYears = data.availableYears
          
          // Thiết lập giá trị mặc định
          if (this.availableYears.length > 0) {
            this.selectedYear = Math.max(...this.availableYears)
          }
          
          if (this.faculties.length > 0) {
            this.selectedFaculty = this.faculties[0].id
          }
          
          if (this.majors.length > 0) {
            this.selectedMajor = this.majors[0].id
          }
          
          // Render biểu đồ ban đầu
          this.$nextTick(() => {
            this.renderChart()
          })
        } catch (err) {
          this.error = `Không thể tải dữ liệu: ${err.message}`
          console.error('Fetch data error:', err)
        } finally {
          this.loading = false
        }
      },
      
      renderChart() {
        // Hủy biểu đồ cũ nếu có
        if (this.chart) {
          this.chart.destroy()
          this.chart = null
        }
        
        // Nếu không có dữ liệu, không vẽ biểu đồ
        if (!this.hasData) return
        
        // Lấy element canvas
        const ctx = this.$refs.chartElement?.getContext('2d')
        if (!ctx) return
        
        // Xác định loại biểu đồ
        let chartType = this.selectedChartType
        
        // Với khoảng điểm luôn hiển thị dạng cột
        if (this.selectedStatType === 'scoreRange') {
          chartType = 'bar'
        }
        
        // Với giới tính luôn hiển thị dạng tròn
        if (this.selectedStatType === 'gender') {
          chartType = 'pie'
        }
        
        // Tạo cấu hình cho biểu đồ
        const options = this.getChartOptions(chartType)
        
        // Tạo biểu đồ mới
        this.chart = new Chart(ctx, {
          type: chartType,
          data: this.chartData,
          options: options
        })
      },
      
      getChartOptions(chartType) {
        // Cấu hình chung cho tất cả biểu đồ
        const common = {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                font: {
                  size: 14
                }
              }
            },
            tooltip: {
              padding: 12,
              bodyFont: {
                size: 14
              },
              callbacks: {
                label: (context) => {
                  const value = context.raw
                  const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0)
                  const percentage = ((value / total) * 100).toFixed(1)
                  return `${context.label || ''}: ${value} (${percentage}%)`
                }
              }
            }
          }
        }
        
        // Cấu hình riêng cho từng loại biểu đồ
        if (chartType === 'pie') {
          return {
            ...common,
            plugins: {
              ...common.plugins,
              legend: {
                ...common.plugins.legend,
                position: 'right'
              }
            }
          }
        } else if (chartType === 'bar') {
          // Cấu hình riêng cho biểu đồ cột
          const barConfig = {
            ...common,
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Số lượng sinh viên',
                  font: {
                    size: 14,
                    weight: 'bold'
                  }
                }
              },
              x: {
                title: {
                  display: true,
                  text: this.getXAxisTitle(),
                  font: {
                    size: 14,
                    weight: 'bold'
                  }
                },
                ticks: {
                  maxRotation: 45,
                  minRotation: 45
                }
              }
            }
          }
          
          // Đặc biệt cho biểu đồ thành phố có thể có nhiều item
          if (this.selectedStatType === 'city') {
            barConfig.scales.x.ticks.font = {
              size: 11
            }
          }
          
          return barConfig
        }
        
        return common
      },
      
      getXAxisTitle() {
        switch (this.selectedStatType) {
          case 'gender':
            return 'Giới tính'
          case 'city':
            return 'Thành phố'
          case 'method':
            return 'Phương thức xét tuyển'
          case 'scoreRange':
            return 'Khoảng điểm'
          default:
            return ''
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .pre-admitted-container {
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
  
  /* Content Section */
  .content-section {
    flex: 1;
    padding: 2rem 0;
    background-color: #f8f9fa;
  }
  
  .loading-container, .error-container {
    text-align: center;
    padding: 2rem;
    margin: 2rem 0;
  }
  
  /* Filters */
  .filters .card {
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
  }
  
  .filters .card:hover {
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
  
  .filters .card-title {
    color: #004d80;
    font-weight: 600;
  }
  
  /* Chart Container */
  .chart-container {
    margin-top: 2rem;
  }
  
  .chart-container .card {
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
  }
  
  .chart-container .card:hover {
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
  
  .chart-title {
    text-align: center;
    margin-bottom: 1.5rem;
    font-weight: 600;
    color: #004d80;
  }
  
  .chart-wrapper {
    height: 500px;
    max-width: 100%;
    margin: 0 auto;
  }
  
  .no-data-message {
    color: #6c757d;
  }
  
  /* Summary stats */
  .stats-summary {
    margin-top: 2rem;
  }
  
  .stats-summary .card {
    border: none;
    border-radius: 10px;
  }
  
  .stats-summary .card-title {
    color: #004d80;
    font-weight: 600;
  }
  
  .stats-summary .list-group-item {
    background-color: transparent;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .chart-wrapper {
      height: 400px;
    }
    
    .stats-summary {
      margin-top: 1rem;
    }
  }
  </style>