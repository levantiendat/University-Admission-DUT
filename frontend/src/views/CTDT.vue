<template>
  <div class="ctdt-container">
    <div class="container py-3">
      <!-- Breadcrumb Navigation -->
      <nav aria-label="breadcrumb" class="mb-3">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/" class="text-decoration-none">
              <i class="fas fa-home"></i> Trang chủ
            </router-link>
          </li>
          <li class="breadcrumb-item">
            <router-link to="/ctdt" class="text-decoration-none">
              Chương trình đào tạo
            </router-link>
          </li>
          <li class="breadcrumb-item active" aria-current="page" v-if="facultyName">
            {{ facultyName }}
          </li>
        </ol>
      </nav>
      
      <!-- Main Content -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow border-0 ctdt-card">
            <div class="card-header ctdt-header d-flex align-items-center">
              <h1 class="fs-4 text-white mb-0">Chương Trình Đào Tạo</h1>
            </div>
            
            <div class="card-body">
              <!-- Filter Controls -->
              <div class="row mb-4">
                <div class="col-md-5">
                  <div class="form-group">
                    <label for="majorSelect" class="form-label fw-bold">Chọn ngành học:</label>
                    <select 
                      id="majorSelect" 
                      v-model="selectedMajorId" 
                      class="form-select shadow-sm" 
                      @change="onMajorChange"
                    >
                      <option value="" disabled selected>-- Chọn ngành học --</option>
                      <option v-for="major in majors" :key="major.id" :value="major.id">
                        {{ major.name }}
                      </option>
                    </select>
                  </div>
                </div>
                
                <div class="col-md-5">
                  <div class="form-group">
                    <label for="majorCourseSelect" class="form-label fw-bold">Chọn chương trình:</label>
                    <select 
                      id="majorCourseSelect" 
                      v-model="selectedMajorCourseId" 
                      class="form-select shadow-sm"
                      :disabled="!majorCourses.length"
                    >
                      <option value="" disabled selected>-- Chọn chương trình --</option>
                      <option v-for="course in majorCourses" :key="course.id" :value="course.id">
                        {{ course.year }} - {{ course.type }}
                      </option>
                    </select>
                  </div>
                </div>
                
                <div class="col-md-2 d-flex align-items-end">
                  <button 
                    class="btn btn-primary w-100" 
                    @click="searchCourseDetails"
                    :disabled="!selectedMajorCourseId || isLoading"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-1" role="status"></span>
                    <span>Tìm kiếm</span>
                  </button>
                </div>
              </div>
              
              <!-- Alerts -->
              <div v-if="showAlert" class="alert mb-4" :class="alertClass" role="alert">
                {{ alertMessage }}
              </div>
              
              <!-- Course Details Table -->
              <div v-if="courseDetails.length" class="course-table-container">
                <div class="table-responsive custom-scrollbar">
                  <table class="table table-bordered no-copy custom-table">
                    <thead>
                      <tr class="align-middle text-center table-header">
                        <th scope="col" style="width: 50px;">TT</th>
                        <th scope="col" style="width: 80px;">Học kỳ</th>
                        <th scope="col">Tên học phần</th>
                        <th scope="col" style="width: 100px;">Mã HP</th>
                        <th scope="col" style="width: 80px;">Số tín chỉ</th>
                        <th scope="col" style="width: 80px;">Tự chọn</th>
                        <th scope="col" style="width: 80px;">HT ĐA</th>
                        <th scope="col" style="width: 80px;">TQ ĐA</th>
                        <th scope="col">Học phần cần học trước</th>
                        <th scope="col">Học song hành với học phần</th>
                        <th scope="col">Cần học phần tiên quyết</th>
                      </tr>
                    </thead>
                    <tbody>
                      <template v-for="(groupedCourses, semester) in groupedBySemester">
                        <!-- Semester Header -->
                        <tr class="semester-header">
                          <td colspan="11" class="bg-light fw-bold">
                            Học kỳ {{ semester }}
                          </td>
                        </tr>
                        <!-- Courses for this semester -->
                        <tr v-for="(detail, index) in groupedCourses" :key="detail.id" :class="{'row-even': index % 2 === 0}">
                          <td class="text-center">{{ getOverallIndex(semester, index) }}</td>
                          <td class="text-center">{{ detail.semester }}</td>
                          <td class="course-name">{{ detail.course?.name }}</td>
                          <td class="text-center">{{ detail.course?.course_code }}</td>
                          <td class="text-center">{{ detail.course?.credits }}</td>
                          <td class="text-center">
                            <span v-if="detail.elective_course" class="check-icon">✓</span>
                          </td>
                          <td class="text-center">
                            <span v-if="detail.pre_capstone" class="check-icon">✓</span>
                          </td>
                          <td class="text-center">
                            <span v-if="detail.mandatory_capstone" class="check-icon">✓</span>
                          </td>
                          <td class="relationship-cell">
                            <div v-for="(prior, priorIndex) in detail.priorCourses" :key="'prior-' + priorIndex">
                              {{ prior.code }} - {{ prior.name }}
                            </div>
                            <span v-if="!detail.priorCourses.length">-</span>
                          </td>
                          <td class="relationship-cell">
                            <div v-for="(coreq, coreqIndex) in detail.corequisites" :key="'coreq-' + coreqIndex">
                              {{ coreq.code }} - {{ coreq.name }}
                            </div>
                            <span v-if="!detail.corequisites.length">-</span>
                          </td>
                          <td class="relationship-cell">
                            <div v-for="(prereq, prereqIndex) in detail.prerequisites" :key="'prereq-' + prereqIndex">
                              {{ prereq.code }} - {{ prereq.name }}
                            </div>
                            <span v-if="!detail.prerequisites.length">-</span>
                          </td>
                        </tr>
                      </template>
                    </tbody>
                  </table>
                </div>
                
                <!-- Legend -->
                <div class="legend mt-4">
                  <div class="d-flex flex-wrap">
                    <div class="me-4 mb-2">
                      <span class="check-icon me-1">✓</span> <strong>Tự chọn:</strong> Học phần tự chọn
                    </div>
                    <div class="me-4 mb-2">
                      <span class="check-icon me-1">✓</span> <strong>HT ĐA:</strong> Học trước đồ án
                    </div>
                    <div class="mb-2">
                      <span class="check-icon me-1">✓</span> <strong>TQ ĐA:</strong> Tiên quyết đồ án
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- No Results Message -->
              <div v-else-if="hasSearched && !isLoading" class="text-center py-4">
                <div class="alert alert-info">
                  <i class="fas fa-info-circle me-2"></i>
                  Không tìm thấy dữ liệu chương trình đào tạo
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
import CTDTController from '@/controllers/CTDTController'

export default {
  name: 'CTDT',
  data() {
    return {
      facultyName: '',
      majors: [],
      majorCourses: [],
      courseDetails: [],
      selectedMajorId: '',
      selectedMajorCourseId: '',
      isLoading: false,
      hasSearched: false,
      showAlert: false,
      alertMessage: '',
      alertClass: 'alert-info'
    }
  },
  computed: {
    /**
     * Group course details by semester for better visualization
     */
    groupedBySemester() {
      const groupedData = {};
      
      this.courseDetails.forEach(detail => {
        const semester = detail.semester.toString();
        if (!groupedData[semester]) {
          groupedData[semester] = [];
        }
        groupedData[semester].push(detail);
      });
      
      // Sort by semester number
      return Object.keys(groupedData)
        .sort((a, b) => parseInt(a) - parseInt(b))
        .reduce((acc, key) => {
          acc[key] = groupedData[key];
          return acc;
        }, {});
    }
  },
  async created() {
    await this.loadFacultyInfo()
    await this.loadMajors()
    
    // Set document title with faculty name for better SEO
    if (this.facultyName) {
      document.title = `Chương Trình Đào Tạo - ${this.facultyName} - Đại học Bách Khoa`;
    } else {
      document.title = 'Chương Trình Đào Tạo - Đại học Bách Khoa';
    }
  },
  methods: {
    /**
     * Calculate the overall index for courses across semesters
     */
    getOverallIndex(semester, index) {
      let count = 0;
      
      // Count all courses in previous semesters
      Object.keys(this.groupedBySemester)
        .sort((a, b) => parseInt(a) - parseInt(b))
        .forEach(sem => {
          if (parseInt(sem) < parseInt(semester)) {
            count += this.groupedBySemester[sem].length;
          }
        });
      
      return count + index + 1;
    },
    
    /**
     * Load faculty information from API
     */
    async loadFacultyInfo() {
      try {
        const facultyId = this.$route.params.id
        if (!facultyId) {
          return
        }
        
        const faculty = await CTDTController.getFacultyById(facultyId)
        if (faculty && faculty.name) {
          this.facultyName = faculty.name
        }
      } catch (error) {
        console.error('Lỗi khi tải thông tin khoa:', error)
      }
    },
    
    /**
     * Load majors list from API
     */
    async loadMajors() {
      try {
        this.isLoading = true
        this.showAlert = false
        
        const facultyId = this.$route.params.id
        if (!facultyId) {
          this.showAlertMessage('Không tìm thấy thông tin khoa', 'alert-danger')
          return
        }
        
        const majors = await CTDTController.getMajorsByFaculty(facultyId)
        this.majors = majors
        
        if (majors.length === 0) {
          this.showAlertMessage('Không tìm thấy ngành nào thuộc khoa này', 'alert-warning')
        }
      } catch (error) {
        console.error('Lỗi khi tải danh sách ngành:', error)
        this.showAlertMessage('Đã xảy ra lỗi khi tải danh sách ngành', 'alert-danger')
      } finally {
        this.isLoading = false
      }
    },
    
    /**
     * Handle major selection change
     */
    async onMajorChange() {
      this.majorCourses = []
      this.selectedMajorCourseId = ''
      this.courseDetails = []
      this.hasSearched = false
      
      if (!this.selectedMajorId) return
      
      try {
        this.isLoading = true
        this.showAlert = false
        
        const majorCourses = await CTDTController.getMajorCoursesByMajorId(this.selectedMajorId)
        this.majorCourses = majorCourses
        
        if (majorCourses.length === 0) {
          this.showAlertMessage('Không tìm thấy chương trình đào tạo nào cho ngành này', 'alert-warning')
        }
      } catch (error) {
        console.error('Lỗi khi tải danh sách chương trình đào tạo:', error)
        this.showAlertMessage('Đã xảy ra lỗi khi tải danh sách chương trình đào tạo', 'alert-danger')
      } finally {
        this.isLoading = false
      }
    },
    
    /**
     * Search for course details
     */
    async searchCourseDetails() {
      if (!this.selectedMajorCourseId) return
      
      try {
        this.isLoading = true
        this.showAlert = false
        this.hasSearched = true
        
        this.courseDetails = await CTDTController.getMajorCourseDetailsByMajorCourseId(this.selectedMajorCourseId)
        
        if (this.courseDetails.length === 0) {
          this.showAlertMessage('Không tìm thấy chi tiết chương trình đào tạo', 'alert-warning')
        }
      } catch (error) {
        console.error('Lỗi khi tải chi tiết chương trình đào tạo:', error)
        this.showAlertMessage('Đã xảy ra lỗi khi tải chi tiết chương trình đào tạo', 'alert-danger')
      } finally {
        this.isLoading = false
      }
    },
    
    /**
     * Show alert message
     */
    showAlertMessage(message, type = 'alert-info') {
      this.alertMessage = message
      this.alertClass = type
      this.showAlert = true
    }
  }
}
</script>

<style scoped>
.ctdt-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* Breadcrumb styling */
.breadcrumb {
  background-color: transparent;
  padding: 0.5rem 0;
}

.breadcrumb-item a {
  color: #0a4275;
  font-weight: 500;
}

.breadcrumb-item.active {
  color: #495057;
  font-weight: 600;
}

.ctdt-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1) !important;
}

.ctdt-header {
  background-color: #0a4275;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-control, .form-select {
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.form-control:focus, .form-select:focus {
  border-color: #4285f4;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background-color: #0a4275;
  border-color: #0a4275;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  font-weight: 500;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: #073561;
  border-color: #073561;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.course-table-container {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  background-color: #ffffff;
  padding: 0.5rem;
}

/* Table styling with semester grouping */
.custom-table {
  margin-bottom: 0;
  border: none;
}

.table-header {
  background-color: #0a4275;
  color: white;
  font-weight: 600;
}

.table-header th {
  padding: 0.75rem 0.5rem;
  vertical-align: middle;
  border: 1px solid #1a5288;
  font-size: 0.9rem;
}

.semester-header td {
  background-color: #e9ecef !important;
  font-weight: 600 !important;
  color: #495057;
  border: 1px solid #dee2e6 !important;
  padding: 0.75rem 1rem !important;
  border-bottom: 2px solid #0a4275 !important;
}

.row-even {
  background-color: rgba(232, 240, 254, 0.2);
}

.custom-table td {
  padding: 0.625rem 0.5rem;
  vertical-align: middle;
  border: 1px solid #dee2e6;
  font-size: 0.9rem;
}

.course-name {
  font-weight: 500;
  color: #0a4275;
}

.relationship-cell {
  font-size: 0.85rem;
  line-height: 1.4;
}

.relationship-cell div {
  margin-bottom: 0.25rem;
}

.relationship-cell div:last-child {
  margin-bottom: 0;
}

.check-icon {
  display: inline-block;
  font-size: 1.1rem;
  font-weight: bold;
  color: #28a745;
}

.legend {
  font-size: 0.9rem;
  color: #495057;
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 0.625rem 0.75rem;
  border-left: 3px solid #0a4275;
}

/* Custom scrollbar */
.custom-scrollbar {
  overflow-x: auto;
}

.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #0a4275;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #073561;
}

.alert {
  border-radius: 6px;
  padding: 0.75rem;
}

/* Prevent copying table content */
.no-copy {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}
</style>