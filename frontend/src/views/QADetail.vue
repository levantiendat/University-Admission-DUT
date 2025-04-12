<template>
    <div class="container mt-4">
      <button class="btn btn-secondary mb-3" @click="$router.go(-1)">Back</button>
      <div class="card card-custom shadow-sm mb-4">
        <div class="card-header custom-header">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <strong>{{ question.user_name }}</strong> (<em>{{ question.email }}</em>)
            </div>
            <small>{{ formatDate(question.question_time) }}</small>
          </div>
        </div>
        <div class="card-body">
          <p>{{ question.question_text }}</p>
        </div>
      </div>
      <h4 class="text-center mt-4 mb-3">Answers</h4>
      <div v-if="answers.length">
        <div class="card card-custom shadow-sm mb-3" v-for="a in answers" :key="a.id">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <strong>{{ a.answer_name }}</strong>
              <small class="text-muted">{{ formatDate(a.answer_time) }}</small>
            </div>
          </div>
          <div class="card-body">
            <p>{{ a.answer_text }}</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p class="text-center">No answers yet.</p>
      </div>
      <!-- Add Answer Form -->
      <div class="card card-custom shadow-sm mt-4">
        <div class="card-header custom-header-secondary" @click="toggleForm">
          <h5 class="mb-0">Add an Answer</h5>
        </div>
        <div v-show="showForm" class="card-body">
          <form @submit.prevent="submitAnswer">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input type="email" v-model="answer.email" class="form-control" :disabled="isAuthenticated" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input type="text" v-model="answer.name" class="form-control" :disabled="isAuthenticated" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Answer</label>
              <textarea v-model="answer.text" class="form-control" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn btn-custom mt-3">Submit Answer</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: 'QADetail',
    data() {
      return {
        question: {},
        answers: [],
        showForm: false,
        answer: {
          email: '',
          name: '',
          text: ''
        }
      }
    },
    computed: {
      isAuthenticated() {
        return !!localStorage.getItem('token')
      }
    },
    methods: {
      loadDetail() {
        const qid = this.$route.params.question_id
        axios.get(`http://localhost:8000/it/Q&A/${qid}`)
          .then(res => {
            this.question = res.data.question
            this.answers = res.data.answers
          })
          .catch(err => console.error(err))
      },
      formatDate(dateStr) {
        const date = new Date(dateStr)
        return date.toLocaleString()
      },
      toggleForm() {
        this.showForm = !this.showForm
      },
      submitAnswer() {
        const qid = this.$route.params.question_id
        const formData = new FormData()
        formData.append('answer_email', this.answer.email)
        formData.append('answer_name', this.answer.name)
        formData.append('answer_text', this.answer.text)
        axios.post(`http://localhost:8000/it/Q&A/${qid}`, formData)
          .then(() => {
            alert("Your answer has been submitted.")
            this.loadDetail()
            this.answer = { email: '', name: '', text: '' }
            this.showForm = false
          })
          .catch(err => {
            console.error(err)
            alert(err.response.data.detail)
          })
      },
      loadUserInfo() {
        const token = localStorage.getItem('token')
        if (token) {
          axios.get('http://localhost:8000/users/me', {
            headers: { Authorization: `Bearer ${token}` }
          })
            .then(res => {
              this.answer.email = res.data.email
              this.answer.name = res.data.full_name
            })
            .catch(err => console.error(err))
        }
      }
    },
    mounted() {
      this.loadDetail()
      if (this.isAuthenticated) {
        this.loadUserInfo()
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
  .custom-header-secondary {
    background-color: #0062cc;
    color: #fff;
    cursor: pointer;
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
  