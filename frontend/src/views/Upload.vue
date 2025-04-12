<template>
    <div class="container mt-4">
      <h2>Upload file Excel để nhập dữ liệu</h2>
      <form @submit.prevent="uploadFile" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="excel_file" class="form-label">Chọn file Excel</label>
          <input type="file" class="form-control" id="excel_file" @change="handleFile" accept=".xlsx, .xls" required>
        </div>
        <button type="submit" class="btn btn-success">Upload</button>
      </form>
      <p class="mt-3">Lưu ý: File Excel phải có các cột: <code>STT, Mã Tỉnh/TP, Tên Tỉnh/TP, Mã Quận/Huyện, Tên Quận/Huyện, Mã Trường, Tên Trường, Địa Chỉ, Khu vực, Trường DTNT</code></p>
      <p v-if="message" class="mt-3">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: 'Upload',
    data() {
      return {
        file: null,
        message: ''
      }
    },
    methods: {
      handleFile(event) {
        this.file = event.target.files[0]
      },
      uploadFile() {
        if (!this.file) return
        const formData = new FormData()
        formData.append('excel_file', this.file)
        axios.post('http://localhost:8000/upload', formData)
          .then(res => {
            this.message = res.data.message
          })
          .catch(err => {
            console.error(err)
            this.message = err.response.data.message || "Có lỗi xảy ra"
          })
      }
    }
  }
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  </style>
  