<template>
    <div>
      <!-- Header -->
      <section class="py-5 ctdt-header">
        <div class="container text-center">
          <h1 class="mb-3">Khám phá Chương Trình Đào Tạo CNTT</h1>
          <p class="lead">Dành cho các thí sinh và học sinh đang tìm hiểu thông tin ngành Công nghệ Thông tin</p>
        </div>
      </section>
  
      <!-- Thanh điều hướng chọn ngành học -->
      <nav class="program-nav py-3">
        <div class="container">
          <ul class="nav nav-pills justify-content-center">
            <li class="nav-item">
              <a class="nav-link" :class="{ active: selectedProgram === 'All' }" href="#" @click.prevent="filterProgram('All')">
                <i class="bi bi-grid"></i> Tất cả
              </a>
            </li>
            <li class="nav-item" v-for="program in uniquePrograms" :key="program">
              <a class="nav-link" :class="{ active: selectedProgram === program }" href="#" @click.prevent="filterProgram(program)">
                <i class="bi bi-book"></i> {{ program }}
              </a>
            </li>
          </ul>
        </div>
      </nav>
  
      <!-- Nội dung chương trình đào tạo -->
      <section class="py-5 ctdt-content">
        <div class="container">
          <div v-for="program in filteredData" :key="program.program" class="mb-5">
            <h2 class="mb-4">{{ program.program }}</h2>
            <div class="row">
              <div class="col-12 mb-4" v-for="file in program.files" :key="file.label">
                <div class="card shadow-sm">
                  <div class="card-header">
                    {{ file.label }}
                  </div>
                  <div class="card-body">
                    <iframe :src="file.url + '#toolbar=0'" width="100%" height="600px" frameborder="0"></iframe>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: 'CTDT',
    data() {
      return {
        pdfData: [],
        selectedProgram: 'All'
      }
    },
    computed: {
      uniquePrograms() {
        const programs = this.pdfData.map(item => item.program)
        return [...new Set(programs)]
      },
      filteredData() {
        if (this.selectedProgram === 'All') return this.pdfData
        return this.pdfData.filter(item => item.program === this.selectedProgram)
      }
    },
    methods: {
      filterProgram(program) {
        this.selectedProgram = program
      }
    },
    mounted() {
      axios.get('http://localhost:8000/it/ctdt')
        .then(res => {
          this.pdfData = res.data
        })
        .catch(err => console.error(err))
    }
  }
  </script>
  
  <style scoped>
  /* Header: nền gradient tạo cảm giác hiện đại và chuyên nghiệp */
  .ctdt-header {
    background: linear-gradient(135deg, #001f3f, #003366);
    color: #fff;
    padding: 60px 0;
  }
  
  /* Nội dung chính: nền sáng, màu chữ tối */
  .ctdt-content {
    background-color: #f9f9f9;
    color: #333;
  }
  
  /* Thanh điều hướng ngành học */
  .program-nav {
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 30px;
  }
  .program-nav .nav-link {
    font-size: 1rem;
    font-weight: 500;
    color: #007bff;
    transition: background-color 0.3s, color 0.3s;
  }
  .program-nav .nav-link.active {
    background-color: #007bff;
    color: #fff;
  }
  .program-nav .nav-link:hover {
    background-color: #007bff;
    color: #fff;
  }
  
  /* Card: thiết kế mềm mại và hiện đại */
  .card {
    border: none;
    border-radius: 8px;
  }
  .card-header {
    background-color: #007bff;
    color: #fff;
    font-weight: bold;
  }
  </style>
  