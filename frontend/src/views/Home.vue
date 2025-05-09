<template>
  <div class="home-container">
    <!-- Carousel tự động chạy hình -->
    <div class="container-fluid">
      <div class="carousel-container">
        <!-- Hình ảnh carousel -->
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

        <!-- Nút điều hướng -->
        <button class="carousel-nav carousel-prev" @click="prevSlide">
          <i class="bi bi-chevron-left"></i>
        </button>
        <button class="carousel-nav carousel-next" @click="nextSlide">
          <i class="bi bi-chevron-right"></i>
        </button>

        <!-- Chỉ số slide - đã điều chỉnh vị trí chính giữa -->
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

    <!-- Khu vực chức năng -->
    <div class="functions-container">
      <div class="container px-10vw">
        <div class="row g-4">
          <!-- Tính điểm xét tuyển -->
          <div class="col-md-4">
            <router-link to="/calculatescore/xettuyenrieng" class="function-card">
              <div class="function-image-container">
                <img src="/calculator.png" alt="Tính điểm xét tuyển phương thức xét tuyển riêng" class="function-image">
                <div class="function-overlay">
                  <h3 class="function-title">Tính điểm xét tuyển phương thức xét tuyển riêng</h3>
                </div>
              </div>
            </router-link>
          </div>

          <!-- Tra cứu khu vực ưu tiên -->
          <div class="col-md-4">
            <router-link to="/school-priority" class="function-card">
              <div class="function-image-container">
                <img src="/school.png" alt="Tra cứu khu vực ưu tiên" class="function-image">
                <div class="function-overlay">
                  <h3 class="function-title">Tra cứu khu vực ưu tiên</h3>
                </div>
              </div>
            </router-link>
          </div>

          <!-- Chương trình đào tạo -->
          <div class="col-md-4">
            <router-link to="/ctdt" class="function-card">
              <div class="function-image-container">
                <img src="/university.png" alt="Chương trình đào tạo" class="function-image">
                <div class="function-overlay">
                  <h3 class="function-title">Chương trình đào tạo</h3>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Phần nội dung khác có thể thêm ở đây -->
    <div class="additional-content">
      <div class="container px-10vw py-5">
        <h2 class="text-center mb-4">Đại học Đà Nẵng - Trường Đại học Bách Khoa</h2>
        <p>
          Chào mừng bạn đến với Cổng thông tin tuyển sinh của Trường Đại học Bách Khoa - Đại học Đà Nẵng. 
          Hệ thống này được thiết kế để giúp các thí sinh dễ dàng tiếp cận thông tin tuyển sinh, 
          tra cứu điểm và tìm hiểu về các chương trình đào tạo của nhà trường.
        </p>
      </div>
    </div>
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
    // Bắt đầu chạy carousel tự động
    this.startCarousel()
  },
  beforeUnmount() {
    // Dừng carousel khi component unmount
    this.stopCarousel()
  },
  methods: {
    // Chạy carousel tự động
    startCarousel() {
      this.slideInterval = setInterval(() => {
        this.nextSlide()
      }, 5000) // 5 giây cho mỗi slide
    },
    
    // Dừng carousel
    stopCarousel() {
      clearInterval(this.slideInterval)
    },
    
    // Đến slide tiếp theo
    nextSlide() {
      if (this.isTransitioning) return;
      this.isTransitioning = true;
      
      // Cập nhật giá trị transition
      const nextSlide = (this.currentSlide + 1) % this.carouselImages.length;
      this.currentSlideWithTransition = this.currentSlide;
      
      // Thực hiện transition
      setTimeout(() => {
        this.currentSlideWithTransition = nextSlide;
        
        // Sau khi transition hoàn tất, cập nhật slide hiện tại
        setTimeout(() => {
          this.currentSlide = nextSlide;
          this.isTransitioning = false;
        }, 500);
      }, 50);
      
      this.resetCarouselTimer();
    },
    
    // Đến slide trước đó
    prevSlide() {
      if (this.isTransitioning) return;
      this.isTransitioning = true;
      
      // Cập nhật giá trị transition
      const prevSlide = (this.currentSlide - 1 + this.carouselImages.length) % this.carouselImages.length;
      this.currentSlideWithTransition = this.currentSlide;
      
      // Thực hiện transition
      setTimeout(() => {
        this.currentSlideWithTransition = prevSlide;
        
        // Sau khi transition hoàn tất, cập nhật slide hiện tại
        setTimeout(() => {
          this.currentSlide = prevSlide;
          this.isTransitioning = false;
        }, 500);
      }, 50);
      
      this.resetCarouselTimer();
    },
    
    // Đến slide cụ thể
    goToSlide(index) {
      if (this.isTransitioning || this.currentSlide === index) return;
      this.isTransitioning = true;
      
      // Xác định hướng chuyển động
      const direction = index > this.currentSlide ? 1 : -1;
      this.currentSlideWithTransition = this.currentSlide;
      
      // Thực hiện transition
      setTimeout(() => {
        this.currentSlideWithTransition = this.currentSlide + direction * 
                                         (direction > 0 ? (index - this.currentSlide) : (this.currentSlide - index));
        
        // Sau khi transition hoàn tất, cập nhật slide hiện tại
        setTimeout(() => {
          this.currentSlide = index;
          this.currentSlideWithTransition = index;
          this.isTransitioning = false;
        }, 500);
      }, 50);
      
      this.resetCarouselTimer();
    },
    
    // Reset timer khi người dùng tương tác
    resetCarouselTimer() {
      this.stopCarousel();
      this.startCarousel();
    }
  }
}
</script>

<style scoped>
.home-container {
  width: 100%;
  overflow-x: hidden;
}

.carousel-container {
  width: 100%;
  aspect-ratio: 16 / 5; /* Tự động giữ đúng tỷ lệ 1600x500 */
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

/* Nút điều hướng carousel - cập nhật kiểu dáng */
.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(200, 200, 200, 0.5);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.5rem;
  color: #333;
  z-index: 2;
  transition: all 0.3s ease;
}

.carousel-nav:hover {
  background-color: rgba(200, 200, 200, 0.8);
}

.carousel-prev {
  left: 0;
}

.carousel-next {
  right: 0;
}

/* Indicators - sửa để đảm bảo nằm chính giữa */
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
}

/* Khu vực chức năng */
.functions-container {
  padding: 40px 0;
  background-color: #f8f9fa;
}

.function-card {
  display: block;
  text-decoration: none;
  color: inherit;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.function-image-container {
  position: relative;
  width: 100%;
  height: 250px;
  overflow: hidden;
}

.function-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.function-card:hover .function-image {
  transform: scale(1.05);
}

.function-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.7));
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 20px;
}

.function-title {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease;
}

.function-card:hover .function-title {
  transform: scale(1.1);
}

/* Additional Content */
.additional-content {
  padding: 20px 0;
  background-color: white;
}

/* Media Queries */
@media (max-width: 992px) {
  .carousel-container {
    aspect-ratio: 16 / 6;
  }
}

@media (max-width: 768px) {
  .carousel-container {
    aspect-ratio: 16 / 7;
  }
  
  .function-image-container {
    height: 200px;
  }
}

@media (max-width: 576px) {
  .carousel-container {
    aspect-ratio: 16 / 9;
  }
  
  .carousel-nav {
    width: 30px;
    height: 50px;
    font-size: 1.2rem;
  }
}
</style>