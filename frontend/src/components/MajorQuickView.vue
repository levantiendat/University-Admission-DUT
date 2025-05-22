<template>
  <Transition name="slide-fade">
    <div v-if="isVisible" class="major-info-widget" :class="{ 'widget-expanded': isExpanded }">
      <!-- Close and expand buttons -->
      <div class="widget-controls">
        <button @click="toggleExpand" class="control-btn expand-btn" :title="isExpanded ? 'Thu gọn' : 'Mở rộng'">
          <i class="bi" :class="isExpanded ? 'bi-arrows-angle-contract' : 'bi-arrows-angle-expand'"></i>
        </button>
        <button @click="close" class="control-btn close-btn" title="Đóng">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      
      <!-- Header -->
      <header class="widget-header">
        <div class="d-flex align-items-center">
          <div class="widget-icon">
            <i class="bi bi-mortarboard-fill"></i>
          </div>
          <h2 class="widget-title">{{ major?.name || 'Thông tin ngành' }}</h2>
        </div>
        <div class="widget-badges">
          <span class="badge bg-primary me-1">{{ major?.major_code }}</span>
          <span class="badge bg-info">{{ major?.faculty_name }}</span>
        </div>
      </header>
      
      <!-- Loading State -->
      <div v-if="loading" class="widget-loading">
        <div class="spinner-border text-primary spinner-border-sm"></div>
        <p>Đang tải thông tin...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="widget-error">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        <span>{{ error }}</span>
      </div>
      
      <!-- Content -->
      <div v-else-if="major" class="widget-content">
        <!-- Stats Summary Section -->
        <div class="widget-stats">
          <div class="stat-item quota">
            <div class="stat-icon"><i class="bi bi-people-fill"></i></div>
            <div class="stat-content">
              <div class="stat-value">{{ major.seats }}</div>
              <div class="stat-label">Chỉ tiêu 2025</div>
            </div>
          </div>
          <div class="stat-item methods">
            <div class="stat-icon"><i class="bi bi-check2-square"></i></div>
            <div class="stat-content">
              <div class="stat-value">{{ admissionMethods.length }}</div>
              <div class="stat-label">Phương thức xét tuyển</div>
            </div>
          </div>
          <div class="stat-item groups" v-if="subjectGroups && subjectGroups.length">
            <div class="stat-icon"><i class="bi bi-grid-3x3-gap"></i></div>
            <div class="stat-content">
              <div class="stat-value">{{ countAllSubjectGroups }}</div>
              <div class="stat-label">Tổ hợp xét tuyển</div>
            </div>
          </div>
        </div>
        
        <!-- Description Section -->
        <div class="widget-section">
          <h3 class="section-title"><i class="bi bi-info-circle me-2"></i>Mô tả ngành</h3>
          <p class="section-content">{{ major.description || 'Chưa có mô tả cho ngành này.' }}</p>
        </div>
        
        <!-- Admission Methods Section -->
        <div class="widget-section" v-if="admissionMethods.length">
          <h3 class="section-title"><i class="bi bi-list-check me-2"></i>Phương thức xét tuyển</h3>
          <div class="method-chips">
            <div v-for="method in admissionMethods" :key="method.admission_methods_id" class="method-chip">
              {{ method.name }}
            </div>
          </div>
        </div>
        
        <!-- Subject Groups Section (Only visible when expanded) -->
        <div class="widget-section" v-if="isExpanded && subjectGroups && subjectGroups.length">
          <h3 class="section-title"><i class="bi bi-grid-3x3-gap me-2"></i>Tổ hợp xét tuyển</h3>
          <div class="subject-groups">
            <div v-for="(groupInfo, idx) in subjectGroups" :key="idx" class="group-section">
              <h4 class="group-method">{{ groupInfo.method_name }}</h4>
              <div class="group-chips">
                <div v-for="group in groupInfo.groups" :key="group.id" class="group-chip">
                  {{ group.name }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Previous Scores Section (Only visible when expanded) -->
        <div class="widget-section" v-if="isExpanded && Object.keys(previousScores).length">
          <h3 class="section-title"><i class="bi bi-bar-chart-line me-2"></i>Điểm chuẩn các năm trước</h3>
          <div class="previous-scores">
            <div v-for="(scores, year) in previousScores" :key="year" class="score-section">
              <h4 class="score-year">Năm {{ year }}</h4>
              <div class="score-chips">
                <div v-for="(score, idx) in scores" :key="idx" class="score-chip">
                  <div class="score-method">{{ score.method_name }}</div>
                  <div class="score-value">{{ score.score }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="widget-actions">
          <button v-if="!isExpanded" @click="toggleExpand" class="btn btn-sm btn-outline-primary">
            <i class="bi bi-arrows-expand me-1"></i>Xem thêm thông tin
          </button>
          <router-link :to="{ name: 'MajorDetail', params: { id: major.id }}" class="btn btn-sm btn-primary">
            <i class="bi bi-info-circle-fill me-1"></i>Chi tiết ngành
          </router-link>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import DetailMajorController from '@/controllers/DetailMajorController'

export default {
  name: 'MajorInfoWidget',
  props: {
    majorId: {
      type: [Number, String],
      default: null
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['close'],
  
  setup(props, { emit }) {
    const major = ref(null)
    const admissionMethods = ref([])
    const subjectGroups = ref([])
    const previousScores = ref({})
    const loading = ref(false)
    const error = ref(null)
    const isVisible = ref(props.visible)
    const isExpanded = ref(false)
    
    // Computed properties
    const countAllSubjectGroups = computed(() => {
      if (!subjectGroups.value.length) return 0
      
      return subjectGroups.value.reduce((total, groupInfo) => {
        return total + (groupInfo.groups?.length || 0)
      }, 0)
    })
    
    // Load major details
    const loadMajorDetail = async (id) => {
      if (!id) return
      
      try {
        loading.value = true
        error.value = null
        
        // Get major details
        major.value = await DetailMajorController.getMajorDetail(id)
        
        // Get admission methods
        admissionMethods.value = await DetailMajorController.getMajorAdmissionMethods(id)
        
        // Load subject groups for THPT and Hoc Ba methods
        const thptMethod = admissionMethods.value.find(m => m.admission_methods_id === 6)
        const hocbaMethod = admissionMethods.value.find(m => m.admission_methods_id === 3)
        
        const groupPromises = []
        
        if (thptMethod) {
          groupPromises.push(
            DetailMajorController.getMajorSubjectGroups(id, 6)
              .then(groups => ({
                admission_method_id: 6,
                method_name: thptMethod.name,
                groups
              }))
              .catch(() => ({
                admission_method_id: 6,
                method_name: thptMethod.name,
                groups: []
              }))
          )
        }
        
        if (hocbaMethod) {
          groupPromises.push(
            DetailMajorController.getMajorSubjectGroups(id, 3)
              .then(groups => ({
                admission_method_id: 3,
                method_name: hocbaMethod.name,
                groups
              }))
              .catch(() => ({
                admission_method_id: 3,
                method_name: hocbaMethod.name,
                groups: []
              }))
          )
        }
        
        subjectGroups.value = await Promise.all(groupPromises)
        
        // Get previous scores
        previousScores.value = await DetailMajorController.getPreviousAdmissionScores(id)
        
      } catch (err) {
        console.error('Lỗi khi tải thông tin chi tiết ngành:', err)
        error.value = 'Đã xảy ra lỗi khi tải thông tin chi tiết ngành.'
      } finally {
        loading.value = false
      }
    }
    
    // Handle close
    const close = () => {
      isVisible.value = false
      setTimeout(() => {
        emit('close')
        resetWidget()
      }, 300) // Match with transition duration
    }
    
    // Toggle expanded state
    const toggleExpand = () => {
      isExpanded.value = !isExpanded.value
    }
    
    // Reset widget state
    const resetWidget = () => {
      major.value = null
      admissionMethods.value = []
      subjectGroups.value = []
      previousScores.value = {}
      error.value = null
      isExpanded.value = false
    }
    
    // Handle escape key to close widget
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isVisible.value) {
        close()
      }
    }
    
    // Watch for prop changes
    watch(() => props.majorId, (newId) => {
      if (newId && isVisible.value) {
        loadMajorDetail(newId)
      }
    })
    
    watch(() => props.visible, (newValue) => {
      isVisible.value = newValue
      if (newValue && props.majorId) {
        loadMajorDetail(props.majorId)
      }
    })
    
    // Lifecycle hooks
    onMounted(() => {
      document.addEventListener('keydown', handleKeyDown)
      if (props.visible && props.majorId) {
        loadMajorDetail(props.majorId)
      }
    })
    
    onBeforeUnmount(() => {
      document.removeEventListener('keydown', handleKeyDown)
    })
    
    return {
      major,
      admissionMethods,
      subjectGroups,
      previousScores,
      loading,
      error,
      isVisible,
      isExpanded,
      countAllSubjectGroups,
      close,
      toggleExpand
    }
  }
}
</script>

<style scoped>
/* Widget Container */
.major-info-widget {
  position: fixed;
  right: 20px;
  top: 80px;
  width: 350px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1040;
  display: flex;
  flex-direction: column;
  padding: 0;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.widget-expanded {
  width: 450px;
}

@media (max-width: 576px) {
  .major-info-widget {
    width: calc(100% - 30px);
    right: 15px;
    top: 70px;
    max-height: calc(100vh - 85px);
  }
  
  .widget-expanded {
    width: calc(100% - 30px);
  }
}

/* Widget Controls */
.widget-controls {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 5px;
  z-index: 10;
}

.control-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  background-color: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: background-color 0.2s;
}

.control-btn:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

.close-btn {
  font-size: 14px;
}

.expand-btn {
  font-size: 12px;
}

/* Widget Header */
.widget-header {
  background-color: #0d47a1;
  color: white;
  padding: 14px 16px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.widget-icon {
  font-size: 20px;
  margin-right: 10px;
}

.widget-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.2;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.widget-badges {
  margin-top: 6px;
  padding-left: 30px;
}

/* Loading & Error States */
.widget-loading, .widget-error {
  padding: 20px;
  text-align: center;
  color: #495057;
}

.widget-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.widget-error {
  background-color: #fff8f8;
  color: #dc3545;
}

/* Widget Content */
.widget-content {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Stats Cards */
.widget-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  margin-bottom: 6px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.stat-item {
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #e9ecef;
  text-align: center;
}

.stat-item:last-child {
  border-right: none;
}

.stat-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 6px;
  font-size: 14px;
}

.quota .stat-icon {
  color: #28a745;
  background-color: rgba(40, 167, 69, 0.1);
}

.methods .stat-icon {
  color: #0d47a1;
  background-color: rgba(13, 71, 161, 0.1);
}

.groups .stat-icon {
  color: #6f42c1;
  background-color: rgba(111, 66, 193, 0.1);
}

.stat-content {
  text-align: center;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.1;
}

.quota .stat-value {
  color: #28a745;
}

.methods .stat-value {
  color: #0d47a1;
}

.groups .stat-value {
  color: #6f42c1;
}

.stat-label {
  font-size: 0.65rem;
  color: #6c757d;
  margin-top: 2px;
}

/* Content Sections */
.widget-section {
  padding: 12px 16px;
  border-bottom: 1px solid #e9ecef;
}

.widget-section:last-of-type {
  border-bottom: none;
}

.section-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #0d47a1;
  margin: 0 0 8px 0;
}

.section-content {
  font-size: 0.8rem;
  color: #212529;
  line-height: 1.4;
  margin: 0;
}

/* Method Chips */
.method-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.method-chip {
  background-color: rgba(13, 71, 161, 0.1);
  color: #0d47a1;
  border-radius: 16px;
  padding: 4px 10px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Subject Groups */
.group-section {
  margin-bottom: 10px;
}

.group-section:last-child {
  margin-bottom: 0;
}

.group-method {
  font-size: 0.75rem;
  font-weight: 600;
  color: #495057;
  margin: 0 0 6px 0;
}

.group-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.group-chip {
  background-color: rgba(111, 66, 193, 0.1);
  color: #6f42c1;
  border-radius: 16px;
  padding: 3px 8px;
  font-size: 0.7rem;
}

/* Previous Scores */
.score-section {
  margin-bottom: 10px;
}

.score-section:last-child {
  margin-bottom: 0;
}

.score-year {
  font-size: 0.75rem;
  font-weight: 600;
  color: #495057;
  margin: 0 0 6px 0;
}

.score-chips {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.score-chip {
  background-color: #f8f9fa;
  padding: 6px;
  border-radius: 6px;
  border-left: 3px solid #28a745;
}

.score-method {
  font-size: 0.65rem;
  color: #495057;
}

.score-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: #28a745;
}

/* Action Buttons */
.widget-actions {
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: auto;
  border-top: 1px solid #e9ecef;
}

.widget-actions .btn {
  flex: 1;
  font-size: 0.75rem;
  padding: 6px 0;
}

/* Transitions */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>