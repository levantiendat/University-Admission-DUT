<template>
  <div class="chat-container">
    <div class="chat-header">
      <div class="chat-title">
        <img src="/dut_logo.png" alt="DUT Logo" class="chat-logo" />
        <div>
          <h2>Trợ lý tư vấn tuyển sinh</h2>
          <small>Đại học Bách Khoa - Đại học Đà Nẵng</small>
        </div>
      </div>
      <div class="chat-actions">
        <button @click="resetChat" class="btn btn-sm btn-outline-light">
          <i class="bi bi-arrow-repeat"></i> Bắt đầu lại
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
            <p>Thông tin sẽ nằm ở file word, bạn có thể tải xuống</p>
            <button @click="downloadDocument(message.documentContent, message.docFilename)" class="btn btn-sm btn-primary">
              <i class="bi bi-download"></i> {{ message.docFilename }}
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
            <img :src="message.image" alt="Image" />
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
            placeholder="Nhập câu hỏi tại đây..." 
            :disabled="loading"
          />
          <button 
            class="btn btn-primary" 
            type="submit" 
            :disabled="!newMessage.trim() || loading"
          >
            <i class="bi bi-send-fill"></i>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue';
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
    
    // Initialize chat
    onMounted(() => {
      messages.value = ChatRasaController.initializeChat();
      scrollToBottom();
    });
    
    // Watch messages and scroll to bottom when they change
    watch(messages, () => {
      nextTick(() => {
        scrollToBottom();
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
      let remainingText = text;
      
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
        // Tìm các đường dẫn bắt đầu bằng /
        const internalLinkRegex = /(\s|^)(\/[a-zA-Z0-9\/\-_]+)(\s|$)/g;
        return text.replace(internalLinkRegex, (match, before, path, after) => 
          `${before}<a href="javascript:void(0)" onclick="window.dispatchEvent(new CustomEvent('navigate-to', {detail: '${path}'}))" class="internal-link">Tại đây</a>${after}`
        );
      }
    };
    
    // Download a document
    const downloadDocument = (content, filename) => {
      ChatRasaServices.createAndDownloadDocument(content, filename);
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
      sendMessage,
      formatMessage,
      formatTime,
      handleButtonClick,
      resetChat,
      downloadDocument
    };
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-header {
  background-color: #0B2942;
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-title {
  display: flex;
  align-items: center;
}

.chat-logo {
  height: 40px;
  width: auto;
  margin-right: 15px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f8f9fa;
  background-image: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), 
                    url('@/assets/dut_logo.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 50%;
  background-blend-mode: lighten;
  background-attachment: fixed;
}

.message {
  display: flex;
  margin-bottom: 15px;
  max-width: 85%;
  align-items: flex-start;
}

.user-message {
  margin-left: auto;
  flex-direction: row-reverse;
}

.bot-message {
  margin-right: auto;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
  flex-shrink: 0;
}

.user-message .message-avatar {
  background-color: #4da0ff;
  color: white;
  font-size: 20px;
}

.bot-avatar {
  width: 35px;
  height: 35px;
}

.message-content {
  padding: 10px 15px;
  border-radius: 15px;
  position: relative;
}

.user-message .message-content {
  background-color: #4da0ff;
  color: white;
  border-top-right-radius: 5px;
}

.bot-message .message-content {
  background-color: white;
  color: #333;
  border-top-left-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.message-text {
  margin-bottom: 5px;
  word-break: break-word;
  line-height: 1.4;
  white-space: pre-wrap; /* This preserves line breaks */
}

.document-download-section {
  margin-top: 10px;
  padding-top: 5px;
  border-top: 1px solid #eee;
  font-size: 0.9rem;
}

.document-download-section p {
  margin-bottom: 5px;
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
  gap: 5px;
  margin-top: 10px;
}

.message-button {
  background-color: white;
  color: #4da0ff;
  border-color: #4da0ff;
}

.message-button:hover {
  background-color: #4da0ff;
  color: white;
}

.message-image img {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 10px;
}

.message-time {
  font-size: 0.7rem;
  opacity: 0.7;
  display: block;
  margin-top: 5px;
}

.chat-input {
  padding: 15px;
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

.input-group {
  border-radius: 25px;
  overflow: hidden;
}

.form-control {
  border-radius: 25px 0 0 25px !important;
  border: 1px solid #4da0ff;
  padding: 10px 15px;
}

.form-control:focus {
  box-shadow: none;
  border-color: #4da0ff;
}

.btn-primary {
  background-color: #4da0ff;
  border-color: #4da0ff;
  border-radius: 0 25px 25px 0 !important;
  padding: 10px 20px;
}

.btn-primary:hover {
  background-color: #0B2942;
  border-color: #0B2942;
}

.bot-typing {
  display: flex;
  margin-bottom: 15px;
  max-width: 85%;
  margin-right: auto;
}

.typing-indicator {
  display: flex;
  align-items: center;
  background-color: #f0f0f0;
  padding: 10px 15px;
  border-radius: 15px;
}

.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin: 0 3px;
  background-color: #888;
  border-radius: 50%;
  animation: typing 1.4s infinite both;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0% { transform: scale(0); opacity: 0.7; }
  50% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0); opacity: 0.7; }
}

@media (max-width: 768px) {
  .chat-container {
    height: calc(100vh - 150px);
    border-radius: 0;
  }
  
  .message {
    max-width: 95%;
  }
}
</style>