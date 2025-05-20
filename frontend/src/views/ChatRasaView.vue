<template>
  <div class="chat-container">
    <div class="chat-header">
      <div class="chat-title">
        <img src="/dut_logo.png" alt="DUT Logo" class="chat-logo" />
        <div class="title-text">
          <h1>Trợ lý tư vấn tuyển sinh DUT</h1>
          <p class="subtitle">Đại học Bách Khoa - Đại học Đà Nẵng</p>
        </div>
      </div>
      <div class="chat-actions">
        <div class="files-dropdown" v-if="downloadableFiles.length > 0">
          <button class="btn btn-sm btn-outline-light files-toggle" @click="toggleFilesMenu">
            <i class="bi bi-file-earmark-word"></i> 
            <span>Tài liệu</span>
            <span class="files-count">{{ downloadableFiles.length }}</span>
          </button>
          <div class="files-menu" :class="{'show': isFilesMenuOpen}">
            <div class="files-header">
              <span>Tài liệu có thể tải xuống</span>
            </div>
            <div class="files-list">
              <div 
                v-for="(file, index) in downloadableFiles" 
                :key="index" 
                class="file-item"
                @click="downloadDocument(file.content, file.filename)"
              >
                <i class="bi bi-file-earmark-word"></i>
                <span class="file-name">{{ file.filename }}</span>
                <i class="bi bi-download"></i>
              </div>
            </div>
          </div>
        </div>
        <button @click="resetChat" class="btn btn-sm btn-outline-light">
          <i class="bi bi-arrow-repeat"></i> <span>Bắt đầu lại</span>
        </button>
      </div>
    </div>
    
    <div class="chat-messages" ref="messageContainer">
      <div 
        v-for="message in messages" 
        :key="message.id" 
        :class="['message', message.sender === 'user' ? 'user-message' : 'bot-message']"
      >
        <div class="message-avatar">
          <i v-if="message.sender === 'user'" class="bi bi-person-circle"></i>
          <img v-else src="@/assets/dut_logo.jpg" alt="Bot" class="bot-avatar" />
        </div>
        <div class="message-content">
          <div class="message-text" v-html="formatMessage(message.visibleText || message.text)"></div>
          
          <!-- Document download section if applicable -->
          <div v-if="message.documentContent" class="document-download-section">
            <button @click="downloadDocument(message.documentContent, message.docFilename)" class="document-download-btn">
              <i class="bi bi-file-earmark-word"></i>
              <span>Tải xuống tài liệu</span>
            </button>
          </div>
          
          <!-- Handle buttons if any -->
          <div v-if="message.buttons && message.buttons.length" class="message-buttons">
            <button 
              v-for="(button, idx) in message.buttons" 
              :key="idx" 
              @click="handleButtonClick(button.payload || button.title)"
              class="btn btn-sm btn-primary message-button"
            >
              {{ button.title }}
            </button>
          </div>
          
          <!-- Handle images if any -->
          <div v-if="message.image" class="message-image">
            <img :src="message.image" alt="Hình ảnh tuyển sinh DUT" />
          </div>
          
          <small class="message-time">{{ formatTime(message.timestamp) }}</small>
        </div>
      </div>
      
      <div v-if="loading" class="bot-typing">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
    
    <div class="chat-input">
      <form @submit.prevent="sendMessage">
        <div class="input-group">
          <input 
            type="text" 
            v-model="newMessage" 
            class="form-control" 
            placeholder="Nhập câu hỏi tuyển sinh tại đây..." 
            :disabled="loading"
            ref="messageInput"
            aria-label="Nhập câu hỏi tuyển sinh"
          />
          <button 
            class="btn btn-primary" 
            type="submit" 
            :disabled="!newMessage.trim() || loading"
            aria-label="Gửi câu hỏi"
          >
            <i class="bi bi-send-fill"></i>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch, computed } from 'vue';
import ChatRasaServices from '@/models/ChatRasaServices';
import ChatRasaController from '@/controllers/ChatRasaController';
import { useRouter } from 'vue-router';

export default {
  name: 'ChatRasaView',
  
  setup() {
    const router = useRouter();
    const messages = ref([]);
    const newMessage = ref('');
    const loading = ref(false);
    const messageContainer = ref(null);
    const messageInput = ref(null);
    const isFilesMenuOpen = ref(false);
    
    // Computed property for downloadable files
    const downloadableFiles = computed(() => {
      return messages.value
        .filter(message => message.documentContent && message.docFilename)
        .map(message => ({
          content: message.documentContent,
          filename: message.docFilename
        }));
    });
    
    // Toggle files menu
    const toggleFilesMenu = () => {
      isFilesMenuOpen.value = !isFilesMenuOpen.value;
    };
    
    // Close files menu when clicking outside
    onMounted(() => {
      document.addEventListener('click', (event) => {
        const filesDropdown = document.querySelector('.files-dropdown');
        if (isFilesMenuOpen.value && filesDropdown && !filesDropdown.contains(event.target)) {
          isFilesMenuOpen.value = false;
        }
      });
      
      // Focus input when page loads
      if (messageInput.value) {
        messageInput.value.focus();
      }
    });
    
    // Initialize chat
    onMounted(() => {
      messages.value = ChatRasaController.initializeChat();
      scrollToBottom();
      
      // Add animation class to messages after a short delay
      setTimeout(() => {
        const messageElements = document.querySelectorAll('.message');
        messageElements.forEach((element, index) => {
          setTimeout(() => {
            element.classList.add('show');
          }, index * 150);
        });
      }, 300);
    });
    
    // Watch messages and scroll to bottom when they change
    watch(messages, (newVal, oldVal) => {
      nextTick(() => {
        scrollToBottom();
        
        // Add animation to new messages
        if (oldVal && newVal.length > oldVal.length) {
          const newMessages = document.querySelectorAll('.message:not(.show)');
          newMessages.forEach((element, index) => {
            setTimeout(() => {
              element.classList.add('show');
            }, index * 150);
          });
        }
      });
    }, { deep: true });
    
    // Scroll to bottom of message container
    const scrollToBottom = () => {
      if (messageContainer.value) {
        messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
      }
    };
    
    // Format message text (handle links, etc.)
    const formatMessage = (text) => {
      if (!text) return '';
      
      // Phân tách và xử lý văn bản theo từng phần
      const parts = [];
      
      // Bước 0: Xử lý các URL đặc biệt trong dấu ngoặc kép
      const quotedUrlRegex = /'(\/[^"]+)'/g;
      text = text.replace(quotedUrlRegex, (match, path) => {
        // Mã hóa URL trong dấu ngoặc kép để xử lý đúng các ký tự đặc biệt và dấu tiếng Việt
        const encodedPath = encodeURI(path);
        return `<a href="javascript:void(0)" onclick="window.dispatchEvent(new CustomEvent('navigate-to', {detail: '${encodedPath}'}))" class="internal-link special-link">Tại đây</a>`;
      });
      
      // Bước 1: Xử lý các URL đầy đủ
      const externalUrlRegex = /(https?:\/\/[^\s]+)/g;
      let match;
      let lastIndex = 0;
      
      while ((match = externalUrlRegex.exec(text)) !== null) {
        // Phần văn bản trước URL
        if (match.index > lastIndex) {
          parts.push(processInternalLinks(text.substring(lastIndex, match.index)));
        }
        
        // URL đầy đủ - giữ nguyên dạng link
        parts.push(`<a href="${match[0]}" target="_blank" rel="noopener noreferrer">${match[0]}</a>`);
        
        lastIndex = externalUrlRegex.lastIndex;
      }
      
      // Phần văn bản còn lại
      if (lastIndex < text.length) {
        parts.push(processInternalLinks(text.substring(lastIndex)));
      }
      
      return parts.join('');
      
      // Hàm xử lý các đường dẫn nội bộ
      function processInternalLinks(text) {
        // Nhận dạng các đường dẫn bắt đầu bằng / (nhưng không nằm trong dấu ngoặc kép, vì đã xử lý ở trên)
        const internalLinkRegex = /(\s|^)(\/[a-zA-Z0-9\/\-_]+(?:\?[a-zA-Z0-9\/\-_&=%ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệể]*)?)/g;
        
        return text.replace(internalLinkRegex, (match, before, path) => {
          // Mã hóa URL để xử lý đúng các ký tự đặc biệt và dấu tiếng Việt
          const encodedPath = encodeURI(path);
          return `${before}<a href="javascript:void(0)" onclick="window.dispatchEvent(new CustomEvent('navigate-to', {detail: '${encodedPath}'}))" class="internal-link">Tại đây</a>`;
        });
      }
    };
    
    // Download a document
    const downloadDocument = (content, filename) => {
      ChatRasaServices.createAndDownloadDocument(content, filename);
      // Close files menu if open
      isFilesMenuOpen.value = false;
    };
    
    // Format timestamp to readable time
    const formatTime = (timestamp) => {
      if (!timestamp) return '';
      
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };
    
    // Send message
    const sendMessage = async () => {
      if (!newMessage.value.trim() || loading.value) return;
      
      loading.value = true;
      
      try {
        messages.value = await ChatRasaController.sendMessage(newMessage.value.trim());
        newMessage.value = '';
        
        // Focus back on input after sending
        nextTick(() => {
          if (messageInput.value) {
            messageInput.value.focus();
          }
        });
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // Handle button click
    const handleButtonClick = (payload) => {
      newMessage.value = payload;
      sendMessage();
    };
    
    // Reset chat
    const resetChat = () => {
      if (confirm('Bạn có chắc chắn muốn bắt đầu cuộc trò chuyện mới?')) {
        messages.value = ChatRasaController.resetChat();
        messages.value = ChatRasaController.initializeChat();
        isFilesMenuOpen.value = false;
        
        // Focus input after reset
        nextTick(() => {
          if (messageInput.value) {
            messageInput.value.focus();
          }
        });
      }
    };
    
    // Listen for custom navigation events
    onMounted(() => {
      window.addEventListener('navigate-to', (event) => {
        const path = event.detail;
        router.push(path);
      });
    });
    
    return {
      messages,
      newMessage,
      loading,
      messageContainer,
      messageInput,
      downloadableFiles,
      isFilesMenuOpen,
      sendMessage,
      formatMessage,
      formatTime,
      handleButtonClick,
      resetChat,
      downloadDocument,
      toggleFilesMenu
    };
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f9fa;
  border-radius: 0;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
}

.chat-header {
  background: linear-gradient(90deg, #0B2942 0%, #1261c3 70%, #4da0ff 100%);
  color: white;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.chat-title {
  display: flex;
  align-items: center;
}

.title-text {
  background: linear-gradient(90deg, white 0%, rgba(255,255,255,0.9) 70%, rgba(255,255,255,0.7) 100%);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  text-shadow: 0px 1px 2px rgba(0,0,0,0.2);
}

.chat-logo {
  height: 40px;
  width: 40px;
  margin-right: 12px;
  filter: drop-shadow(0px 1px 2px rgba(0,0,0,0.2));
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.8);
  background-color: white;
  padding: 2px;
}

.title-text h1 {
  font-size: 1.2rem;
  margin-bottom: 0.1rem;
  font-weight: 600;
}

.subtitle {
  font-size: 0.8rem;
  opacity: 0.9;
  margin: 0;
}

.chat-actions {
  display: flex;
  gap: 10px;
}

/* Files dropdown styles */
.files-dropdown {
  position: relative;
}

.files-toggle {
  display: flex;
  align-items: center;
  gap: 5px;
  position: relative;
  border-color: rgba(255,255,255,0.7);
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.files-toggle:hover {
  background-color: rgba(255,255,255,0.15);
  transform: translateY(-1px);
}

.files-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  color: #0B2942;
  border-radius: 50%;
  min-width: 18px;
  height: 18px;
  font-size: 0.7rem;
  font-weight: bold;
  margin-left: 4px;
}

.files-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 5px;
  width: 250px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  color: #333;
  z-index: 100;
  opacity: 0;
  transform: translateY(-5px);
  pointer-events: none;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.files-menu.show {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.files-menu::before {
  content: '';
  position: absolute;
  top: -5px;
  right: 15px;
  width: 10px;
  height: 10px;
  background: white;
  transform: rotate(45deg);
  box-shadow: -2px -2px 3px rgba(0,0,0,0.05);
}

.files-header {
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
  font-weight: 600;
  color: #0B2942;
  font-size: 0.85rem;
}

.files-list {
  max-height: 250px;
  overflow-y: auto;
  padding: 4px 0;
}

.file-item {
  padding: 8px 12px;
  display: flex;
  align-items: center;
  transition: all 0.15s;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
}

.file-item:last-child {
  border-bottom: none;
}

.file-item:hover {
  background-color: #f0f7ff;
  transform: translateY(-1px);
}

.file-item i:first-child {
  color: #4da0ff;
  font-size: 1.1rem;
  margin-right: 10px;
}

.file-item i:last-child {
  margin-left: auto;
  color: #666;
  opacity: 0;
  transition: all 0.2s;
}

.file-item:hover i:last-child {
  opacity: 0.7;
}

.file-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
  font-size: 0.85rem;
}

/* Main Chat Area */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 3vw; /* Changed to 3vw from left and right as per request */
  background-color: #f8f9fa;
  background-image: linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)), 
                    url('@/assets/dut_logo.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 25%;
  background-blend-mode: lighten;
  background-attachment: fixed;
}

.message {
  display: flex;
  margin-bottom: 24px;
  max-width: 70%; /* Adjusted down to make messages appear closer to edges */
  align-items: flex-start;
  opacity: 0;
  transform: translateY(15px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.message.show {
  opacity: 1;
  transform: translateY(0);
}

.user-message {
  margin-left: auto;
  flex-direction: row-reverse;
}

.bot-message {
  margin-right: auto;
}

.message-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
  flex-shrink: 0;
  box-shadow: 0 3px 5px rgba(0,0,0,0.1);
}

.user-message .message-avatar {
  background: linear-gradient(135deg, #0B2942, #1261c3);
  color: white;
  font-size: 18px;
}

.bot-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1.5px solid white;
}

.message-content {
  padding: 14px 18px;
  border-radius: 16px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  font-size: 0.95rem;
  line-height: 1.5;
}

.user-message .message-content {
  background: linear-gradient(135deg, #0B2942, #1261c3, #4da0ff);
  color: white;
  border-top-right-radius: 4px;
}

.bot-message .message-content {
  background-color: white;
  color: #333;
  border-top-left-radius: 4px;
}

.user-message .message-content::before {
  content: '';
  position: absolute;
  right: -8px;
  top: 0;
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #0B2942, #1261c3);
  border-radius: 0 15px 0 0;
  z-index: -1;
}

.bot-message .message-content::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 0;
  width: 18px;
  height: 18px;
  background: white;
  border-radius: 15px 0 0 0;
  z-index: -1;
}

.message-text {
  margin-bottom: 5px;
  word-break: break-word;
  line-height: 1.5;
  white-space: pre-wrap; /* This preserves line breaks */
}

.document-download-section {
  margin-top: 10px;
}

.document-download-btn {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(90deg, white, #e6f0ff);
  color: #0B2942;
  border: none;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}

.user-message .document-download-btn {
  background: linear-gradient(90deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
}

.document-download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0,0,0,0.15);
}

.document-download-btn i {
  margin-right: 8px;
  font-size: 1.1rem;
  color: #4da0ff;
}

.message-text a {
  color: inherit;
  text-decoration: underline;
}

.internal-link {
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
}

.message-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.message-button {
  background-color: white;
  color: #4da0ff;
  border-color: #4da0ff;
  transition: all 0.2s ease;
  border-radius: 15px;
  font-size: 0.85rem;
  padding: 4px 12px;
}

.message-button:hover {
  background-color: #4da0ff;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}

.message-image img {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 10px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}

.message-time {
  font-size: 0.7rem;
  opacity: 0.7;
  display: block;
  margin-top: 6px;
  text-align: right;
}

.bot-message .message-time {
  text-align: left;
}

/* ChatGPT-style input at bottom */
.chat-input {
  padding: 15px 3vw; /* Changed to match the 3vw from chat messages */
  background-color: #f8f9fa;
  border-top: 1px solid rgba(0,0,0,0.08);
  margin-top: auto;
}

.input-group {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background-color: white;
  max-width: 1000px;
  margin: 0 auto;
}

.form-control {
  border-radius: 8px 0 0 8px !important;
  border: 1px solid #e0e0e0;
  padding: 12px 16px;
  font-size: 0.95rem;
  height: auto;
  background-color: white;
}

.form-control:focus {
  box-shadow: none;
  border-color: #4da0ff;
}

.btn-primary {
  background: linear-gradient(135deg, #0B2942, #1261c3, #4da0ff);
  border: none;
  border-radius: 0 8px 8px 0 !important;
  padding: 0 16px;
  font-size: 1.1rem;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0B2942, #1261c3);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.bot-typing {
  display: flex;
  margin-bottom: 24px;
  max-width: 70%;
  margin-right: auto;
}

.typing-indicator {
  display: flex;
  align-items: center;
  background-color: white;
  padding: 12px 18px;
  border-radius: 16px;
  border-top-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  position: relative;
}

.typing-indicator::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 0;
  width: 18px;
  height: 18px;
  background: white;
  border-radius: 15px 0 0 0;
  z-index: -1;
}

.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin: 0 3px;
  background-color: #4da0ff;
  border-radius: 50%;
  animation: typing 1.4s infinite both;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

.internal-link.special-link {
  font-weight: bold;
  text-decoration: underline;
  color: inherit;
  padding: 2px 5px;
  background-color: rgba(255,255,255,0.2);
  border-radius: 3px;
}

@keyframes typing {
  0% { transform: scale(0); opacity: 0.7; }
  50% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0); opacity: 0.7; }
}

/* Custom Scrollbar */
.chat-messages::-webkit-scrollbar,
.files-list::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track,
.files-list::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.05);
}

.chat-messages::-webkit-scrollbar-thumb,
.files-list::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.1);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover,
.files-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0,0,0,0.2);
}

/* Responsive adjustments */
@media (max-width: 991px) {
  .message {
    max-width: 75%;
  }
}

@media (max-width: 768px) {
  .chat-container {
    border-radius: 0;
  }
  
  .message {
    max-width: 80%;
  }
  
  .chat-logo {
    height: 35px;
    width: 35px;
  }
  
  .title-text h1 {
    font-size: 1.1rem;
  }
  
  .chat-actions button span {
    display: none;
  }
  
  .files-menu {
    width: 220px;
    right: -70px;
  }
  
  .files-menu::before {
    right: 85px;
  }
}

@media (max-width: 576px) {
  .chat-header {
    padding: 10px 12px;
  }
  
  .message {
    max-width: 85%;
  }
  
  .chat-input {
    padding: 10px 3vw;
  }
  
  .message-content {
    padding: 12px 15px;
  }
  
  .form-control {
    padding: 10px 15px;
  }
  
  .btn-primary {
    padding: 0 15px;
  }
}
</style>