<template>
  <div class="modal fade" id="majorQuickViewModal" tabindex="-1" aria-labelledby="majorModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-md">
      <div class="modal-content">
        <header class="modal-header bg-primary text-white py-2">
          <h2 class="modal-title fs-5" id="majorModalLabel">
            <i class="bi bi-mortarboard-fill me-1" aria-hidden="true"></i>
            {{ major ? major.name : 'Thông tin ngành' }}
          </h2>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Đóng"></button>
        </header>
        <div class="modal-body p-0">
          <div v-if="loading" class="text-center p-3">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="mt-2 small">Đang tải thông tin chi tiết ngành...</p>
          </div>
          
          <main v-else-if="major" class="p-3">
            <section class="row g-3 mb-3">
              <div class="col-md-8">
                <h3 class="major-name mb-1">{{ major.name }}</h3>
                <div class="mb-2">
                  <span class="badge bg-secondary me-1">Mã: {{ major.major_code }}</span>
                  <span class="badge bg-info">{{ major.faculty_name }}</span>
                </div>
                <div class="major-description mt-2">
                  <h4 class="description-title">Mô tả ngành:</h4>
                  <p class="small mb-0">{{ major.description || 'Chưa có mô tả cho ngành này.' }}</p>
                </div>
              </div>
              <div class="col-md-4">
                <div class="row g-2">
                  <div class="col-6 col-md-12">
                    <div class="detail-card quota">
                      <div class="detail-card-title">
                        <i class="bi bi-people-fill me-1" aria-hidden="true"></i> Chỉ tiêu 2025
                      </div>
                      <div class="detail-card-value">{{ major.seats }}</div>
                    </div>
                  </div>
                  <div class="col-6 col-md-12">
                    <div class="detail-card methods">
                      <div class="detail-card-title">
                        <i class="bi bi-check2-square me-1" aria-hidden="true"></i> Phương thức
                      </div>
                      <div class="detail-card-value">{{ admissionMethods.length }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
            
            <div class="text-center mt-3">
              <!-- Thay thế router-link bằng button để xử lý đóng modal trước khi điều hướng -->
              <button 
                class="btn btn-primary btn-sm"
                @click="navigateToDetail(major.id)"
              >
                <i class="bi bi-info-circle-fill me-1" aria-hidden="true"></i> Xem thông tin chi tiết ngành
              </button>
            </div>
          </main>
          
          <div v-else-if="error" class="alert alert-danger m-3 py-2">
            <i class="bi bi-exclamation-triangle-fill me-1" aria-hidden="true"></i>
            {{ error }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onBeforeUnmount, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DetailMajorController from '@/controllers/DetailMajorController'

export default {
  name: 'MajorQuickView',
  props: {
    majorId: {
      type: [Number, String],
      default: null
    },
    show: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['modal-closed'],
  
  setup(props, { emit }) {
    const router = useRouter()
    const major = ref(null)
    const admissionMethods = ref([])
    const loading = ref(false)
    const error = ref(null)
    let modalInstance = null
    
    const loadMajorDetail = async (id) => {
      if (!id) return
      
      try {
        loading.value = true
        error.value = null
        
        // Lấy thông tin chi tiết về ngành
        major.value = await DetailMajorController.getMajorDetail(id)
        
        // Lấy các phương thức xét tuyển
        admissionMethods.value = await DetailMajorController.getMajorAdmissionMethods(id)
        
      } catch (err) {
        console.error('Lỗi khi tải thông tin chi tiết ngành:', err)
        error.value = 'Đã xảy ra lỗi khi tải thông tin chi tiết ngành.'
      } finally {
        loading.value = false
      }
    }
    
    const initModal = () => {
      const modalElement = document.getElementById('majorQuickViewModal')
      if (modalElement && window.bootstrap && window.bootstrap.Modal) {
        // Khởi tạo modal
        modalInstance = new bootstrap.Modal(modalElement)
        
        // Thêm sự kiện để xử lý khi modal đóng
        modalElement.addEventListener('hidden.bs.modal', handleModalHidden)
      }
    }
    
    const closeModal = () => {
      if (modalInstance) {
        modalInstance.hide()
        
        // Đảm bảo modal backdrop cũng được xóa
        const backdrop = document.querySelector('.modal-backdrop')
        if (backdrop) {
          backdrop.remove()
        }
        
        // Reset class trên body
        document.body.classList.remove('modal-open')
        document.body.style.overflow = ''
        document.body.style.paddingRight = ''
      }
    }
    
    // Điều hướng đến trang chi tiết sau khi đóng modal
    const navigateToDetail = (id) => {
      closeModal() // Đóng modal trước
      
      // Sử dụng setTimeout để đảm bảo modal đã đóng hoàn toàn trước khi chuyển trang
      setTimeout(() => {
        router.push({ name: 'MajorDetail', params: { id } })
        emit('modal-closed') // Thông báo cho parent component
      }, 50)
    }
    
    const handleModalHidden = () => {
      // Emit event thông báo modal đã đóng
      emit('modal-closed')
      
      // Reset data
      major.value = null
      admissionMethods.value = []
    }
    
    // Watch for changes in props.majorId
    watch(() => props.majorId, (newId) => {
      if (newId) {
        loadMajorDetail(newId)
      }
    })
    
    // Watch for changes in props.show
    watch(() => props.show, (newValue) => {
      if (newValue && props.majorId) {
        // Đảm bảo modal đã được khởi tạo
        if (!modalInstance) {
          initModal()
        }
        
        if (modalInstance) {
          modalInstance.show()
        }
      } else if (!newValue && modalInstance) {
        closeModal()
      }
    })
    
    // Khởi tạo modal khi component được mount
    onMounted(() => {
      initModal()
    })
    
    // Cleanup khi component bị hủy
    onBeforeUnmount(() => {
      const modalElement = document.getElementById('majorQuickViewModal')
      if (modalElement) {
        modalElement.removeEventListener('hidden.bs.modal', handleModalHidden)
      }
      
      // Đóng modal và xóa instance
      if (modalInstance) {
        closeModal()
        modalInstance = null
      }
    })
    
    return {
      major,
      admissionMethods,
      loading,
      error,
      navigateToDetail
    }
  }
}
</script>

<style scoped>
.major-name {
  color: #0d47a1;
  font-weight: 700;
  font-size: 1.1rem;
}

.detail-card {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  padding: 0.75rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  height: 100%;
}

.detail-card-title {
  color: #495057;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

.detail-card-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0d47a1;
}

.detail-card.quota .detail-card-value {
  color: #28a745;
}

.major-description {
  color: #495057;
}

.description-title {
  color: #0d47a1;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

@media (max-width: 768px) {
  .detail-card {
    padding: 0.5rem;
  }
  
  .detail-card-value {
    font-size: 1.25rem;
  }
  
  .major-name {
    font-size: 1rem;
  }
  
  .description-title {
    font-size: 0.8rem;
  }
}
</style>