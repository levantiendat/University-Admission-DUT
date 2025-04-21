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
          <!-- Stat Type Navigation Menu -->
          <div class="stat-type-menu mb-4">
            <div class="card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center flex-wrap mb-3">
                  <h5 class="card-title m-0 mb-2 mb-md-0">Thống kê sinh viên trúng tuyển</h5>
                  <div class="stat-nav-buttons">
                    <button 
                      v-for="(statType, index) in statTypes" 
                      :key="index"
                      class="btn btn-sm mb-1"
                      :class="[selectedStatType === statType.value ? 'btn-primary' : 'btn-outline-primary']"
                      @click="changeStatType(statType.value)"
                    >
                      <i :class="statType.icon" class="me-1"></i>
                      {{ statType.label }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Filter options -->
          <div class="filters mb-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title mb-3">Tùy chọn hiển thị</h5>
                
                <div class="row">
                  <!-- Chart Type Selection (only for city and method) -->
                  <div class="col-md-4" v-if="selectedStatType === 'city' || selectedStatType === 'method'">
                    <div class="form-group mb-3">
                      <label for="chartType" class="form-label">Dạng biểu đồ:</label>
                      <select id="chartType" class="form-select" v-model="selectedChartType">
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
                </div>
  
                <div class="row">
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
  
          <!-- Chart display container - TĂNG KÍCH THƯỚC -->
          <div class="chart-container">
            <div class="card">
              <div class="card-body">
                <h3 class="chart-title">{{ chartTitle }}</h3>
                
                <!-- Gender Chart -->
                <div v-if="selectedStatType === 'gender'" class="chart-wrapper chart-wrapper-tall" id="gender-chart-container">
                  <div v-if="currentChartData && hasChartData" class="chart-inner-container">
                    <canvas ref="chartCanvas"></canvas>
                  </div>
                  <div v-else class="no-data-message text-center py-5">
                    <i class="fas fa-venus-mars fa-3x mb-3 text-muted"></i>
                    <h4>Không có dữ liệu về giới tính</h4>
                    <p>Không tìm thấy dữ liệu thống kê phù hợp với các điều kiện đã chọn.</p>
                  </div>
                </div>
                
                <!-- City Chart - TĂNG KÍCH THƯỚC -->
                <div v-else-if="selectedStatType === 'city'" class="chart-wrapper chart-wrapper-tall" id="city-chart-container">
                  <div v-if="currentChartData && hasChartData" class="chart-inner-container">
                    <canvas ref="chartCanvas"></canvas>
                  </div>
                  <div v-else class="no-data-message text-center py-5">
                    <i class="fas fa-city fa-3x mb-3 text-muted"></i>
                    <h4>Không có dữ liệu về thành phố</h4>
                    <p>Không tìm thấy dữ liệu thống kê phù hợp với các điều kiện đã chọn.</p>
                  </div>
                </div>
                
                <!-- Method Chart - TĂNG KÍCH THƯỚC -->
                <div v-else-if="selectedStatType === 'method'" class="chart-wrapper chart-wrapper-tall" id="method-chart-container">
                  <div v-if="currentChartData && hasChartData" class="chart-inner-container">
                    <canvas ref="chartCanvas"></canvas>
                  </div>
                  <div v-else class="no-data-message text-center py-5">
                    <i class="fas fa-tasks fa-3x mb-3 text-muted"></i>
                    <h4>Không có dữ liệu về phương thức xét tuyển</h4>
                    <p>Không tìm thấy dữ liệu thống kê phù hợp với các điều kiện đã chọn.</p>
                  </div>
                </div>
                
                <!-- Score Range Chart - Dùng bảng thay vì chart + TĂNG KÍCH THƯỚC -->
                <div v-else-if="selectedStatType === 'scoreRange'" class="chart-wrapper chart-wrapper-extra-tall">
                  <div v-if="currentChartData && hasChartData">
                    <div id="score-range-table-container" class="score-range-table-container">
                      <table class="table table-bordered table-hover">
                        <thead class="table-primary">
                          <tr>
                            <th>Khoảng điểm</th>
                            <th>Số lượng sinh viên</th>
                            <th>Tỷ lệ</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(value, index) in currentChartData.datasets[0].data" :key="index">
                            <td><strong>{{ currentChartData.labels[index] }}</strong></td>
                            <td>{{ value }}</td>
                            <td>{{ ((value / totalStudents) * 100).toFixed(1) }}%</td>
                          </tr>
                        </tbody>
                        <tfoot class="table-secondary">
                          <tr>
                            <th>Tổng cộng</th>
                            <th>{{ totalStudents }}</th>
                            <th>100%</th>
                          </tr>
                        </tfoot>
                      </table>
                      
                      <!-- Hiển thị biểu đồ cột đơn giản bằng các div - TĂNG KÍCH THƯỚC -->
                      <div class="score-bar-chart mt-5">
                        <h5 class="mb-4">Biểu đồ phân bố khoảng điểm</h5>
                        <div
                          v-for="(value, index) in currentChartData.datasets[0].data"
                          :key="index"
                          class="score-bar-item"
                        >
                          <div class="bar-label">{{ currentChartData.labels[index] }}</div>
                          <div class="bar-container">
                            <div
                              class="bar-value"
                              :style="{
                                width: `${(value / Math.max(...currentChartData.datasets[0].data)) * 100}%`,
                                backgroundColor: getScoreBarColor(index, currentChartData.datasets[0].data.length)
                              }"
                            ></div>
                            <span class="bar-text">{{ value }} sinh viên ({{ ((value / totalStudents) * 100).toFixed(1) }}%)</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="no-data-message text-center py-5">
                    <i class="fas fa-chart-line fa-3x mb-3 text-muted"></i>
                    <h4>Không có dữ liệu về khoảng điểm</h4>
                    <p>Không tìm thấy dữ liệu thống kê phù hợp với các điều kiện đã chọn.</p>
                  </div>
                </div>
  
                <!-- Summary stats below chart -->
                <div class="stats-summary mt-4" v-if="currentChartData && hasChartData">
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
        
        // Các loại biểu đồ 
        statTypes: [
          { value: 'gender', label: 'Giới tính', icon: 'fas fa-venus-mars' },
          { value: 'city', label: 'Thành phố', icon: 'fas fa-city' },
          { value: 'method', label: 'Phương thức xét tuyển', icon: 'fas fa-tasks' },
          { value: 'scoreRange', label: 'Khoảng điểm', icon: 'fas fa-chart-line' }
        ],
        
        // Chart object
        chart: null,
        
        // Dữ liệu biểu đồ
        currentChartData: null
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
      
      hasChartData() {
        return this.currentChartData && 
               this.currentChartData.datasets && 
               this.currentChartData.datasets[0] && 
               this.currentChartData.datasets[0].data &&
               this.currentChartData.datasets[0].data.length > 0 &&
               !this.currentChartData.datasets[0].data.every(val => val === 0);
      },
      
      // Tính toán tổng số sinh viên
      totalStudents() {
        if (!this.hasChartData) return 0;
        return this.currentChartData.datasets[0].data.reduce((sum, val) => sum + val, 0);
      },
      
      // Tính toán tỷ lệ nam/nữ
      genderRatio() {
        if (!this.hasChartData || this.selectedStatType !== 'gender') return 'N/A';
        
        const maleCount = this.currentChartData.datasets[0].data[0] || 0;
        const femaleCount = this.currentChartData.datasets[0].data[1] || 0;
        
        if (femaleCount === 0) return 'N/A';
        
        const ratio = (maleCount / femaleCount).toFixed(2);
        return `${ratio}:1`;
      },
      
      // Xác định item có giá trị cao nhất
      getTopItemText() {
        switch (this.selectedStatType) {
          case 'gender':
            return 'Giới tính chiếm đa số:';
          case 'city':
            return 'Thành phố có nhiều sinh viên nhất:';
          case 'method':
            return 'Phương thức xét tuyển phổ biến nhất:';
          case 'scoreRange':
            return 'Khoảng điểm phổ biến nhất:';
          default:
            return 'Giá trị phổ biến nhất:';
        }
      },
      
      // Lấy giá trị cao nhất
      topItemValue() {
        if (!this.hasChartData) return 'N/A';
        
        const data = this.currentChartData.datasets[0].data;
        const labels = this.currentChartData.labels;
        
        let maxIndex = 0;
        let maxValue = data[0];
        
        for (let i = 1; i < data.length; i++) {
          if (data[i] > maxValue) {
            maxValue = data[i];
            maxIndex = i;
          }
        }
        
        return `${labels[maxIndex]} (${maxValue} sinh viên)`;
      }
    },
    watch: {
      selectedChartType() {
        this.updateChartData();
      },
      selectedYear() {
        this.updateChartData();
      },
      selectedTargetType() {
        // Reset selected faculty and major when changing scope
        if (this.selectedTargetType !== 'faculty') {
          this.selectedFaculty = null;
        }
        if (this.selectedTargetType !== 'major') {
          this.selectedMajor = null;
          this.selectedFacultyForMajor = '';
        }
        this.updateChartData();
      },
      selectedFaculty() {
        this.updateChartData();
      },
      selectedFacultyForMajor() {
        // Khi chọn khoa mới cho ngành, đặt lại ngành đã chọn nếu ngành đó không thuộc khoa này
        if (this.selectedFacultyForMajor && this.selectedMajor) {
          const major = this.majors.find(m => m.id === parseInt(this.selectedMajor));
          if (major && major.faculty_id !== parseInt(this.selectedFacultyForMajor)) {
            this.selectedMajor = null;
          }
        }
        
        // Nếu danh sách ngành được lọc có ngành, chọn ngành đầu tiên
        if (this.filteredMajors.length > 0 && !this.selectedMajor) {
          this.selectedMajor = this.filteredMajors[0].id;
          this.updateChartData();
        }
      },
      selectedMajor() {
        this.updateChartData();
      }
    },
    async mounted() {
      await this.fetchData();
    },
    methods: {
      // Thay đổi loại thống kê
      changeStatType(statType) {
        // Hủy chart hiện tại trước khi đổi loại
        if (this.chart) {
          this.chart.destroy();
          this.chart = null;
        }
        
        this.selectedStatType = statType;
        
        // Thiết lập loại biểu đồ mặc định cho từng loại thống kê
        if (statType === 'gender') {
          this.selectedChartType = 'pie';
        } else if (statType === 'scoreRange') {
          this.selectedChartType = 'bar';
        }
        
        // Render biểu đồ tương ứng sau khi DOM cập nhật
        this.$nextTick(() => {
          this.updateChartData();
        });
      },
      
      // Lấy dữ liệu từ API
      async fetchData() {
        this.loading = true;
        this.error = null;
        
        try {
          // Lấy tất cả dữ liệu từ controller
          const data = await preAdmittedStudentController.getAllData();
          
          // Cập nhật state
          this.faculties = data.faculties || [];
          this.majors = data.majors || [];
          this.cities = data.cities || [];
          this.admissionMethods = data.admissionMethods || [];
          this.stats = {
            gender: data.stats?.gender || [],
            city: data.stats?.city || [],
            method: data.stats?.method || [],
            scoreRange: data.stats?.scoreRange || []
          };
          this.availableYears = data.availableYears || [];
          
          // Thiết lập giá trị mặc định
          if (this.availableYears.length > 0) {
            this.selectedYear = Math.max(...this.availableYears);
          }
          
          if (this.faculties.length > 0) {
            this.selectedFaculty = this.faculties[0].id;
          }
          
          if (this.majors.length > 0) {
            this.selectedMajor = this.majors[0].id;
          }
          
          // Cập nhật dữ liệu và render biểu đồ đầu tiên
          this.$nextTick(() => {
            this.updateChartData();
          });
        } catch (err) {
          this.error = `Không thể tải dữ liệu: ${err.message}`;
          console.error('Fetch data error:', err);
        } finally {
          this.loading = false;
        }
      },
      
      // Cập nhật dữ liệu cho biểu đồ
      updateChartData() {
        try {
          // Điều kiện lọc dữ liệu
          const conditions = {
            year: parseInt(this.selectedYear)
          }
          
          // Xác định major_id dựa trên phạm vi thống kê
          if (this.selectedTargetType === 'major' && this.selectedMajor) {
            conditions.majorId = parseInt(this.selectedMajor)
          } else if (this.selectedTargetType === 'faculty' && this.selectedFaculty) {
            conditions.facultyId = parseInt(this.selectedFaculty)
            conditions.majorsInFaculty = preAdmittedStudentController.getMajorIdsByFaculty(
              this.majors,
              parseInt(this.selectedFaculty)
            )
          }
          
          // Lấy dữ liệu thống kê dựa trên loại đã chọn
          switch (this.selectedStatType) {
            case 'gender':
              this.currentChartData = preAdmittedStudentController.prepareGenderStatsData(
                this.stats.gender,
                conditions,
                this.majors
              );
              break;
            case 'city':
              this.currentChartData = preAdmittedStudentController.prepareCityStatsData(
                this.stats.city,
                conditions,
                this.cities,
                10
              );
              break;
            case 'method':
              this.currentChartData = preAdmittedStudentController.prepareMethodStatsData(
                this.stats.method,
                conditions,
                this.admissionMethods
              );
              break;
            case 'scoreRange':
              this.currentChartData = preAdmittedStudentController.prepareScoreRangeStatsData(
                this.stats.scoreRange,
                conditions
              );
              break;
            default:
              this.currentChartData = null;
          }
          
          // Render biểu đồ hiện tại sau khi dữ liệu đã được cập nhật
          this.$nextTick(() => {
            this.renderChart();
          });
        } catch (error) {
          console.error('Error updating chart data:', error);
          this.currentChartData = null;
        }
      },
      
      // Lấy màu cho thanh biểu đồ khoảng điểm
      getScoreBarColor(index, total) {
        // Tạo gradient màu từ xanh lá (thấp) đến đỏ (cao)
        const ratio = total > 1 ? index / (total - 1) : 0;
        
        const r = Math.round(75 + ratio * (255 - 75));
        const g = Math.round(192 - ratio * (192 - 99));
        const b = Math.round(192 - ratio * (192 - 132));
        
        return `rgba(${r}, ${g}, ${b}, 0.8)`;
      },
      
      // Render biểu đồ với kích thước lớn hơn
      renderChart() {
        // Không render chart nếu là khoảng điểm (đã dùng bảng và biểu đồ thanh tùy chỉnh)
        if (this.selectedStatType === 'scoreRange' || !this.hasChartData) {
          return;
        }
        
        this.$nextTick(() => {
          try {
            // Hủy chart cũ nếu tồn tại
            if (this.chart) {
              this.chart.destroy();
              this.chart = null;
            }
            
            // Lấy canvas element
            const canvas = this.$refs.chartCanvas;
            if (!canvas) {
              console.error('Canvas element not found');
              return;
            }
            
            // Xác định loại biểu đồ
            let chartType = this.selectedChartType;
            
            // Với giới tính luôn hiển thị dạng tròn
            if (this.selectedStatType === 'gender') {
              chartType = 'pie';
            }
            
            // Tạo deep copy của dữ liệu để tránh tham chiếu
            const chartData = JSON.parse(JSON.stringify(this.currentChartData));
            
            // Cấu hình cho biểu đồ với kích thước lớn hơn
            const options = {
              responsive: true,
              maintainAspectRatio: false, // Quan trọng để điều chỉnh kích thước
              plugins: {
                legend: {
                  position: chartType === 'pie' ? 'right' : 'top',
                  display: chartType === 'pie',
                  labels: {
                    font: {
                      size: 14, // Tăng kích thước chữ của legend
                      weight: '500'
                    },
                    padding: 15 // Thêm padding cho labels
                  }
                },
                tooltip: {
                  bodyFont: {
                    size: 14 // Tăng kích thước chữ của tooltip
                  },
                  titleFont: {
                    size: 16,
                    weight: 'bold'
                  },
                  padding: 12,
                  callbacks: {
                    label: (context) => {
                      const value = context.raw;
                      const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                      const percentage = ((value / total) * 100).toFixed(1);
                      return `${context.label || ''}: ${value} (${percentage}%)`;
                    }
                  }
                }
              }
            };
            
            // Thêm scales cho biểu đồ cột với kích thước lớn hơn
            if (chartType === 'bar') {
              // Xác định giá trị tối đa trên trục Y
              const maxValue = Math.max(...chartData.datasets[0].data);
              
              // Tính toán phân vị (stepSize) dựa trên phạm vi thống kê
              let stepSize = 10; 
              
              if (this.selectedTargetType === 'university') {
                // Với toàn trường, dùng phân vị lớn hơn
                stepSize = Math.ceil(maxValue / 5 / 100) * 100;
                stepSize = Math.max(stepSize, 100); // Đảm bảo tối thiểu là 100
              } else {
                // Với khoa, ngành dùng phân vị nhỏ hơn
                stepSize = Math.ceil(maxValue / 5 / 10) * 10;
                stepSize = Math.max(stepSize, 10); // Đảm bảo tối thiểu là 10
              }
              
              options.scales = {
                y: {
                  grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                    lineWidth: 1
                  },
                  beginAtZero: true,
                  title: {
                    display: true,
                    text: 'Số lượng sinh viên',
                    font: { 
                      size: 16, // Tăng kích thước tiêu đề
                      weight: 'bold'
                    },
                    padding: {
                      bottom: 15
                    }
                  },
                  ticks: {
                    stepSize: stepSize,  // Thiết lập phân vị theo khoảng đã tính
                    font: {
                      size: 14 // Tăng kích thước chữ
                    },
                    padding: 10
                  }
                },
                x: {
                  grid: {
                    display: false
                  },
                  title: {
                    display: true,
                    text: this.selectedStatType === 'city' ? 'Thành phố' : 
                          this.selectedStatType === 'method' ? 'Phương thức xét tuyển' : 'Giá trị',
                    font: { 
                      size: 16, // Tăng kích thước tiêu đề
                      weight: 'bold'
                    },
                    padding: {
                      top: 15
                    }
                  },
                  ticks: {
                    maxRotation: 45,
                    minRotation: 45,
                    font: {
                      size: 12 // Tăng kích thước chữ
                    }
                  }
                }
              };
            }
            
            // Tăng kích thước của nét vẽ và điểm
            if (chartData.datasets && chartData.datasets.length > 0) {
              chartData.datasets.forEach(dataset => {
                dataset.borderWidth = 2; // Tăng độ rộng của đường viền
                if (chartType === 'pie') {
                  dataset.hoverOffset = 15; // Tăng offset khi hover trên biểu đồ tròn
                }
              });
            }
            
            // Tạo biểu đồ mới
            this.chart = new Chart(canvas.getContext('2d'), {
              type: chartType,
              data: chartData,
              options: options
            });
          } catch (error) {
            console.error('Error rendering chart:', error);
          }
        });
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
  
  /* Stat Type Menu */
  .stat-type-menu .btn {
    margin: 0 0.25rem;
    padding: 0.375rem 0.75rem;
  }
  
  .stat-nav-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    justify-content: flex-end;
  }
  
  @media (max-width: 768px) {
    .stat-nav-buttons {
      justify-content: center;
      margin-top: 0.5rem;
    }
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
    margin-bottom: 2rem;
    font-weight: 600;
    font-size: 1.75rem;
    color: #004d80;
  }
  
  /* TĂNG KÍCH THƯỚC BIỂU ĐỒ */
  .chart-wrapper {
    height: auto;
    min-height: 600px; /* Tăng từ 500px lên 600px */
    max-width: 100%;
    margin: 0 auto;
    position: relative;
    padding: 15px;
  }
  
  .chart-wrapper-tall {
    height: 700px; /* Tăng kích thước cho biểu đồ */
  }
  
  .chart-wrapper-extra-tall {
    min-height: 800px; /* Tăng kích thước đặc biệt cho biểu đồ khoảng điểm */
  }
  
  .chart-inner-container {
    width: 100%;
    height: 100%;
    position: relative;
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
    padding: 1rem 1.25rem; /* Tăng padding cho items */
    font-size: 1.1rem; /* Tăng kích thước chữ */
  }
  
  .stats-summary .badge {
    font-size: 1rem; /* Tăng kích thước của badge */
    padding: 0.5rem 0.75rem; /* Tăng padding cho badge */
  }
  
  /* Score Range Table */
  .score-range-table-container {
    overflow-x: auto;
  }
  
  .score-range-table-container table {
    margin-bottom: 0;
    font-size: 1.1rem; /* Tăng kích thước chữ trong bảng */
  }
  
  .score-range-table-container th,
  .score-range-table-container td {
    padding: 0.75rem 1rem; /* Tăng padding trong cells */
  }
  
  /* Score Bar Chart */
  .score-bar-chart {
    margin-top: 3rem; /* Tăng margin */
  }
  
  .score-bar-chart h5 {
    font-size: 1.35rem; /* Tăng kích thước tiêu đề */
    margin-bottom: 2rem;
    font-weight: 600;
    color: #004d80;
  }
  
  .score-bar-item {
    margin-bottom: 2rem; /* Tăng khoảng cách giữa các thanh */
  }
  
  .bar-label {
    font-weight: 600;
    margin-bottom: 10px; /* Tăng margin */
    font-size: 1.1rem; /* Tăng kích thước chữ */
  }
  
  .bar-container {
    height: 50px; /* Tăng chiều cao của thanh từ 25px lên 50px */
    background-color: #f1f1f1;
    border-radius: 8px; /* Tăng border radius */
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .bar-value {
    height: 100%;
    border-radius: 6px; /* Tăng border radius */
    transition: width 0.8s ease;
  }
  
  .bar-text {
    position: absolute;
    left: 15px; /* Tăng padding bên trái */
    top: 50%;
    transform: translateY(-50%);
    color: #000;
    font-weight: 600;
    text-shadow: 0px 0px 5px rgba(255, 255, 255, 0.9);
    font-size: 1.05rem; /* Tăng kích thước chữ */
  }
  
  /* Responsive adjustments */
  @media (max-width: 992px) {
    .chart-wrapper,
    .chart-wrapper-tall {
      height: 600px; /* Giảm chiều cao một chút trên màn hình trung bình */
    }
    
    .chart-wrapper-extra-tall {
      min-height: 700px;
    }
  }
  
  @media (max-width: 768px) {
    .chart-wrapper,
    .chart-wrapper-tall {
      height: 500px; /* Giảm chiều cao trên mobile */
    }
    
    .chart-wrapper-extra-tall {
      min-height: 600px;
    }
    
    .stats-summary {
      margin-top: 1.5rem;
    }
    
    .bar-container {
      height: 40px; /* Giảm chiều cao thanh trên mobile */
    }
    
    .bar-text {
      font-size: 0.9rem;
    }
    
    .chart-title {
      font-size: 1.5rem;
      margin-bottom: 1.5rem;
    }
  }
  
  /* Thêm clearfix để đảm bảo container luôn chứa đầy đủ nội dung */
  .chart-container::after {
    content: "";
    display: table;
    clear: both;
  }
  </style>