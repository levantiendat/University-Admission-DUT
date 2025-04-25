<template>
  <div class="ctdt-container">
    <div class="container py-4">
      <div class="row">
        <div class="col-12">
          <div class="card shadow border-0 ctdt-card">
            <div class="card-header ctdt-header">
              <h2 class="text-center text-white mb-0">
                Chương Trình Đào Tạo
                <small v-if="facultyName" class="d-block mt-2 fs-5">{{ facultyName }}</small>
              </h2>
            </div>
            
            <div class="card-body">
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
              
              <div v-if="showAlert" class="alert mb-4" :class="alertClass" role="alert">
                {{ alertMessage }}
              </div>
              
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
                      <tr v-for="(detail, index) in courseDetails" :key="detail.id" :class="{'row-even': index % 2 === 0}">
                        <td class="text-center">{{ index + 1 }}</td>
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
                    </tbody>
                  </table>
                </div>
                
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
      alertClass: 'alert-info',
      currentDate: '2025-04-25 13:33:37',
      currentUser: 'levantiendatHiện'
    }
  },
  async created() {
    await this.loadFacultyInfo()
    await this.loadMajors()
  },
  methods: {
    /**
     * Tải thông tin khoa từ API
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
     * Tải danh sách ngành từ API
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
     * Xử lý khi chọn ngành thay đổi
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
     * Tìm kiếm chi tiết chương trình đào tạo
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
     * Hiển thị thông báo
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
  background-color: #f5f9ff;
  min-height: 100vh;
  padding-bottom: 2rem;
}

.ctdt-card {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.ctdt-header {
  background-color: #0a4275;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-control, .form-select {
  border-radius: 6px;
  padding: 0.6rem 1rem;
  border: 1px solid #e0e6ed;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.form-control:focus, .form-select:focus {
  border-color: #4285f4;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background-color: #0a4275;
  border-color: #0a4275;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: #073561;
  border-color: #073561;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.course-table-container {
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  background-color: #ffffff;
  padding: 0.5rem;
}

/* Custom table styles */
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
  padding: 1rem 0.75rem;
  vertical-align: middle;
  border: 1px solid #1a5288;
}

.row-even {
  background-color: rgba(232, 240, 254, 0.4);
}

.custom-table td {
  padding: 0.75rem;
  vertical-align: middle;
  border: 1px solid #dee2e6;
}

.course-name {
  font-weight: 500;
  color: #0a4275;
}

.relationship-cell {
  font-size: 0.9rem;
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
  font-size: 1.2rem;
  font-weight: bold;
  color: #28a745;
}

.legend {
  font-size: 0.9rem;
  color: #6c757d;
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 0.75rem 1rem;
  border-left: 4px solid #0a4275;
}

/* Custom scrollbar */
.custom-scrollbar {
  overflow-x: auto;
}

.custom-scrollbar::-webkit-scrollbar {
  height: 8px;
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
  border-radius: 8px;
  padding: 1rem;
}

/* Prevent copying table content */
.no-copy {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.no-copy::selection {
  background: transparent;
}

.no-copy::-moz-selection {
  background: transparent;
}

.no-copy td, .no-copy th {
  -webkit-touch-callout: none;
}
</style>