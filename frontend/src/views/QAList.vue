<template>
    <div class="container mt-4">
      <h2 class="mb-4 text-center">Questions & Answers</h2>
      <div class="row" v-if="questions.length">
        <div class="col-md-6 col-lg-4" v-for="q in questions" :key="q.id">
          <div class="qa-card">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5>{{ q.user_name }}</h5>
              <small class="text-muted">{{ formatDate(q.question_time) }}</small>
            </div>
            <p>{{ q.question_text }}</p>
            <router-link :to="`/qa/${q.id}`" class="btn btn-detail">Detail</router-link>
          </div>
        </div>
      </div>
      <div v-else>
        <p class="text-center">No questions found.</p>
      </div>
      <!-- Floating button để tạo câu hỏi mới -->
      <router-link to="/qa/create" class="fab">+</router-link>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: 'QAList',
    data() {
      return {
        questions: []
      }
    },
    methods: {
      loadQuestions() {
        axios.get('http://localhost:8000/it/Q&A')
          .then(res => {
            this.questions = res.data
          })
          .catch(err => console.error(err))
      },
      formatDate(dateStr) {
        const date = new Date(dateStr)
        return date.toLocaleString()
      }
    },
    mounted() {
      this.loadQuestions()
    }
  }
  </script>
  
  <style scoped>
  .qa-card {
    border: 1px solid #dee2e6;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 1rem;
    background-color: #f8f9fa;
    transition: box-shadow 0.3s;
  }
  .qa-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  .btn-detail {
    background-color: #0062cc;
    color: #fff;
    padding: 0.5rem 1rem;
    text-decoration: none;
  }
  .fab {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background-color: #0062cc;
    color: #fff;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    text-decoration: none;
  }
  </style>
  