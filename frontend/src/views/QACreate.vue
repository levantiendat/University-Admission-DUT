<template>
    <div class="container mt-4">
      <button class="btn btn-secondary mb-3" @click="$router.go(-1)">Back</button>
      <div class="card card-custom shadow-sm">
        <div class="card-header custom-header">
          <h2 class="mb-0">Create New Question</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="createQuestion">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input type="email" v-model="question.email" class="form-control" :disabled="isAuthenticated" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input type="text" v-model="question.user_name" class="form-control" :disabled="isAuthenticated" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Question</label>
              <textarea v-model="question.question_text" class="form-control" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn btn-custom">Submit Question</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: 'QACreate',
    data() {
      return {
        question: {
          email: '',
          user_name: '',
          question_text: ''
        }
      }
    },
    computed: {
      isAuthenticated() {
        return !!localStorage.getItem('token')
      }
    },
    mounted() {
      if (this.isAuthenticated) {
        const token = localStorage.getItem('token')
        axios.get('http://localhost:8000/users/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(res => {
          this.question.email = res.data.email
          this.question.user_name = res.data.full_name
        })
        .catch(err => console.error(err))
      }
    },
    methods: {
      createQuestion() {
        const formData = new FormData()
        formData.append('email', this.question.email)
        formData.append('user_name', this.question.user_name)
        formData.append('question_text', this.question.question_text)
        axios.post('http://localhost:8000/it/Q&A/create', formData)
          .then(() => {
            alert("Your question has been submitted.")
            this.$router.push({ name: 'QAList' })
          })
          .catch(err => {
            console.error(err)
            alert(err.response.data.detail)
          })
      }
    }
  }
  </script>
  
  <style scoped>
  .card-custom {
    border: 1px solid #dee2e6;
    border-radius: 0.5rem;
  }
  .custom-header {
    background-color: #0062cc;
    color: #fff;
    padding: 1rem;
  }
  .btn-custom {
    background-color: #0062cc;
    border: none;
    color: #fff;
  }
  .btn-custom:hover {
    background-color: #004a9c;
  }
  </style>
  