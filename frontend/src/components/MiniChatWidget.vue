<template>
    <div class="mini-chat-container" v-if="isAuthenticated">
      <!-- Chat toggle button -->
      <button 
        class="chat-toggle-btn" 
        @click="toggleChat" 
        :class="{ 'active': isChatOpen }"
        v-tooltip="isChatOpen ? 'Thu nhỏ' : 'Chat với trợ lý'"
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
            <button @click="resetChat" class="btn btn-sm btn-link text-white">
              <i class="bi bi-arrow-repeat"></i>
            </button>
            <button @click="goToFullChat" class="btn btn-sm btn-link text-white">
              <i class="bi bi-arrows-angle-expand"></i>
            </button>
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
              <div class="mini-message-text" v-html="formatMessage(message.text)"></div>
              
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
      
      // Toggle chat window
      const toggleChat = () => {
        isChatOpen.value = !isChatOpen.value;
        
        if (isChatOpen.value) {
          // Reset unread count when opening
          unreadCount.value = 0;
          
          // Initialize chat if not already
          if (messages.value.length === 0) {
            messages.value = ChatRasaController.initializeChat();
          }
          
          // Give time for DOM to update before scrolling
          nextTick(() => {
            scrollToBottom();
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
        
        // Convert URLs to links
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, url => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);
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
      
      // Watch messages and scroll to bottom when they change
      watch(messages, (newMessages, oldMessages) => {
        nextTick(() => {
          scrollToBottom();
          
          // Increment unread count if chat is closed and we have new bot messages
          if (!isChatOpen.value && oldMessages && newMessages.length > oldMessages.length) {
            const newBotMessages = newMessages.filter(
              (msg, idx) => msg.sender === 'bot' && (idx >= oldMessages.length || msg.id !== oldMessages[idx]?.id)
            );
            unreadCount.value += newBotMessages.length;
          }
        });
      }, { deep: true });
      
      // Load existing chat history when mounted
      onMounted(() => {
        if (isAuthenticated.value) {
          const existingMessages = ChatRasaController.getChatHistory();
          if (existingMessages.length > 0) {
            messages.value = existingMessages;
          }
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
        toggleChat,
        goToFullChat,
        sendMessage,
        formatMessage,
        handleButtonClick,
        resetChat
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
    background-color: #4da0ff;
    color: white;
    border: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
    background-color: #0B2942;
    transform: scale(1.05);
  }
  
  .chat-toggle-btn.active {
    background-color: #dc3545;
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
  }
  
  .mini-chat-window {
    position: absolute;
    bottom: 75px;
    right: 0;
    width: 350px;
    height: 450px;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: all 0.3s ease;
    transform: scale(0);
    transform-origin: bottom right;
    opacity: 0;
    pointer-events: none;
  }
  
  .mini-chat-window.open {
    transform: scale(1);
    opacity: 1;
    pointer-events: all;
  }
  
  .mini-chat-header {
    background-color: #0B2942;
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
    font-size: 0.9rem;
  }
  
  .mini-chat-logo {
    height: 25px;
    width: auto;
    margin-right: 10px;
  }
  
  .mini-chat-actions {
    display: flex;
    align-items: center;
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
  }
  
  .user-message .mini-message-avatar {
    background-color: #4da0ff;
    color: white;
    font-size: 14px;
  }
  
  .mini-bot-avatar {
    width: 24px;
    height: 24px;
  }
  
  .mini-message-content {
    padding: 8px 12px;
    border-radius: 12px;
  }
  
  .user-message .mini-message-content {
    background-color: #4da0ff;
    color: white;
    border-top-right-radius: 4px;
  }
  
  .bot-message .mini-message-content {
    background-color: white;
    color: #333;
    border-top-left-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .mini-message-text {
  word-break: break-word;
  line-height: 1.3;
  white-space: pre-wrap; /* This preserves line breaks */
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
    background-color: #f0f0f0;
    padding: 8px 10px;
    border-radius: 12px;
  }
  
  .mini-typing-indicator span {
    display: inline-block;
    width: 6px;
    height: 6px;
    margin: 0 2px;
    background-color: #888;
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
    background-color: #4da0ff;
    border-color: #4da0ff;
    border-radius: 0 20px 20px 0 !important;
    padding: 8px 15px;
  }
  
  .btn-primary:hover {
    background-color: #0B2942;
    border-color: #0B2942;
  }
  
  @keyframes typing {
    0% { transform: scale(0); opacity: 0.7; }
    50% { transform: scale(1); opacity: 1; }
    100% { transform: scale(0); opacity: 0.7; }
  }
  
  @media (max-width: 576px) {
    .mini-chat-window {
      width: 300px;
      height: 400px;
      right: 10px;
    }
  
    .chat-toggle-btn {
      width: 50px;
      height: 50px;
      font-size: 1.2rem;
      right: 15px;
      bottom: 15px;
    }
  }
  </style>