<template>
  <div class="mini-chat-container" v-if="isAuthenticated">
    <!-- Chat toggle button -->
    <button 
      class="chat-toggle-btn" 
      @click="toggleChat" 
      :class="{ 'active': isChatOpen }"
      :title="isChatOpen ? 'Thu nhỏ' : 'Chat với trợ lý'"
    >
      <i v-if="isChatOpen" class="bi bi-x-lg"></i>
      <i v-else class="bi bi-chat-dots-fill"></i>
      <span v-if="unreadCount && !isChatOpen" class="unread-badge">{{ unreadCount }}</span>
    </button>
    
    <!-- Mini chat window -->
    <div class="mini-chat-window" :class="{ 'open': isChatOpen }">
      <div class="mini-chat-header">
        <div class="mini-chat-title">
          <img src="/dut_logo.png" alt="DUT Logo" class="mini-chat-logo" />
          <div>Trợ lý tuyển sinh</div>
        </div>
        <div class="mini-chat-actions">
          <button 
            v-if="downloadableFiles.length > 0" 
            @click="toggleFilesMenu" 
            class="btn btn-sm btn-link text-white" 
            title="Xem tài liệu"
          >
            <i class="bi bi-file-earmark-word"></i>
            <span class="mini-files-badge" v-if="downloadableFiles.length">{{ downloadableFiles.length }}</span>
          </button>
          <button @click="resetChat" class="btn btn-sm btn-link text-white" title="Bắt đầu lại">
            <i class="bi bi-arrow-repeat"></i>
          </button>
          <button @click="goToFullChat" class="btn btn-sm btn-link text-white" title="Mở rộng">
            <i class="bi bi-arrows-angle-expand"></i>
          </button>
        </div>
      </div>
      
      <!-- Files menu -->
      <div class="mini-files-menu" :class="{'show': isFilesMenuOpen}">
        <div class="mini-files-header">
          <span>Tài liệu có thể tải xuống</span>
          <button @click="toggleFilesMenu" class="mini-files-close">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="mini-files-list">
          <div 
            v-for="(file, index) in downloadableFiles" 
            :key="index" 
            class="mini-file-item"
            @click="downloadDocument(file.content, file.filename)"
          >
            <i class="bi bi-file-earmark-word"></i>
            <span class="mini-file-name">{{ file.filename }}</span>
            <i class="bi bi-download"></i>
          </div>
          <div v-if="downloadableFiles.length === 0" class="mini-no-files">
            Không có tài liệu nào
          </div>
        </div>
      </div>
      
      <div class="mini-chat-messages" ref="miniMessageContainer">
        <div 
          v-for="message in messages" 
          :key="message.id" 
          :class="['mini-message', message.sender === 'user' ? 'user-message' : 'bot-message']"
        >
          <div class="mini-message-avatar">
            <i v-if="message.sender === 'user'" class="bi bi-person-circle"></i>
            <img v-else src="@/assets/dut_logo.jpg" alt="Bot" class="mini-bot-avatar" />
          </div>
          <div class="mini-message-content">
            <div class="mini-message-text" v-html="formatMessage(message.visibleText || message.text)"></div>
            
            <!-- Document download section if applicable -->
            <div v-if="message.documentContent" class="mini-document-download">
              <button @click="downloadDocument(message.documentContent, message.docFilename)" class="mini-document-btn">
                <i class="bi bi-file-earmark-word"></i>
                <span>Tải tài liệu</span>
              </button>
            </div>
            
            <!-- Handle buttons if any -->
            <div v-if="message.buttons && message.buttons.length" class="mini-message-buttons">
              <button 
                v-for="(button, idx) in message.buttons" 
                :key="idx" 
                @click="handleButtonClick(button.payload || button.title)"
                class="btn btn-sm btn-outline-primary mini-message-button"
              >
                {{ button.title }}
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="mini-bot-typing">
          <div class="mini-typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      
      <div class="mini-chat-input">
        <form @submit.prevent="sendMessage">
          <div class="input-group">
            <input 
              type="text" 
              v-model="newMessage" 
              class="form-control" 
              placeholder="Nhập câu hỏi..." 
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
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useRouter } from 'vue-router';
import ChatRasaController from '@/controllers/ChatRasaController';
import ChatRasaServices from '@/models/ChatRasaServices';
import store from '@/store';

export default {
  name: 'MiniChatWidget',
  
  setup() {
    const router = useRouter();
    const isAuthenticated = computed(() => !!store.state.token);
    
    const isChatOpen = ref(false);
    const messages = ref([]);
    const newMessage = ref('');
    const loading = ref(false);
    const miniMessageContainer = ref(null);
    const unreadCount = ref(0);
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
    
    // Toggle chat window
    const toggleChat = () => {
      isChatOpen.value = !isChatOpen.value;
      isFilesMenuOpen.value = false;
      
      if (isChatOpen.value) {
        // Reset unread count when opening
        unreadCount.value = 0;
        
        // Initialize chat if not already
        if (messages.value.length === 0) {
          messages.value = ChatRasaController.initializeChat();
        }
        
        // Add animations to messages
        nextTick(() => {
          scrollToBottom();
          const messageElements = document.querySelectorAll('.mini-message:not(.show)');
          messageElements.forEach((element, index) => {
            setTimeout(() => {
              element.classList.add('show');
            }, index * 100);
          });
        });
      }
    };
    
    // Navigate to full chat page
    const goToFullChat = () => {
      router.push('/chat');
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
        const internalLinkRegex = /(\s|^)(\/[a-zA-Z0-9\/\-_]+(?:\?[a-zA-Z0-9\/\-_&=%]*)?)/g;
        
        return text.replace(internalLinkRegex, (match, before, path) => {
          // Mã hóa URL để xử lý đúng các ký tự đặc biệt và dấu tiếng Việt
          const encodedPath = encodeURI(path);
          return `${before}<a href="javascript:void(0)" onclick="window.dispatchEvent(new CustomEvent('navigate-to', {detail: '${encodedPath}'}))" class="internal-link">Tại đây</a>`;
        });
      }
    };
    
    // Download document
    const downloadDocument = (content, filename) => {
      ChatRasaServices.createAndDownloadDocument(content, filename);
      isFilesMenuOpen.value = false;
    };
    
    // Scroll to bottom of message container
    const scrollToBottom = () => {
      if (miniMessageContainer.value) {
        miniMessageContainer.value.scrollTop = miniMessageContainer.value.scrollHeight;
      }
    };
    
    // Send message
    const sendMessage = async () => {
      if (!newMessage.value.trim() || loading.value) return;
      
      loading.value = true;
      
      try {
        // Get updated messages from controller
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
        isFilesMenuOpen.value = false;
      }
    };
    
    // Watch messages and scroll to bottom when they change
    watch(messages, (newMessages, oldMessages) => {
      nextTick(() => {
        scrollToBottom();
        
        // Add animations to new messages
        if (oldMessages && newMessages.length > oldMessages.length) {
          const newMessageElements = document.querySelectorAll('.mini-message:not(.show)');
          newMessageElements.forEach((element, index) => {
            setTimeout(() => {
              element.classList.add('show');
            }, index * 100);
          });
          
          // Increment unread count if chat is closed and we have new bot messages
          if (!isChatOpen.value) {
            const newBotMessages = newMessages.filter(
              (msg, idx) => msg.sender === 'bot' && (idx >= oldMessages.length || msg.id !== oldMessages[idx]?.id)
            );
            unreadCount.value += newBotMessages.length;
          }
        }
      });
    }, { deep: true });
    
    // Close files menu when clicking outside
    onMounted(() => {
      document.addEventListener('click', (event) => {
        // Skip if chat is not open
        if (!isChatOpen.value) return;
        
        const filesMenu = document.querySelector('.mini-files-menu');
        const filesButton = document.querySelector('.mini-chat-actions button:first-child');
        
        if (isFilesMenuOpen.value && 
            filesMenu && 
            filesButton && 
            !filesMenu.contains(event.target) && 
            !filesButton.contains(event.target)) {
          isFilesMenuOpen.value = false;
        }
      });
      
      // Listen for custom navigation events
      window.addEventListener('navigate-to', (event) => {
        const path = event.detail;
        router.push(path);
      });
    });
    
    // Load existing chat history when mounted
    onMounted(() => {
      if (isAuthenticated.value) {
        messages.value = ChatRasaController.getChatHistory();
      }
    });
    
    return {
      isAuthenticated,
      isChatOpen,
      messages,
      newMessage,
      loading,
      unreadCount,
      miniMessageContainer,
      downloadableFiles,
      isFilesMenuOpen,
      toggleChat,
      goToFullChat,
      sendMessage,
      formatMessage,
      handleButtonClick,
      resetChat,
      downloadDocument,
      toggleFilesMenu
    };
  }
}
</script>

<style scoped>
.mini-chat-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1060;
}

.chat-toggle-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0B2942, #1261c3, #4da0ff);
  color: white;
  border: none;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s;
  z-index: 1062;
}

.chat-toggle-btn:hover {
  transform: scale(1.05) translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.chat-toggle-btn.active {
  background: linear-gradient(135deg, #dc3545, #e35d6a);
}

.unread-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.mini-chat-window {
  position: absolute;
  bottom: 75px;
  right: 0;
  width: 350px;
  height: 450px;
  border-radius: 12px;
  background-color: white;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform: scale(0.8) translateY(50px);
  opacity: 0;
  pointer-events: none;
}

.mini-chat-window.open {
  transform: scale(1) translateY(0);
  opacity: 1;
  pointer-events: all;
}

.mini-chat-header {
  background: linear-gradient(90deg, #0B2942 0%, #1261c3 70%, #4da0ff 100%);
  color: white;
  padding: 12px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.mini-chat-title {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  background: linear-gradient(90deg, white 0%, rgba(255,255,255,0.9) 70%, rgba(255,255,255,0.7) 100%);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.mini-chat-logo {
  height: 28px;
  width: 28px;
  margin-right: 10px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.8);
  background-color: white;
  padding: 2px;
}

.mini-chat-actions {
  display: flex;
  align-items: center;
}

.mini-chat-actions button {
  position: relative;
}

.mini-files-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background-color: white;
  color: #0B2942;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Files menu */
.mini-files-menu {
  position: absolute;
  top: 50px;
  right: 10px;
  width: 240px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.15);
  color: #333;
  z-index: 200;
  opacity: 0;
  transform: translateY(-10px);
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.mini-files-menu.show {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.mini-files-header {
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
  font-weight: 600;
  color: #0B2942;
  font-size: 0.85rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mini-files-close {
  background: none;
  border: none;
  color: #666;
  font-size: 1rem;
  cursor: pointer;
  padding: 2px;
}

.mini-files-list {
  max-height: 180px;
  overflow-y: auto;
  padding: 5px 0;
}

.mini-file-item {
  padding: 8px 15px;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
  cursor: pointer;
}

.mini-file-item:hover {
  background-color: #f0f7ff;
}

.mini-file-item i:first-child {
  color: #4da0ff;
  font-size: 1rem;
  margin-right: 10px;
}

.mini-file-item i:last-child {
  margin-left: auto;
  color: #666;
  opacity: 0.7;
}

.mini-file-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
  font-size: 0.85rem;
}

.mini-no-files {
  padding: 15px;
  text-align: center;
  color: #666;
  font-style: italic;
  font-size: 0.85rem;
}

.mini-chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  background-color: #f8f9fa;
  background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), 
                    url('@/assets/dut_logo.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 40%;
  background-blend-mode: lighten;
}

.mini-message {
  display: flex;
  margin-bottom: 12px;
  max-width: 90%;
  font-size: 0.9rem;
  opacity: 0;
  transform: translateY(15px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.mini-message.show {
  opacity: 1;
  transform: translateY(0);
}

.mini-message.user-message {
  margin-left: auto;
  flex-direction: row-reverse;
}

.mini-message.bot-message {
  margin-right: auto;
}

.mini-message-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 5px;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.user-message .mini-message-avatar {
  background: linear-gradient(135deg, #0B2942, #1261c3);
  color: white;
  font-size: 14px;
}

.mini-bot-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.mini-message-content {
  padding: 8px 12px;
  border-radius: 15px;
  position: relative;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.user-message .mini-message-content {
  background: linear-gradient(135deg, #0B2942, #1261c3, #4da0ff);
  color: white;
  border-top-right-radius: 3px;
}

.bot-message .mini-message-content {
  background-color: white;
  color: #333;
  border-top-left-radius: 3px;
}

.user-message .mini-message-content::before {
  content: '';
  position: absolute;
  right: -5px;
  top: 0;
  width: 15px;
  height: 15px;
  background: linear-gradient(135deg, #0B2942, #1261c3);
  border-radius: 0 15px 0 0;
  z-index: -1;
}

.bot-message .mini-message-content::before {
  content: '';
  position: absolute;
  left: -5px;
  top: 0;
  width: 15px;
  height: 15px;
  background: white;
  border-radius: 15px 0 0 0;
  z-index: -1;
}

.mini-message-text {
  word-break: break-word;
  line-height: 1.3;
  white-space: pre-wrap;
}

.mini-message-text a {
  color: inherit;
  text-decoration: underline;
}

.internal-link {
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
}

.mini-document-download {
  margin-top: 6px;
}

.mini-document-btn {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(90deg, white, #e6f0ff);
  color: #0B2942;
  border: none;
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 0.8rem;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.user-message .mini-document-btn {
  background: linear-gradient(90deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
}

.mini-document-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.15);
}

.mini-document-btn i {
  margin-right: 5px;
  font-size: 0.9rem;
  color: #4da0ff;
}

.mini-message-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}

.mini-message-button {
  font-size: 0.8rem;
  padding: 3px 8px;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.mini-message-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.mini-bot-typing {
  display: flex;
  margin-bottom: 10px;
  max-width: 90%;
  margin-right: auto;
}

.mini-typing-indicator {
  display: flex;
  align-items: center;
  background-color: white;
  padding: 8px 10px;
  border-radius: 15px;
  border-top-left-radius: 3px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.mini-typing-indicator span {
  display: inline-block;
  width: 6px;
  height: 6px;
  margin: 0 2px;
  background-color: #4da0ff;
  border-radius: 50%;
  animation: typing 1.4s infinite both;
}

.mini-typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.mini-typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

.mini-chat-input {
  padding: 10px;
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

.input-group {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.form-control {
  border-radius: 20px 0 0 20px !important;
  border: 1px solid #4da0ff;
  padding: 8px 12px;
  font-size: 0.9rem;
}

.form-control:focus {
  box-shadow: none;
  border-color: #4da0ff;
}

.btn-primary {
  background: linear-gradient(135deg, #0B2942, #1261c3, #4da0ff);
  border: none;
  border-radius: 0 20px 20px 0 !important;
  padding: 8px 15px;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0B2942, #1261c3);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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

@media (max-width: 576px) {
  .mini-chat-window {
    width: 320px;
    height: 400px;
    right: 5px;
  }

  .chat-toggle-btn {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
    right: 10px;
    bottom: 10px;
  }
  
  .mini-files-menu {
    width: 220px;
    right: 5px;
  }
}
</style>