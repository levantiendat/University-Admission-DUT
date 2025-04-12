// src/models/authService.js

import axios from 'axios'
import config from '@/config/apiConfig'  // nếu bạn đã tách riêng file cấu hình base API

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

export default {
  async login(email, password) {
    const data = new URLSearchParams({ username: email, password })
    return axios.post(`${BASE_API_URL}/auth/login`, data)
  },

  async register({ name, email, phone_number, password }) {
    // Gọi API đăng ký với body JSON
    return axios.post(`${BASE_API_URL}/auth/register`, {
      name,
      email,
      phone_number,
      password
    })
  },

  googleLoginUrl() {
    return `${BASE_API_URL}/auth/google`
  }
}
