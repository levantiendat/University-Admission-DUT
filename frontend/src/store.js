// src/store.js
import { reactive } from 'vue'

const STORAGE_KEY = 'token'

const state = reactive({
  token: sessionStorage.getItem(STORAGE_KEY) || '',
  user: {}
})

// Lưu token vào store và sessionStorage
function setToken(token) {
  state.token = token
  sessionStorage.setItem(STORAGE_KEY, token)
  initUser()
}

// Xóa token và thông tin user
function clearToken() {
  state.token = ''
  state.user = {}
  sessionStorage.removeItem(STORAGE_KEY)
}

// Giải mã token JWT (không xác thực chữ ký)
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
    console.error('Lỗi giải mã token:', error)
    return null
  }
}

// Khởi tạo user từ token
function initUser() {
  if (state.token) {
    const payload = parseJwt(state.token)
    if (payload && payload.sub) {
      state.user.email = payload.sub
    } else {
      clearToken() // Token lỗi thì xóa luôn
    }
  }
}

// Kiểm tra token còn hạn không
function isTokenValid() {
  if (!state.token) return false
  const payload = parseJwt(state.token)
  if (!payload || !payload.exp) return false
  const now = Date.now() / 1000
  return payload.exp > now
}

// Kiểm tra và tự động chuyển hướng nếu token hết hạn
function checkTokenOrRedirect(router) {
  if (!isTokenValid()) {
    alert('Vui lòng đăng nhập lại.')
    clearToken()
    router.push({ name: 'Login' })
  }
}

// Khi app khởi động, tự init thông tin
initUser()

export default {
  state,
  setToken,
  clearToken,
  parseJwt,
  initUser,
  isTokenValid,
  checkTokenOrRedirect
}
