import ChatRasaServices from '@/models/ChatRasaServices';
import store from '@/store';

export default {
  /**
   * Send a message to the Rasa chatbot and process the response
   * @param {string} message - User message text
   * @returns {Promise} - Promise with the processed messages
   */
  async sendMessage(message) {
    try {
      // Get user ID from store
      const userId = store.state.user?.id || 'anonymous';
      
      // Get current chat history
      const chatHistory = ChatRasaServices.getChatHistory(userId);
      
      // Add user message to history
      const userMessage = {
        id: Date.now(),
        text: message,
        sender: 'user',
        timestamp: new Date().toISOString()
      };
      chatHistory.push(userMessage);
      
      // Send message to Rasa
      const response = await ChatRasaServices.sendMessage(message, userId);
      
      // Process bot responses - consolidate multiple messages into one if needed
      if (response && response.length > 0) {
        if (response.length === 1) {
          // Single message response - handle normally
          const botMessage = {
            id: Date.now() + Math.random(),
            text: response[0].text || '',
            sender: 'bot',
            timestamp: new Date().toISOString(),
            buttons: response[0].buttons || [],
            image: response[0].image || null,
            custom: response[0].custom || null
          };
          chatHistory.push(botMessage);
        } else {
          // Multiple messages in one response - consolidate them
          let consolidatedText = '';
          let buttons = [];
          let image = null;
          let custom = null;
          
          // Combine all messages from the response
          response.forEach((msg, index) => {
            // Add the message text, preserving all newlines
            if (msg.text) {
              // Only add separator between messages, not before the first one
              if (consolidatedText !== '') {
                consolidatedText += '\n\n'; // Double newline between separate messages
              }
              
              // Add the message text as is, preserving all original line breaks
              consolidatedText += msg.text;
            }
            
            // Collect any buttons from any part of the response
            if (msg.buttons && msg.buttons.length) {
              buttons = [...buttons, ...msg.buttons];
            }
            
            // Use the first image found (if any)
            if (!image && msg.image) {
              image = msg.image;
            }
            
            // Merge custom data if present
            if (msg.custom) {
              custom = {...custom, ...msg.custom};
            }
          });
          
          // Create a single consolidated message
          const botMessage = {
            id: Date.now() + Math.random(),
            text: consolidatedText,
            sender: 'bot',
            timestamp: new Date().toISOString(),
            buttons: buttons.length > 0 ? buttons : null,
            image: image,
            custom: custom
          };
          chatHistory.push(botMessage);
        }
      } else {
        // Fallback if no response
        chatHistory.push({
          id: Date.now() + Math.random(),
          text: "Sorry, I'm having trouble connecting. Please try again later.",
          sender: 'bot',
          timestamp: new Date().toISOString()
        });
      }
      
      // Save updated history
      ChatRasaServices.saveChatHistory(userId, chatHistory);
      
      // Return the updated message list
      return chatHistory;
    } catch (error) {
      console.error('Error in sendMessage:', error);
      // Return error as a bot message
      const chatHistory = ChatRasaServices.getChatHistory(store.state.user?.id || 'anonymous');
      chatHistory.push({
        id: Date.now(),
        text: "I'm sorry, something went wrong. Please try again later.",
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true
      });
      ChatRasaServices.saveChatHistory(store.state.user?.id || 'anonymous', chatHistory);
      return chatHistory;
    }
  },

  /**
   * Get the current chat history
   * @returns {Array} - Array of message objects
   */
  getChatHistory() {
    const userId = store.state.user?.id || 'anonymous';
    return ChatRasaServices.getChatHistory(userId);
  },

  /**
   * Reset the chat history
   */
  resetChat() {
    const userId = store.state.user?.id || 'anonymous';
    ChatRasaServices.saveChatHistory(userId, []);
    return [];
  },
  
  /**
   * Initialize the chat with a welcome message if history is empty
   * @returns {Array} - Updated chat history
   */
  initializeChat() {
    const userId = store.state.user?.id || 'anonymous';
    let chatHistory = ChatRasaServices.getChatHistory(userId);
    
    if (chatHistory.length === 0) {
      // Add welcome message
      chatHistory = [{
        id: Date.now(),
        text: "Xin chào! Tôi là trợ lý ảo của Đại học Bách khoa Đà Nẵng. Tôi có thể giúp gì cho bạn về thông tin tuyển sinh?",
        sender: 'bot',
        timestamp: new Date().toISOString()
      }];
      ChatRasaServices.saveChatHistory(userId, chatHistory);
    }
    
    return chatHistory;
  }
};