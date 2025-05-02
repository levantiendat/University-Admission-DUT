<template>
    <div class="admin-major-course-details">
      <div class="admin-page-header">
        <div class="d-flex align-items-center mb-3">
          <router-link :to="`/admins/major-courses`" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết khung chương trình đào tạo</h2>
            <p class="admin-page-description" v-if="majorCourse">
              {{ majorCourse.type }} ngành {{ getMajorName(majorCourse.major_id) }} ({{ majorCourse.year }})
            </p>
          </div>
        </div>
        
        <div class="d-flex justify-content-between align-items-center">
          <div class="filters">
            <div class="semester-filter">
              <label for="semester-filter">Học kỳ:</label>
              <select id="semester-filter" v-model="filters.semester" class="form-select form-select-sm" @change="applyFilters">
                <option value="">Tất cả học kỳ</option>
                <option v-for="sem in availableSemesters" :key="sem" :value="sem">
                  Học kỳ {{ sem }}
                </option>
              </select>
            </div>
            
            <div class="type-filter">
              <label for="type-filter">Loại học phần:</label>
              <select id="type-filter" v-model="filters.type" class="form-select form-select-sm" @change="applyFilters">
                <option value="">Tất cả loại</option>
                <option value="mandatory">Bắt buộc</option>
                <option value="elective">Tự chọn</option>
                <option value="pre_capstone">Tiền đồ án</option>
                <option value="mandatory_capstone">Đồ án tốt nghiệp</option>
              </select>
            </div>
            
            <div class="search-box">
              <i class="bi bi-search search-icon"></i>
              <input 
                type="text" 
                v-model="searchQuery" 
                class="search-input" 
                placeholder="Tìm kiếm học phần..."
                @input="applyFilters"
              >
            </div>
          </div>
          
          <router-link :to="`/admins/major-courses/${majorCourseId}/details/create`" class="btn-create">
            <i class="bi bi-plus-circle me-2"></i>Thêm học phần
          </router-link>
        </div>
      </div>
  
      <!-- Loading Indicator -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải chi tiết khung chương trình...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
      
      <!-- Success message -->
      <div v-if="successMessage" class="success-message">
        <i class="bi bi-check-circle-fill me-2"></i>
        {{ successMessage }}
        <button class="close-button" @click="successMessage = ''">×</button>
      </div>
  
      <div v-if="!loading && !error" class="semester-tabs">
        <div class="semester-selector">
          <button 
            v-for="sem in availableSemesters" 
            :key="sem"
            class="semester-tab" 
            :class="{ 'active': selectedSemester === sem }"
            @click="selectedSemester = sem"
          >
            Học kỳ {{ sem }}
          </button>
        </div>
  
        <div class="tab-content">
          <div v-for="sem in availableSemesters" :key="`content-${sem}`" v-show="selectedSemester === sem" class="semester-content">
            <div class="course-count">
              <span>{{ getCoursesForSemester(sem).length }} học phần</span>
              <span class="total-credits">
                {{ calculateTotalCreditsForSemester(sem) }} tín chỉ
              </span>
            </div>
            
            <div class="course-cards">
              <div 
                v-for="detail in getCoursesForSemester(sem)" 
                :key="detail.id"
                class="course-card"
                :class="{
                  'elective': detail.elective_course,
                  'pre-capstone': detail.pre_capstone,
                  'capstone': detail.mandatory_capstone
                }"
              >
                <div class="course-header">
                  <h5 class="course-name">{{ getCourseNameById(detail.course_id) }}</h5>
                  <span class="course-code">{{ getCourseCodeById(detail.course_id) }}</span>
                </div>
                
                <div class="course-info">
                  <div class="course-credits">
                    <i class="bi bi-award"></i>
                    {{ getCreditsById(detail.course_id) }} tín chỉ
                  </div>
                  
                  <div class="course-type">
                    <span v-if="detail.elective_course" class="badge bg-info">Tự chọn</span>
                    <span v-else class="badge bg-primary">Bắt buộc</span>
                    <span v-if="detail.pre_capstone" class="badge bg-warning ms-1">Tiền đồ án</span>
                    <span v-if="detail.mandatory_capstone" class="badge bg-danger ms-1">Đồ án TN</span>
                  </div>
                </div>
                
                <div class="course-relations">
                  <div v-if="detail.prior_courses && detail.prior_courses.length > 0" class="relation-group">
                    <div class="relation-title">
                      <i class="bi bi-arrow-left-circle"></i>
                      Học trước:
                    </div>
                    <div class="relation-list">
                      <span 
                        v-for="priorId in detail.prior_courses" 
                        :key="`prior-${priorId}`" 
                        class="relation-item"
                        :title="getCourseNameByDetailId(priorId)"
                      >
                        {{ getCourseCodeByDetailId(priorId) }}
                      </span>
                    </div>
                  </div>
                  
                  <div v-if="detail.prerequisites && detail.prerequisites.length > 0" class="relation-group">
                    <div class="relation-title">
                      <i class="bi bi-diagram-3"></i>
                      Tiên quyết:
                    </div>
                    <div class="relation-list">
                      <span 
                        v-for="prereqId in detail.prerequisites" 
                        :key="`prereq-${prereqId}`" 
                        class="relation-item"
                        :title="getCourseNameByDetailId(prereqId)"
                      >
                        {{ getCourseCodeByDetailId(prereqId) }}
                      </span>
                    </div>
                  </div>
                  
                  <div v-if="detail.corequisites && detail.corequisites.length > 0" class="relation-group">
                    <div class="relation-title">
                      <i class="bi bi-grid"></i>
                      Song hành:
                    </div>
                    <div class="relation-list">
                      <span 
                        v-for="coreqId in detail.corequisites" 
                        :key="`coreq-${coreqId}`" 
                        class="relation-item"
                        :title="getCourseNameByDetailId(coreqId)"
                      >
                        {{ getCourseCodeByDetailId(coreqId) }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div class="course-actions">
                  <router-link 
                    :to="`/admins/major-courses/${majorCourseId}/details/${detail.id}/edit`" 
                    class="btn-edit"
                    title="Chỉnh sửa học phần"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </router-link>
                  
                  <button 
                    class="btn-delete"
                    @click="confirmDelete(detail)"
                    title="Xóa học phần khỏi chương trình"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
              
              <!-- Empty State for Semester -->
              <div v-if="getCoursesForSemester(sem).length === 0" class="empty-semester">
                <i class="bi bi-journal-x empty-icon"></i>
                <p>Chưa có học phần nào trong học kỳ {{ sem }}</p>
                <router-link :to="`/admins/major-courses/${majorCourseId}/details/create`" class="btn-add-course">
                  <i class="bi bi-plus-circle me-2"></i>Thêm học phần
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa học phần</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa học phần <strong>{{ getCourseNameById(detailToDelete?.course_id) }}</strong> ({{ getCourseCodeById(detailToDelete?.course_id) }}) khỏi khung chương trình?</p>
            <p>Học kỳ: {{ detailToDelete?.semester }}</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Việc này sẽ xóa tất cả các mối quan hệ có liên quan (học trước, tiên quyết, song hành). Hành động này không thể khôi phục.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteMajorCourseDetail" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import MajorCourseDetailController from '@/controllers/admins/MajorCourseDetailController'
  import MajorCourseController from '@/controllers/admins/MajorCourseController'
  import MajorController from '@/controllers/admins/MajorController'
  
  export default {
    name: 'AdminMajorCourseDetails',
    props: {
      majorCourseId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const route = useRoute()
      const majorCourseDetails = ref([])
      const courses = ref([])
      const majorCourse = ref(null)
      const majors = ref([])
      const loading = ref(true)
      const error = ref(null)
      const successMessage = ref('')
      const searchQuery = ref('')
      const selectedSemester = ref(1) // Default to first semester
  
      // Filters
      const filters = reactive({
        semester: '',
        type: ''
      })
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const detailToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Computed property to get unique available semesters
      const availableSemesters = computed(() => {
        if (!majorCourseDetails.value) return []
        
        const semesters = majorCourseDetails.value.map(detail => detail.semester)
        return [...new Set(semesters)].sort((a, b) => a - b)
      })
      
      // Helper methods to get course information
      const getCourseNameById = (courseId) => {
        const course = courses.value.find(c => c.id === courseId)
        return course ? course.name : 'Không xác định'
      }
      
      const getCourseCodeById = (courseId) => {
        const course = courses.value.find(c => c.id === courseId)
        return course ? course.course_code : 'N/A'
      }
      
      const getCreditsById = (courseId) => {
        const course = courses.value.find(c => c.id === courseId)
        return course ? course.credits : 'N/A'
      }
      
      const getCourseNameByDetailId = (detailId) => {
        const detail = majorCourseDetails.value.find(d => d.id === detailId)
        if (!detail) return 'Không xác định'
        return getCourseNameById(detail.course_id)
      }
      
      const getCourseCodeByDetailId = (detailId) => {
        const detail = majorCourseDetails.value.find(d => d.id === detailId)
        if (!detail) return 'N/A'
        return getCourseCodeById(detail.course_id)
      }
      
      const getMajorName = (majorId) => {
        const major = majors.value.find(m => m.id === majorId)
        return major ? major.name : 'Không xác định'
      }
      
      // Filter courses by semester
      const getCoursesForSemester = (semester) => {
        return majorCourseDetails.value.filter(detail => detail.semester === semester)
      }
      
      // Calculate total credits for a semester
      const calculateTotalCreditsForSemester = (semester) => {
        let total = 0
        const semesterCourses = getCoursesForSemester(semester)
        
        semesterCourses.forEach(detail => {
          const course = courses.value.find(c => c.id === detail.course_id)
          if (course) {
            total += course.credits
          }
        })
        
        return total
      }
      
      // Apply filters
      const applyFilters = () => {
        // Implementation of filters here
        // This will be implemented when needed, as we're using tabs for now
      }
  
      // Fetch data
      const fetchData = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load major course details by major course id
          const response = await MajorCourseDetailController.getMajorCourseDetailsByMajorCourseId(props.majorCourseId)
          
          // Load major course info
          const majorCourseData = await MajorCourseController.getMajorCourseById(props.majorCourseId)
          
          // Load majors for displaying names
          const majorsData = await MajorController.getAllMajors()
          
          // Set data
          courses.value = response.courses || []
          majorCourseDetails.value = response.major_course_details || []
          majorCourse.value = majorCourseData
          majors.value = majorsData
          
          // Set initial selected semester
          if (availableSemesters.value.length > 0) {
            selectedSemester.value = availableSemesters.value[0]
          }
          
          // Check if there's a success message from navigation
          if (route.query.success) {
            successMessage.value = route.query.success
            
            // Clear the success message after 5 seconds
            setTimeout(() => {
              successMessage.value = ''
            }, 5000)
          }
        } catch (err) {
          error.value = `Không thể tải chi tiết khung chương trình: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      // Confirm delete
      const confirmDelete = (detail) => {
        detailToDelete.value = detail
        showDeleteModal.value = true
      }
  
      // Cancel delete
      const cancelDelete = () => {
        showDeleteModal.value = false
        detailToDelete.value = null
      }
  
      // Delete major course detail
      const deleteMajorCourseDetail = async () => {
        if (!detailToDelete.value) return
        
        try {
          isDeleting.value = true
          await MajorCourseDetailController.deleteMajorCourseDetail(detailToDelete.value.id)
          
          // Remove from list
          majorCourseDetails.value = majorCourseDetails.value.filter(d => d.id !== detailToDelete.value.id)
          
          // Close modal and reset
          showDeleteModal.value = false
          detailToDelete.value = null
          
          successMessage.value = 'Xóa học phần khỏi khung chương trình thành công!'
          
          // Clear the success message after 5 seconds
          setTimeout(() => {
            successMessage.value = ''
          }, 5000)
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      onMounted(() => {
        fetchData()
      })
  
      return {
        majorCourseDetails,
        courses,
        majorCourse,
        majors,
        loading,
        error,
        successMessage,
        searchQuery,
        filters,
        availableSemesters,
        selectedSemester,
        showDeleteModal,
        detailToDelete,
        isDeleting,
        getCourseNameById,
        getCourseCodeById,
        getCreditsById,
        getCourseNameByDetailId,
        getCourseCodeByDetailId,
        getMajorName,
        getCoursesForSemester,
        calculateTotalCreditsForSemester,
        applyFilters,
        confirmDelete,
        cancelDelete,
        deleteMajorCourseDetail
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-major-course-details {
    width: 100%;
  }
  
  .admin-page-header {
    margin-bottom: 2rem;
  }
  
  .admin-page-title {
    font-size: 1.75rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .admin-page-description {
    color: #6c757d;
    font-size: 0.95rem;
  }
  
  .btn-back {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #f8f9fa;
    color: #0B2942;
    text-decoration: none;
    margin-right: 1rem;
    transition: all 0.2s ease;
  }
  
  .btn-back:hover {
    background-color: #e9ecef;
    transform: translateX(-2px);
  }
  
  .filters {
    display: flex;
    gap: 1rem;
    align-items: center;
  }
  
  .semester-filter,
  .type-filter {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .semester-filter label,
  .type-filter label {
    font-weight: 500;
    color: #0B2942;
    margin-bottom: 0;
    white-space: nowrap;
  }
  
  .form-select-sm {
    padding: 0.25rem 2rem 0.25rem 0.5rem;
    font-size: 0.875rem;
    min-width: 100px;
  }
  
  .search-box {
    position: relative;
    min-width: 200px;
  }
  
  .search-icon {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #95a5a6;
  }
  
  .search-input {
    padding: 0.375rem 0.75rem 0.375rem 30px;
    font-size: 0.875rem;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    width: 100%;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .btn-create {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s;
  }
  
  .btn-create:hover {
    background-color: #4da0ff;
    color: #fff;
    transform: translateY(-2px);
  }
  
  /* Success Message */
  .success-message {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    position: relative;
  }
  
  .close-button {
    position: absolute;
    right: 10px;
    top: 10px;
    background: none;
    border: none;
    color: #155724;
    font-size: 1.2rem;
    cursor: pointer;
  }
  
  /* Loading Animation */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 0;
  }
  
  .spinner {
    margin: 0 auto;
    width: 70px;
    text-align: center;
  }
  
  .spinner > div {
    width: 18px;
    height: 18px;
    background-color: #0B2942;
    border-radius: 100%;
    display: inline-block;
    animation: sk-bouncedelay 1.4s infinite ease-in-out both;
    margin: 0 3px;
  }
  
  .spinner .bounce1 {
    animation-delay: -0.32s;
  }
  
  .spinner .bounce2 {
    animation-delay: -0.16s;
  }
  
  @keyframes sk-bouncedelay {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1.0); }
  }
  
  .loading-text {
    margin-top: 1rem;
    color: #6c757d;
    font-size: 1rem;
  }
  
  /* Error Message */
  .error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .error-icon {
    font-size: 1.25rem;
    margin-right: 0.75rem;
  }
  
  /* Semester Tabs */
  .semester-tabs {
    margin-top: 2rem;
  }
  
  .semester-selector {
    display: flex;
    overflow-x: auto;
    border-bottom: 1px solid #dee2e6;
    margin-bottom: 1rem;
  }
  
  .semester-tab {
    padding: 0.75rem 1.5rem;
    background-color: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    font-weight: 500;
    color: #6c757d;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
  }
  
  .semester-tab:hover {
    color: #0B2942;
  }
  
  .semester-tab.active {
    color: #0B2942;
    border-bottom-color: #0B2942;
  }
  
  .semester-content {
    padding: 1rem 0;
  }
  
  .course-count {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding: 0.5rem 1rem;
    background-color: #f8f9fa;
    border-radius: 6px;
  }
  
  .total-credits {
    font-weight: 600;
    color: #0B2942;
  }
  
  /* Course Cards */
  .course-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }
  
  .course-card {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 1.25rem;
    position: relative;
    border-top: 4px solid #0B2942;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .course-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  }
  
  .course-card.elective {
    border-top-color: #17a2b8;
  }
  
  .course-card.pre-capstone {
    border-top-color: #ffc107;
  }
  
  .course-card.capstone {
    border-top-color: #dc3545;
  }
  
  .course-header {
    margin-bottom: 1rem;
  }
  
  .course-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.25rem;
  }
  
  .course-code {
    font-family: monospace;
    color: #6c757d;
    font-size: 0.9rem;
    padding: 0.2rem 0.5rem;
    background-color: #f8f9fa;
    border-radius: 4px;
  }
  
  .course-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .course-credits {
    font-weight: 500;
    color: #0B2942;
  }
  
  .course-credits i {
    color: #ffc107;
    margin-right: 0.25rem;
  }
  
  .course-type {
    display: flex;
    gap: 0.25rem;
  }
  
  .badge {
    font-weight: 500;
    font-size: 0.75rem;
    padding: 0.35rem 0.65rem;
  }
  
  /* Course Relations */
  .course-relations {
    margin-bottom: 1rem;
  }
  
  .relation-group {
    margin-bottom: 0.75rem;
  }
  
  .relation-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #6c757d;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  
  .relation-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .relation-item {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    font-size: 0.8rem;
    font-family: monospace;
    color: #0B2942;
    cursor: help;
  }
  
  /* Course Actions */
  .course-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  
  .btn-edit, .btn-delete {
    width: 35px;
    height: 35px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-edit {
    background-color: #f8f9fa;
    color: #0B2942;
  }
  
  .btn-edit:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .btn-delete {
    background-color: #f8f9fa;
    color: #dc3545;
  }
  
  .btn-delete:hover {
    background-color: #f8d7da;
    color: #dc3545;
  }
  
  /* Empty State for Semester */
  .empty-semester {
    grid-column: 1 / -1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    background-color: #f8f9fa;
    border-radius: 10px;
    text-align: center;
  }
  
  .empty-icon {
    font-size: 3rem;
    color: #adb5bd;
    margin-bottom: 1rem;
  }
  
  .btn-add-course {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin-top: 1rem;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s;
  }
  
  .btn-add-course:hover {
    background-color: #4da0ff;
    color: #fff;
    transform: translateY(-2px);
  }
  
  /* Modal Styling */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
  }
  
  .modal-content {
    background-color: #fff;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    overflow: hidden;
  }
  
  .modal-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .modal-title {
    font-size: 1.25rem;
    color: #0B2942;
    margin: 0;
  }
  
  .btn-close {
    background: transparent;
    border: none;
    font-size: 1.5rem;
    line-height: 1;
    color: #6c757d;
    cursor: pointer;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  
  .btn-cancel {
    padding: 0.5rem 1rem;
    background-color: #f8f9fa;
    color: #6c757d;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .btn-delete {
    padding: 0.5rem 1rem;
    background-color: #dc3545;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-delete:hover:not(:disabled) {
    background-color: #c82333;
  }
  
  .btn-delete:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .text-danger {
    color: #dc3545;
  }
  
  @media (max-width: 768px) {
    .filters {
      flex-direction: column;
      align-items: stretch;
    }
    
    .semester-filter,
    .type-filter {
      margin-bottom: 0.5rem;
    }
    
    .admin-page-header {
      flex-direction: column;
      gap: 1rem;
    }
    
    .btn-create {
      width: 100%;
      justify-content: center;
    }
    
    .course-cards {
      grid-template-columns: 1fr;
    }
  }
  </style>