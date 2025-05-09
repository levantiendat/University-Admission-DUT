<template>
  <div class="ctdt-container">
    <section class="hero-section">
      <div class="content">
        <h1 class="title">Chương Trình Đào Tạo</h1>
        <p class="subtitle">Trường Đại học Bách Khoa - Đại Học Đà Nẵng</p>
      </div>
    </section>

    <section class="faculties-section">
      <div class="container">
        <h2 class="section-title">Danh Sách Khoa</h2>
        
        <div class="row g-4">
          <div v-if="loading" class="col-12 text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Đang tải...</span>
            </div>
          </div>
          
          <div v-else-if="error" class="col-12 text-center py-4">
            <div class="alert alert-danger" role="alert">
              {{ error }}
            </div>
          </div>
          
          <div v-else-if="faculties.length === 0" class="col-12 text-center py-4">
            <p>Không có khoa nào được tìm thấy.</p>
          </div>
          
          <div v-else class="col-md-6 col-lg-4 mb-4" v-for="faculty in faculties" :key="faculty.id">
            <router-link :to="'/ctdt/' + faculty.id" class="faculty-card">
              <div class="card-icon">
                <i class="bi bi-mortarboard-fill"></i>
              </div>
              <div class="card-body">
                <h3 class="faculty-name">{{ faculty.name }}</h3>
                <div class="faculty-code">Mã khoa: {{ faculty.faculty_code }}</div>
                <p class="faculty-description">{{ faculty.description || 'Khám phá chương trình đào tạo tiên tiến và đội ngũ giảng viên chất lượng cao.' }}</p>
                <div class="explore-link">
                  <span>Xem chương trình</span>
                  <i class="bi bi-arrow-right"></i>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import CTDTAllController from '@/controllers/CTDTAllController'

export default {
  name: 'CTDTAll',
  setup() {
    const faculties = ref([])
    const loading = ref(true)
    const error = ref(null)

    const loadFaculties = async () => {
      loading.value = true
      error.value = null
      
      try {
        faculties.value = await CTDTAllController.getFaculties()
      } catch (err) {
        console.error('Error loading faculties:', err)
        error.value = 'Không thể tải danh sách khoa. Vui lòng thử lại sau.'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadFaculties()
      // Set page title for SEO
      document.title = 'Chương Trình Đào Tạo - Đại học Bách Khoa Đà Nẵng'
    })

    return {
      faculties,
      loading,
      error
    }
  }
}
</script>

<style scoped>
.ctdt-container {
  background-color: #f8f9fa;
}

.hero-section {
  background: linear-gradient(135deg, #0B2942 0%, #1a73e8 100%);
  color: white;
  padding: 3rem 1rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  border-radius: 0 0 30px 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: 300px;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.05;
  z-index: 0;
}

.hero-section .content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.title {
  font-size: 2.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

.faculties-section {
  padding: 3rem 1rem;
}

.section-title {
  text-align: center;
  color: #0B2942;
  margin-bottom: 2.5rem;
  font-weight: 600;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background-color: #4da0ff;
}

.faculty-card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
  text-decoration: none;
  color: #333;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
}

.faculty-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: #4da0ff;
}

.card-icon {
  background: linear-gradient(135deg, #0B2942 0%, #1a73e8 100%);
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  position: absolute;
  top: -20px;
  right: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card-body {
  padding: 1.5rem;
  padding-top: 2rem;
}

.faculty-name {
  color: #0B2942;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.faculty-code {
  color: #4da0ff;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 0.75rem;
  display: inline-block;
  background-color: rgba(77, 160, 255, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.faculty-description {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  height: 4.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.explore-link {
  display: flex;
  align-items: center;
  color: #4da0ff;
  font-weight: 500;
  margin-top: auto;
  font-size: 0.95rem;
}

.explore-link i {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.faculty-card:hover .explore-link i {
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .title {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .faculties-section {
    padding: 2rem 0.5rem;
  }
  
  .card-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
    top: -15px;
    right: 15px;
  }
}
</style>