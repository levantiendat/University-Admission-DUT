<template>
  <main class="chat-container" role="main" aria-label="Trợ lý tư vấn tuyển sinh DUT">
    <header class="chat-header">
      <div class="chat-title">
        <img src="/dut_logo.png" alt="Logo Đại học Bách Khoa - Đại học Đà Nẵng" class="chat-logo" width="40" height="40" />
        <div class="title-text">
          <h1>Trợ lý tư vấn tuyển sinh DUT</h1>
          <p class="subtitle">Đại học Bách Khoa - Đại học Đà Nẵng</p>
        </div>
      </div>
      
      <div class="chat-actions">
        <div class="files-dropdown" v-if="downloadableFiles.length > 0">
          <button 
            class="btn btn-sm btn-outline-light files-toggle" 
            @click="toggleFilesMenu"
            aria-expanded="isFilesMenuOpen"
            aria-controls="filesMenu"
            aria-label="Xem tài liệu có thể tải xuống"
          >
            <i class="bi bi-file-earmark-word" aria-hidden="true"></i> 
            <span class="action-text">Tài liệu</span>
            <span class="files-count" aria-label="Số lượng tài liệu">{{ downloadableFiles.length }}</span>
          </button>
          
          <div 
            id="filesMenu"
            class="files-menu" 
            :class="{'show': isFilesMenuOpen}"
            role="menu" 
            aria-labelledby="filesMenuButton"
          >
            <div class="files-header">
              <span>Tài liệu có thể tải xuống</span>
            </div>
            <div class="files-list">
              <button 
                v-for="(file, index) in downloadableFiles" 
                :key="index" 
                class="file-item"
                @click="downloadDocument(file.content, file.filename)"
                role="menuitem"
              >
                <i class="bi bi-file-earmark-word" aria-hidden="true"></i>
                <span class="file-name">{{ file.filename }}</span>
                <i class="bi bi-download" aria-hidden="true"></i>
              </button>
            </div>
          </div>
        </div>
        
        <button 
          @click="resetChat" 
          class="btn btn-sm btn-outline-light"
          aria-label="Bắt đầu cuộc trò chuyện mới"
        >
          <i class="bi bi-arrow-repeat" aria-hidden="true"></i> 
          <span class="action-text">Bắt đầu lại</span>
        </button>
      </div>
    </header>
    
    <section 
      class="chat-messages" 
      ref="messageContainer"
      aria-live="polite"
      aria-relevant="additions"
    >
      <div 
        v-for="message in messages" 
        :key="message.id" 
        :class="['message', message.sender === 'user' ? 'user-message' : 'bot-message']"
        role="listitem"
      >
        <div class="message-avatar" aria-hidden="true">
          <i v-if="message.sender === 'user'" class="bi bi-person-circle"></i>
          <img 
            v-else 
            src="@/assets/dut_logo.jpg" 
            alt="" 
            class="bot-avatar" 
            width="30" 
            height="30" 
          />
        </div>
        
        <div 
          class="message-content"
          :aria-label="message.sender === 'user' ? 'Tin nhắn của bạn' : 'Tin nhắn từ trợ lý tư vấn'"
        >
          <div 
            class="message-text" 
            v-html="formatMessage(message.visibleText || message.text)"
          ></div>
          
          <!-- Document download section if applicable -->
          <div v-if="message.documentContent" class="document-download-section">
            <button 
              @click="downloadDocument(message.documentContent, message.docFilename)" 
              class="document-download-btn"
              aria-label="Tải xuống tài liệu"
            >
              <i class="bi bi-file-earmark-word" aria-hidden="true"></i>
              <span>Tải xuống tài liệu</span>
            </button>
          </div>
          
          <!-- Handle buttons if any -->
          <div v-if="message.buttons && message.buttons.length" class="message-buttons" role="group">
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
            <img 
              :src="message.image" 
              :alt="`Hình ảnh tuyển sinh DUT - ${message.imageAlt || 'Thông tin tuyển sinh'}`" 
              loading="lazy"
              width="300"
              height="auto"
            />
          </div>
          
          <time class="message-time" :datetime="message.timestamp">
            {{ formatTime(message.timestamp) }}
          </time>
        </div>
      </div>
      
      <div v-if="loading" class="bot-typing" aria-live="polite">
        <div class="typing-indicator" aria-label="Trợ lý đang nhập...">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </section>
    
    <footer class="chat-input">
      <form @submit.prevent="sendMessage" aria-label="Form nhập câu hỏi">
        <div class="input-group">
          <input 
            type="text" 
            v-model="newMessage" 
            class="form-control" 
            placeholder="Nhập câu hỏi tuyển sinh tại đây..." 
            :disabled="loading"
            ref="messageInput"
            aria-label="Nhập câu hỏi tuyển sinh"
            autocomplete="off"
            list="chatSuggestions"
          />
          <datalist id="chatSuggestions">
            <option value="Điểm chuẩn năm trước là bao nhiêu?"></option>
            <option value="Ngành học nào có cơ hội việc làm cao?"></option>
            <option value="Khi nào hết hạn đăng ký xét tuyển?"></option>
            <option value="Học phí ngành Công nghệ thông tin?"></option>
            <option value="Thông tin về ký túc xá?"></option>
          </datalist>
          <button 
            class="btn btn-primary" 
            type="submit" 
            :disabled="!newMessage.trim() || loading"
            aria-label="Gửi câu hỏi"
          >
            <i class="bi bi-send-fill" aria-hidden="true"></i>
            <span class="sr-only">Gửi</span>
          </button>
        </div>
      </form>
    </footer>
    
    <div aria-live="assertive" class="sr-only" role="status">
      {{ notificationMessage }}
    </div>
  </main>
</template>

<script>
import { ref, onMounted, nextTick, watch, computed } from 'vue';
import ChatRasaServices from '@/models/ChatRasaServices';
import ChatRasaController from '@/controllers/ChatRasaController';
import { useRouter } from 'vue-router';
import { useHead } from '@vueuse/head'; // You'll need to install @vueuse/head

export default {
  name: 'ChatRasaView',
  
  setup() {
    // SEO Setup using @vueuse/head
    useHead({
      title: 'Trợ lý tư vấn tuyển sinh DUT - Đại học Bách Khoa Đà Nẵng',
      meta: [
        { name: 'description', content: 'Trò chuyện với trợ lý ảo để nhận thông tin tuyển sinh đại học Bách Khoa Đà Nẵng. Hỗ trợ 24/7 về điểm chuẩn, ngành học, đăng ký xét tuyển.' },
        { name: 'keywords', content: 'tư vấn tuyển sinh, đại học Bách Khoa Đà Nẵng, DUT, chatbot tuyển sinh, trợ lý ảo DUT' },
        { name: 'author', content: 'Đại học Bách Khoa - Đại học Đà Nẵng' },
        { property: 'og:title', content: 'Trợ lý tư vấn tuyển sinh DUT' },
        { property: 'og:description', content: 'Trò chuyện với trợ lý ảo để nhận thông tin tuyển sinh đại học Bách Khoa Đà Nẵng.' },
        { property: 'og:type', content: 'website' }
      ],
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Trợ lý tư vấn tuyển sinh DUT",
            "description": "Trò chuyện với trợ lý ảo để nhận thông tin tuyển sinh Đại học Bách Khoa Đà Nẵng",
            "applicationCategory": "EducationalApplication",
            "operatingSystem": "Web",
            "offers": {
              "@type": "Offer",
              "price": "0"
            }
          })
        }
      ]
    });

    const router = useRouter();
    const messages = ref([]);
    const newMessage = ref('');
    const loading = ref(false);
    const messageContainer = ref(null);
    const messageInput = ref(null);
    const isFilesMenuOpen = ref(false);
    const notificationMessage = ref(''); // For screen reader announcements
    
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
    
    // Close files menu when clicking outside and keyboard navigation
    onMounted(() => {
      document.addEventListener('click', (event) => {
        const filesDropdown = document.querySelector('.files-dropdown');
        if (isFilesMenuOpen.value && filesDropdown && !filesDropdown.contains(event.target)) {
          isFilesMenuOpen.value = false;
        }
      });
      
      // Add keyboard support for escape key to close menu
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && isFilesMenuOpen.value) {
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
      
      // Notify screen readers that chat has initialized
      notificationMessage.value = 'Trợ lý tư vấn tuyển sinh đã sẵn sàng. Hãy nhập câu hỏi của bạn.';
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
          
          // Announce new message for screen readers if it's from the bot
          const latestMessage = newVal[newVal.length - 1];
          if (latestMessage && latestMessage.sender !== 'user') {
            notificationMessage.value = 'Trợ lý đã trả lời: ' + 
              (latestMessage.visibleText || latestMessage.text || '').substring(0, 100) + 
              (latestMessage.visibleText && latestMessage.visibleText.length > 100 ? '...' : '');
          }
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
        return `<a href="javascript:void(0)" onclick="window.dispatchEvent(new CustomEvent('navigate-to', {detail: '${encodedPath}'}))" class="internal-link special-link" role="button">Tại đây</a>`;
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
        const internalLinkRegex = /(\s|^)(\/[a-zA-Z0-9\/\-_]+(?:\?[a-zA-Z0-9\/\-_&=%ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêế...]*))/g;
        
        return text.replace(internalLinkRegex, (match, before, path) => {
          // Mã hóa URL để xử lý đúng các ký tự đặc biệt và dấu tiếng Việt
          const encodedPath = encodeURI(path);
          return `${before}<a href="javascript:void(0)" onclick="window.dispatchEvent(new CustomEvent('navigate-to', {detail: '${encodedPath}'}))" class="internal-link" role="button">Tại đây</a>`;
        });
      }
    };
    
    // Download a document
    const downloadDocument = (content, filename) => {
      ChatRasaServices.createAndDownloadDocument(content, filename);
      // Close files menu if open
      isFilesMenuOpen.value = false;
      
      // Notify screen readers
      notificationMessage.value = `Đang tải xuống tài liệu ${filename}`;
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
      notificationMessage.value = 'Đang gửi tin nhắn...';
      
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
        notificationMessage.value = 'Có lỗi xảy ra khi gửi tin nhắn. Vui lòng thử lại sau.';
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
        notificationMessage.value = 'Cuộc trò chuyện đã được làm mới';
        
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
      
      // Detect and handle mobile devices better
      const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
      if (isMobile) {
        document.body.classList.add('mobile-device');
      }
    });
    
    return {
      messages,
      newMessage,
      loading,
      messageContainer,
      messageInput,
      downloadableFiles,
      isFilesMenuOpen,
      notificationMessage,
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

<style>
/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

/* Root-level CSS variables for consistent styling */
:root {
  --primary-color: #0B2942;
  --secondary-color: #1261c3;
  --accent-color: #4da0ff;
  --text-dark: #1a1a1a;
  --text-light: #ffffff;
  --background-light: #f8f9fa;
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 16px;
  --border-color: rgba(0,0,0,0.1);
  --shadow-sm: 0 2px 5px rgba(0,0,0,0.05);
  --shadow-md: 0 3px 8px rgba(0,0,0,0.1);
  --shadow-lg: 0 5px 15px rgba(0,0,0,0.1);
  --transition-speed: 0.3s;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--background-light);
  border-radius: 0;
  box-shadow: var(--shadow-md);
  overflow: hidden;
  position: relative;
  max-width: 100%;
  margin: 0 auto;
}

@media (min-width: 1200px) {
  .chat-container {
    max-width: 1140px;
    height: 85vh;
    margin: 2rem auto;
    border-radius: var(--border-radius-md);
  }
}

.chat-header {
  background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 70%, var(--accent-color) 100%);
  color: var(--text-light);
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
  box-shadow: var(--shadow-sm);
}

.chat-title {
  display: flex;
  align-items: center;
}

.title-text {
  background: linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.9) 70%, rgba(255,255,255,0.7) 100%);
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
  object-fit: contain;
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
  transition: all var(--transition-speed) ease;
}

.files-toggle:hover, .files-toggle:focus {
  background-color: rgba(255,255,255,0.15);
  transform: translateY(-1px);
  border-color: rgba(255,255,255,0.9);
  outline: none;
}

.files-toggle:focus-visible {
  outline: 2px solid rgba(255,255,255,0.5);
  outline-offset: 2px;
}

.files-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  color: var(--primary-color);
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
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  color: var(--text-dark);
  z-index: 100;
  opacity: 0;
  transform: translateY(-5px);
  pointer-events: none;
  transition: all var(--transition-speed) cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 1px solid var(--border-color);
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
  color: var(--primary-color);
  font-size: 0.85rem;
}

.files-list {
  max-height: 250px;
  overflow-y: auto;
  padding: 4px 0;
}

.file-item {
  width: 100%;
  text-align: left;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  transition: all 0.15s;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
  background: none;
  border: none;
  outline: none;
  color: var(--text-dark);
}

.file-item:last-child {
  border-bottom: none;
}

.file-item:hover, .file-item:focus {
  background-color: #f0f7ff;
  transform: translateY(-1px);
  outline: none;
}

.file-item:focus-visible {
  outline: 2px solid var(--accent-color);
}

.file-item i:first-child {
  color: var(--accent-color);
  font-size: 1.1rem;
  margin-right: 10px;
}

.file-item i:last-child {
  margin-left: auto;
  color: #666;
  opacity: 0;
  transition: all var(--transition-speed);
}

.file-item:hover i:last-child, .file-item:focus i:last-child {
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
  padding: 20px 3vw;
  background-color: var(--background-light);
  background-image: linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)), 
                    url('@/assets/dut_logo.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 25%;
  background-blend-mode: lighten;
  background-attachment: fixed;
  scroll-behavior: smooth;
}

.message {
  display: flex;
  margin-bottom: 24px;
  max-width: 70%;
  align-items: flex-start;
  opacity: 0;
  transform: translateY(15px);
  transition: opacity var(--transition-speed) ease, transform var(--transition-speed) ease;
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
  box-shadow: var(--shadow-sm);
}

.user-message .message-avatar {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: var(--text-light);
  font-size: 18px;
}

.bot-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1.5px solid white;
  object-fit: cover;
}

.message-content {
  padding: 14px 18px;
  border-radius: var(--border-radius-lg);
  position: relative;
  box-shadow: var(--shadow-sm);
  font-size: 0.95rem;
  line-height: 1.5;
  word-break: break-word;
}

.user-message .message-content {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
  color: var(--text-light);
  border-top-right-radius: var(--border-radius-sm);
}

.bot-message .message-content {
  background-color: white;
  color: var(--text-dark);
  border-top-left-radius: var(--border-radius-sm);
}

.user-message .message-content::before {
  content: '';
  position: absolute;
  right: -8px;
  top: 0;
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
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
  color: var(--primary-color);
  border: none;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-speed) ease;
  outline: none;
}

.user-message .document-download-btn {
  background: linear-gradient(90deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
}

.document-download-btn:hover, .document-download-btn:focus {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  outline: none;
}

.document-download-btn:focus-visible {
  outline: 2px solid var(--accent-color);
}

.document-download-btn i {
  margin-right: 8px;
  font-size: 1.1rem;
  color: var(--accent-color);
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
  color: var(--accent-color);
  border-color: var(--accent-color);
  transition: all var(--transition-speed) ease;
  border-radius: 15px;
  font-size: 0.85rem;
  padding: 4px 12px;
  outline: none;
}

.message-button:hover, .message-button:focus {
  background-color: var(--accent-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  outline: none;
}

.message-button:focus-visible {
  outline: 2px solid var(--accent-color);
  outline-offset: 2px;
}

.message-image img {
  max-width: 100%;
  border-radius: var(--border-radius-md);
  margin-top: 10px;
  box-shadow: var(--shadow-sm);
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
  padding: 15px 3vw;
  background-color: var(--background-light);
  border-top: 1px solid var(--border-color);
  margin-top: auto;
}

.input-group {
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  background-color: white;
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
}

.form-control {
  border-radius: var(--border-radius-md) 0 0 var(--border-radius-md) !important;
  border: 1px solid #e0e0e0;
  padding: 12px 16px;
  font-size: 0.95rem;
  height: auto;
  background-color: white;
  flex-grow: 1;
}

.form-control:focus {
  box-shadow: none;
  border-color: var(--accent-color);
  outline: none;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
  border: none;
  border-radius: 0 var(--border-radius-md) var(--border-radius-md) 0 !important;
  padding: 0 16px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 50px;
}

.btn-primary:hover, .btn-primary:not(:disabled):active {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  box-shadow: var(--shadow-sm);
}

.btn-primary:focus {
  box-shadow: none;
  outline: none;
}

.btn-primary:focus-visible {
  outline: 2px solid var(--accent-color);
  outline-offset: -1px;
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
  border-radius: var(--border-radius-lg);
  border-top-left-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-sm);
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
  background-color: var(--accent-color);
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

/* Improve touch interactions on mobile */
@media (pointer: coarse) {
  .message-button, .document-download-btn, .files-toggle, .btn {
    min-height: 38px; /* Ensure touch targets are at least 44px */
    min-width: 38px;
  }
}

/* Focus indicators for better keyboard navigation */
button:focus-visible, a:focus-visible, input:focus-visible {
  outline: 2px solid var(--accent-color);
  outline-offset: 2px;
}

@keyframes typing {
  0% { transform: scale(0); opacity: 0.7; }
  50% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0); opacity: 0.7; }
}

/* Custom Scrollbar */
.chat-messages::-webkit-scrollbar,
.files-list::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track,
.files-list::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.05);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb,
.files-list::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.1);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover,
.files-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0,0,0,0.2);
}

/* Enhanced Responsive Styles */
@media (max-width: 991px) {
  .message {
    max-width: 75%;
  }
  
  .chat-header {
    padding: 10px 15px;
  }
}

@media (max-width: 768px) {
  .chat-container {
    border-radius: 0;
    height: 100vh;
    margin: 0;
    max-width: 100%;
  }
  
  .message {
    max-width: 85%;
  }
  
  .chat-logo {
    height: 35px;
    width: 35px;
  }
  
  .title-text h1 {
    font-size: 1.1rem;
  }
  
  .action-text {
    display: none;
  }
  
  .files-menu {
    width: 220px;
    right: -70px;
  }
  
  .files-menu::before {
    right: 85px;
  }
  
  .input-group {
    flex-wrap: nowrap;
  }
}

@media (max-width: 576px) {
  .chat-header {
    padding: 10px 12px;
  }
  
  .message {
    max-width: 90%;
  }
  
  .chat-messages {
    padding: 15px 2vw;
  }
  
  .chat-input {
    padding: 10px 2vw;
  }
  
  .message-content {
    padding: 12px 15px;
  }
  
  .form-control {
    padding: 10px 15px;
  }
  
  .message-buttons {
    flex-direction: column;
    gap: 6px;
    align-items: flex-start;
  }
  
  .message-button {
    width: 100%;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .chat-container {
    background-color: #1a1a1a;
  }
  
  .chat-messages {
    background-color: #1a1a1a;
    background-image: linear-gradient(rgba(26,26,26,0.9), rgba(26,26,26,0.9)), 
                      url('@/assets/dut_logo.jpg');
  }
  
  .chat-input {
    background-color: #1a1a1a;
  }
  
  .bot-message .message-content {
    background-color: #2a2a2a;
    color: #e0e0e0;
  }
  
  .bot-message .message-content::before {
    background-color: #2a2a2a;
  }
  
  .typing-indicator, .typing-indicator::before {
    background-color: #2a2a2a;
  }
  
  .files-menu, .files-menu::before {
    background-color: #2a2a2a;
    color: #e0e0e0;
  }
  
  .files-header {
    border-bottom-color: #3a3a3a;
  }
  
  .file-item {
    border-bottom-color: #3a3a3a;
    color: #e0e0e0;
  }
  
  .file-item:hover {
    background-color: #3a3a3a;
  }
  
  .input-group {
    background-color: #2a2a2a;
  }
  
  .form-control {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border-color: #3a3a3a;
  }
  
  .document-download-btn {
    background: linear-gradient(90deg, #2a2a2a, #3a3a3a);
    color: #e0e0e0;
  }
}
</style>