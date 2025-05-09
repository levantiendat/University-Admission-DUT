<template>
  <div class="home-container">
    <!-- Carousel section (preserved as requested) -->
    <section class="carousel-section">
      <div class="container-fluid p-0">
        <div class="carousel-container">
          <!-- Carousel slides -->
          <div class="carousel-slides">
            <div v-for="(image, index) in carouselImages" :key="index" 
                 :class="['carousel-slide', { active: currentSlide === index }]"
                 :style="{ 
                   transform: `translateX(${100 * (index - currentSlideWithTransition)}%)`,
                   zIndex: currentSlide === index ? 1 : 0
                 }">
              <img :src="image" :alt="`Poster ${index + 1}`" class="carousel-image">
            </div>
          </div>

          <!-- Navigation buttons -->
          <button class="carousel-nav carousel-prev" @click="prevSlide" aria-label="Previous slide">
            <i class="bi bi-chevron-left"></i>
          </button>
          <button class="carousel-nav carousel-next" @click="nextSlide" aria-label="Next slide">
            <i class="bi bi-chevron-right"></i>
          </button>

          <!-- Indicators -->
          <div class="carousel-indicators-container">
            <div class="carousel-indicators">
              <span 
                v-for="(image, index) in carouselImages" 
                :key="`indicator-${index}`"
                :class="['carousel-indicator', { active: currentSlide === index }]"
                @click="goToSlide(index)"
              ></span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- University mission statement section -->
    <section class="mission-section">
      <div class="container">
        <div class="mission-content">
          <h1 class="university-name">Đại học Đà Nẵng - Trường Đại học Bách Khoa</h1>
          <p class="mission-text">
            Trường Đại học Bách khoa - Đại học Đà Nẵng là trường đại học kỹ thuật công lập định hướng nghiên cứu, 
            hướng đến hệ sinh thái giáo dục nhân bản, đổi mới và sáng tạo; tạo cơ hội cho mọi người phát triển 
            giá trị bản thân, thể hiện trách nhiệm với cộng đồng và xã hội.
          </p>
          <div class="university-stats">
            <div class="stat-item">
              <div class="stat-number">39</div>
              <div class="stat-label">Ngành đào tạo</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">15,000+</div>
              <div class="stat-label">Sinh viên</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick access section -->
    <section class="quick-access-section">
      <div class="container">
        <h2 class="section-title">Truy cập nhanh</h2>
        <div class="quick-links">
          <router-link to="/major" class="quick-link-item admission">
            <div class="icon-wrapper">
              <i class="bi bi-mortarboard-fill"></i>
            </div>
            <span>Ngành đào tạo</span>
          </router-link>
          
          <router-link to="/admission" class="quick-link-item programs">
            <div class="icon-wrapper">
              <i class="bi bi-journal-check"></i>
            </div>
            <span>Thông tin tuyển sinh</span>
          </router-link>
          
          <router-link to="/school-priority" class="quick-link-item scholarship">
            <div class="icon-wrapper">
              <i class="bi bi-geo-alt-fill"></i>
            </div>
            <span>Khu vực ưu tiên</span>
          </router-link>
          
          <router-link to="/ctdt" class="quick-link-item curriculum">
            <div class="icon-wrapper">
              <i class="bi bi-book-fill"></i>
            </div>
            <span>Chương trình đào tạo</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Admission information section -->
    <section class="admission-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Tuyển sinh năm 2025</h2>
          <router-link to="/admission" class="view-all">Xem tất cả <i class="bi bi-arrow-right"></i></router-link>
        </div>
        
        <div class="row g-4">
          <div class="col-md-4">
            <router-link to="/admission/totnghiep_thpt" class="info-card">
              <div class="info-card-inner">
                <div class="card-icon">
                  <i class="bi bi-file-earmark-text-fill"></i>
                </div>
                <h3>Xét tuyển theo điểm thi tốt nghiệp THPT</h3>
                <p>Xét tuyển dựa trên kết quả kỳ thi tốt nghiệp THPT quốc gia năm 2025</p>
                <span class="read-more">Chi tiết <i class="bi bi-arrow-right"></i></span>
              </div>
            </router-link>
          </div>
          
          <div class="col-md-4">
            <router-link to="/admission/hocba_thpt" class="info-card">
              <div class="info-card-inner">
                <div class="card-icon">
                  <i class="bi bi-journal-album"></i>
                </div>
                <h3>Xét tuyển theo điểm học tập THPT</h3>
                <p>Xét tuyển dựa trên kết quả học tập trong quá trình học THPT</p>
                <span class="read-more">Chi tiết <i class="bi bi-arrow-right"></i></span>
              </div>
            </router-link>
          </div>
          
          <div class="col-md-4">
            <router-link to="/admission/xettuyenrieng" class="info-card">
              <div class="info-card-inner">
                <div class="card-icon">
                  <i class="bi bi-patch-check-fill"></i>
                </div>
                <h3>Xét tuyển riêng theo đề án</h3>
                <p>Phương thức xét tuyển riêng theo đề án tuyển sinh của nhà trường</p>
                <span class="read-more">Chi tiết <i class="bi bi-arrow-right"></i></span>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Support tools section -->
    <section class="tools-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Công cụ hỗ trợ</h2>
        </div>
        
        <div class="row g-4">
          <div class="col-md-6 col-lg-3">
            <router-link to="/calculatescore/thpt" class="tool-card">
              <div class="tool-icon">
                <i class="bi bi-calculator-fill"></i>
              </div>
              <h3>Tính điểm xét tuyển thi THPT</h3>
            </router-link>
          </div>
          
          <div class="col-md-6 col-lg-3">
            <router-link to="/calculatescore/hb" class="tool-card">
              <div class="tool-icon">
                <i class="bi bi-calculator"></i>
              </div>
              <h3>Tính điểm xét tuyển học bạ</h3>
            </router-link>
          </div>
          
          <div class="col-md-6 col-lg-3">
            <router-link to="/calculatescore/xettuyenrieng" class="tool-card">
              <div class="tool-icon">
                <i class="bi bi-puzzle-fill"></i>
              </div>
              <h3>Tính điểm xét tuyển riêng</h3>
            </router-link>
          </div>
          
          <div class="col-md-6 col-lg-3">
            <router-link to="/school-priority" class="tool-card">
              <div class="tool-icon">
                <i class="bi bi-geo-alt"></i>
              </div>
              <h3>Tra cứu điểm ưu tiên khu vực</h3>
            </router-link>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Statistics section -->
    <section class="stats-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Thống kê & Dữ liệu</h2>
        </div>
        
        <div class="row g-4">
          <div class="col-md-6">
            <router-link to="/statistics/previous-admission" class="stat-card">
              <div class="stat-card-inner">
                <div class="card-icon">
                  <i class="bi bi-graph-up"></i>
                </div>
                <div class="stat-content">
                  <h3>Điểm chuẩn các năm trước</h3>
                  <p>Tra cứu điểm chuẩn trúng tuyển các ngành trong những năm qua</p>
                </div>
              </div>
            </router-link>
          </div>
          
          <div class="col-md-6">
            <router-link to="/statistics/pre-admitted-student" class="stat-card">
              <div class="stat-card-inner">
                <div class="card-icon">
                  <i class="bi bi-people-fill"></i>
                </div>
                <div class="stat-content">
                  <h3>Thống kê sinh viên nhập học</h3>
                  <p>Dữ liệu thống kê về sinh viên nhập học các năm trước</p>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Q&A and support section -->
    <section class="qa-section">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <div class="qa-content">
              <h2>Bạn cần hỗ trợ?</h2>
              <p>Trường Đại học Bách Khoa - Đại học Đà Nẵng luôn sẵn sàng giải đáp thắc mắc và tư vấn cho thí sinh về quy trình tuyển sinh, ngành học và các thông tin liên quan.</p>
              <div class="qa-buttons">
                <router-link to="/qa" class="qa-button">
                  <i class="bi bi-question-circle-fill"></i> Hỏi đáp Q&A
                </router-link>
                <router-link to="/chat" class="qa-button">
                  <i class="bi bi-chat-dots-fill"></i> Chat với trợ lý
                </router-link>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="contact-info">
              <h3>Thông tin liên hệ</h3>
              <div class="contact-item">
                <i class="bi bi-geo-alt-fill"></i>
                <span>54 Nguyễn Lương Bằng, Phường Hòa Khánh Bắc, Quận Liên Chiểu, Thành Phố Đà Nẵng</span>
              </div>
              <div class="contact-item">
                <i class="bi bi-telephone-fill"></i>
                <span>0888 477 377 - 0888 377 177 - 0888 577 277</span>
              </div>
              <div class="contact-item">
                <i class="bi bi-envelope-fill"></i>
                <span>tuyensinhbkdn@dut.udn.vn</span>
              </div>
              <div class="social-links">
                <a href="https://www.facebook.com/bachkhoaDUT" target="_blank" class="social-link" aria-label="Facebook">
                  <i class="bi bi-facebook"></i>
                </a>
                <a href="https://www.youtube.com/@DUTMedia" target="_blank" class="social-link" aria-label="YouTube">
                  <i class="bi bi-youtube"></i>
                </a>
                <a href="https://dut.udn.vn/" target="_blank" class="social-link" aria-label="Website">
                  <i class="bi bi-globe"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      carouselImages: [
        '/poster_1.png', 
        '/poster_2.png', 
        '/poster_3.jpg'
      ],
      currentSlide: 0,
      currentSlideWithTransition: 0,
      slideInterval: null,
      isTransitioning: false
    }
  },
  mounted() {
    // Set page title for SEO
    document.title = 'Trang chủ - Đại học Bách Khoa - Đại học Đà Nẵng'
    
    // Start carousel
    this.startCarousel()
  },
  beforeUnmount() {
    // Stop carousel when component unmounts
    this.stopCarousel()
  },
  methods: {
    // Carousel methods
    startCarousel() {
      this.slideInterval = setInterval(() => {
        this.nextSlide()
      }, 5000) // 5 seconds per slide
    },
    
    stopCarousel() {
      clearInterval(this.slideInterval)
    },
    
    nextSlide() {
      if (this.isTransitioning) return;
      this.isTransitioning = true;
      
      const nextSlide = (this.currentSlide + 1) % this.carouselImages.length;
      this.currentSlideWithTransition = this.currentSlide;
      
      setTimeout(() => {
        this.currentSlideWithTransition = nextSlide;
        
        setTimeout(() => {
          this.currentSlide = nextSlide;
          this.isTransitioning = false;
        }, 500);
      }, 50);
      
      this.resetCarouselTimer();
    },
    
    prevSlide() {
      if (this.isTransitioning) return;
      this.isTransitioning = true;
      
      const prevSlide = (this.currentSlide - 1 + this.carouselImages.length) % this.carouselImages.length;
      this.currentSlideWithTransition = this.currentSlide;
      
      setTimeout(() => {
        this.currentSlideWithTransition = prevSlide;
        
        setTimeout(() => {
          this.currentSlide = prevSlide;
          this.isTransitioning = false;
        }, 500);
      }, 50);
      
      this.resetCarouselTimer();
    },
    
    goToSlide(index) {
      if (this.isTransitioning || this.currentSlide === index) return;
      this.isTransitioning = true;
      
      const direction = index > this.currentSlide ? 1 : -1;
      this.currentSlideWithTransition = this.currentSlide;
      
      setTimeout(() => {
        this.currentSlideWithTransition = this.currentSlide + direction * 
                                       (direction > 0 ? (index - this.currentSlide) : (this.currentSlide - index));
        
        setTimeout(() => {
          this.currentSlide = index;
          this.currentSlideWithTransition = index;
          this.isTransitioning = false;
        }, 500);
      }, 50);
      
      this.resetCarouselTimer();
    },
    
    resetCarouselTimer() {
      this.stopCarousel();
      this.startCarousel();
    }
  }
}
</script>

<style scoped>
/* Base styles */
.home-container {
  width: 100%;
  overflow-x: hidden;
  color: #333;
}

/* Section common styles */
section {
  padding: 3rem 0;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #0B2942;
  position: relative;
  margin-bottom: 2rem;
}

.section-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -10px;
  height: 4px;
  width: 60px;
  background: #4da0ff;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.view-all {
  text-decoration: none;
  color: #4da0ff;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.view-all:hover {
  transform: translateX(5px);
}

/* Carousel styles (preserved from original but optimized) */
.carousel-section {
  padding: 0;
}

.carousel-container {
  width: 100%;
  aspect-ratio: 16 / 5;
  overflow: hidden;
  position: relative;
}

.carousel-slides {
  width: 100%;
  height: 100%;
  position: relative;
}

.carousel-slide {
  position: absolute;
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease-in-out;
  left: 0;
  top: 0;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.8rem;
  color: white;
  z-index: 2;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.carousel-nav:hover {
  background-color: rgba(255, 255, 255, 0.4);
}

.carousel-prev {
  left: 20px;
}

.carousel-next {
  right: 20px;
}

.carousel-indicators-container {
  position: absolute;
  bottom: 20px;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  z-index: 2;
}

.carousel-indicators {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.carousel-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-indicator.active,
.carousel-indicator:hover {
  background-color: #fff;
  transform: scale(1.2);
}

/* Mission section */
.mission-section {
  background: linear-gradient(135deg, #0B2942 0%, #1a73e8 100%);
  color: white;
  padding: 3.5rem 0;
}

.mission-content {
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}

.university-name {
  font-weight: 700;
  font-size: 2.2rem;
  margin-bottom: 1.5rem;
}

.mission-text {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 2rem;
  padding: 0 1rem;
}

.university-stats {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #4da0ff;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  color: #e0e0e0;
}

/* Quick access section */
.quick-access-section {
  background-color: #f8f9fa;
  padding: 4rem 0;
}

.quick-access-section .section-title {
  text-align: center;
  margin-bottom: 3rem;
}

.quick-access-section .section-title::after {
  left: 50%;
  transform: translateX(-50%);
}

.quick-links {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.quick-link-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #333;
  transition: all 0.3s ease;
  width: 200px;
}

.quick-link-item:hover {
  transform: translateY(-10px);
}

.icon-wrapper {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  font-size: 2.5rem;
}

.quick-link-item span {
  font-weight: 600;
  font-size: 1.1rem;
  text-align: center;
}

.quick-link-item.admission .icon-wrapper {
  background-color: rgba(77, 160, 255, 0.15);
  color: #4da0ff;
}

.quick-link-item.programs .icon-wrapper {
  background-color: rgba(255, 193, 7, 0.15);
  color: #ffc107;
}

.quick-link-item.scholarship .icon-wrapper {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
}

.quick-link-item.curriculum .icon-wrapper {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
}

.quick-link-item:hover .icon-wrapper {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* Admission section */
.admission-section {
  padding: 4rem 0;
}

.info-card {
  display: block;
  text-decoration: none;
  color: inherit;
  height: 100%;
}

.info-card-inner {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  height: 100%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid #eaeaea;
}

.info-card-inner:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border-color: #4da0ff;
}

.info-card .card-icon {
  font-size: 2rem;
  color: #0B2942;
  margin-bottom: 1rem;
}

.info-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #0B2942;
}

.info-card p {
  color: #6c757d;
  font-size: 0.95rem;
  margin-bottom: 1rem;
  flex-grow: 1;
}

.info-card .read-more {
  color: #4da0ff;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: auto;
}

.info-card-inner:hover .read-more i {
  transform: translateX(5px);
  transition: transform 0.3s ease;
}

/* Tools section */
.tools-section {
  background-color: #f8f9fa;
  padding: 4rem 0;
}

.tool-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  height: 100%;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: inherit;
  border: 1px solid #eaeaea;
}

.tool-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border-color: #4da0ff;
}

.tool-icon {
  font-size: 2.5rem;
  color: #0B2942;
  margin-bottom: 1rem;
}

.tool-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  text-align: center;
}

/* Stats section */
.stats-section {
  padding: 4rem 0;
}

.stat-card {
  display: block;
  text-decoration: none;
  color: inherit;
  height: 100%;
}

.stat-card-inner {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  height: 100%;
  border: 1px solid #eaeaea;
}

.stat-card-inner:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border-color: #4da0ff;
}

.stat-card .card-icon {
  font-size: 2.5rem;
  color: #0B2942;
  flex-shrink: 0;
}

.stat-content {
  flex-grow: 1;
}

.stat-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #0B2942;
}

.stat-card p {
  color: #6c757d;
  font-size: 0.95rem;
  margin-bottom: 0;
}

/* Faculty section */
.faculty-section {
  background-color: #f8f9fa;
  padding: 4rem 0;
}

.faculty-card {
  display: block;
  text-decoration: none;
  color: inherit;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  margin: 0 auto;
  max-width: 500px;
  border: 1px solid #eaeaea;
}

.faculty-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border-color: #4da0ff;
}

.faculty-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.faculty-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.faculty-card:hover .faculty-image img {
  transform: scale(1.05);
}

.faculty-info {
  padding: 1.5rem;
}

.faculty-info h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #0B2942;
}

.faculty-info p {
  color: #6c757d;
  font-size: 0.95rem;
  margin-bottom: 0;
}

/* Q&A section */
.qa-section {
  background: linear-gradient(135deg, #0B2942 0%, #1a73e8 100%);
  color: white;
  padding: 4rem 0;
}

.qa-content {
  padding: 1rem;
  height: 100%;
}

.qa-content h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.qa-content p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.7;
}

.qa-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.qa-button {
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 30px;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  font-weight: 500;
}

.qa-button:hover {
  background: white;
  color: #0B2942;
  transform: translateY(-3px);
}

.contact-info {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(5px);
  height: 100%;
}

.contact-info h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.contact-item i {
  font-size: 1.2rem;
  margin-right: 1rem;
  margin-top: 0.2rem;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: white;
  color: #0B2942;
  transform: translateY(-3px);
}

/* Responsive styles */
@media (max-width: 992px) {
  .section-title {
    font-size: 1.75rem;
  }
  
  .carousel-container {
    aspect-ratio: 16 / 6;
  }
  
  .university-name {
    font-size: 1.8rem;
  }
  
  .mission-text {
    font-size: 1rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .contact-info {
    margin-top: 2rem;
  }
}

@media (max-width: 768px) {
  .carousel-container {
    aspect-ratio: 16 / 7;
  }
  
  .university-stats {
    gap: 1rem;
  }
  
  .stat-item {
    width: 45%;
  }
  
  .quick-links {
    gap: 1rem;
  }
  
  .icon-wrapper {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }
  
  .carousel-nav {
    width: 40px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .faculty-image {
    height: 160px;
  }
  
  .qa-content, .contact-info {
    padding: 1.5rem;
  }
}

@media (max-width: 576px) {
  section {
    padding: 2rem 0;
  }
  
  .carousel-container {
    aspect-ratio: 16 / 9;
  }
  
  .university-name {
    font-size: 1.5rem;
  }
  
  .university-stats {
    flex-direction: column;
    gap: 1.5rem;
    align-items: center;
  }
  
  .carousel-nav {
    width: 35px;
    height: 50px;
    font-size: 1.2rem;
  }
  
  .carousel-prev {
    left: 10px;
  }
  
  .carousel-next {
    right: 10px;
  }
  
  .quick-link-item {
    width: 45%;
  }
  
  .icon-wrapper {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .view-all {
    align-self: flex-end;
  }
}
</style>