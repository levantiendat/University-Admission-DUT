// src/store.js
import { reactive } from 'vue'

const state = reactive({
  token: localStorage.getItem('token') || '',
  user: {}  // Ví dụ lưu thông tin người dùng (chỉ dùng email ở đây)
})

// Hàm lưu token vào store và localStorage
function setToken(token) {
  state.token = token
  localStorage.setItem('token', token)
  initUser() // Cập nhật thông tin user sau khi lưu token
}

// Hàm xóa token
function clearToken() {
  state.token = ''
  state.user = {}
  localStorage.removeItem('token')
}

// Hàm giải mã token JWT (không xác thực chữ ký)
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (error) {
    console.error("Lỗi giải mã token:", error)
    return null
  }
}

// Khởi tạo thông tin user dựa trên token
function initUser() {
  if (state.token) {
    const payload = parseJwt(state.token)
    if (payload && payload.sub) {
      state.user.email = payload.sub
    }
  }
}

// Khi khởi động, nếu có token trong localStorage, cập nhật thông tin user
initUser()

export default {
  state,
  setToken,
  clearToken,
  parseJwt,
  initUser
}
