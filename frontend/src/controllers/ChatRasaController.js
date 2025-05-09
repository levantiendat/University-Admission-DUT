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
        timestamp: new Date().toISOString(),
        visibleText: message
      };
      chatHistory.push(userMessage);
      
      // Send message to Rasa
      const response = await ChatRasaServices.sendMessage(message, userId);
      
      // Process bot responses - consolidate multiple messages into one if needed
      if (response && response.length > 0) {
        if (response.length === 1) {
          // Single message response - handle normally
          const processedMessage = this.processMessageContent(response[0].text || '');
          
          const botMessage = {
            id: Date.now() + Math.random(),
            text: response[0].text || '',
            sender: 'bot',
            timestamp: new Date().toISOString(),
            buttons: response[0].buttons || [],
            image: response[0].image || null,
            custom: response[0].custom || null,
            visibleText: processedMessage.visibleText,
            documentContent: processedMessage.documentContent,
            docFilename: processedMessage.documentContent ? `data_${Date.now()}.docx` : null
          };
          chatHistory.push(botMessage);
        } else {
          // Multiple messages in one response - consolidate them
          let consolidatedText = '';
          let buttons = [];
          let image = null;
          let custom = null;
          let hasDocument = false;
          
          // Check if any message contains a document
          for (const msg of response) {
            if (msg.text && msg.text.includes('<document>')) {
              hasDocument = true;
              break;
            }
          }
          
          if (hasDocument) {
            // If there's a document, only use that message
            for (const msg of response) {
              if (msg.text && msg.text.includes('<document>')) {
                const processedMessage = this.processMessageContent(msg.text);
                
                const botMessage = {
                  id: Date.now() + Math.random(),
                  text: msg.text,
                  sender: 'bot',
                  timestamp: new Date().toISOString(),
                  buttons: msg.buttons || [],
                  image: msg.image || null,
                  custom: msg.custom || null,
                  visibleText: processedMessage.visibleText,
                  documentContent: processedMessage.documentContent,
                  docFilename: processedMessage.documentContent ? `data_${Date.now()}.docx` : null
                };
                chatHistory.push(botMessage);
                break;
              }
            }
          } else {
            // No document, combine messages as before
            response.forEach((msg) => {
              if (msg.text) {
                if (consolidatedText !== '') {
                  consolidatedText += '\n\n';
                }
                consolidatedText += msg.text;
              }
              
              if (msg.buttons && msg.buttons.length) {
                buttons = [...buttons, ...msg.buttons];
              }
              
              if (!image && msg.image) {
                image = msg.image;
              }
              
              if (msg.custom) {
                custom = {...custom, ...msg.custom};
              }
            });
            
            const botMessage = {
              id: Date.now() + Math.random(),
              text: consolidatedText,
              sender: 'bot',
              timestamp: new Date().toISOString(),
              buttons: buttons.length > 0 ? buttons : null,
              image: image,
              custom: custom,
              visibleText: consolidatedText
            };
            chatHistory.push(botMessage);
          }
        }
      } else {
        // Fallback if no response
        chatHistory.push({
          id: Date.now() + Math.random(),
          text: "Sorry, I'm having trouble connecting. Please try again later.",
          sender: 'bot',
          timestamp: new Date().toISOString(),
          visibleText: "Sorry, I'm having trouble connecting. Please try again later."
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
        isError: true,
        visibleText: "I'm sorry, something went wrong. Please try again later."
      });
      ChatRasaServices.saveChatHistory(store.state.user?.id || 'anonymous', chatHistory);
      return chatHistory;
    }
  },

  /**
   * Process message content to separate visible text from document content
   * @param {string} messageText - Original message text
   * @returns {Object} - Object with visibleText and documentContent
   */
  processMessageContent(messageText) {
    if (!messageText) {
      return { visibleText: '', documentContent: null };
    }
    
    // Check if message contains <document> tag
    const documentTagIndex = messageText.indexOf('<document>');
    if (documentTagIndex === -1) {
      return { visibleText: messageText, documentContent: null };
    }
    
    // Split the message into visible text and document content
    const visibleText = messageText.substring(0, documentTagIndex).trim();
    const documentContent = messageText.substring(documentTagIndex + 10).trim(); // +10 to skip '<document>' tag
    
    return { visibleText, documentContent };
  },

  /**
   * Get the current chat history
   * @returns {Array} - Array of message objects
   */
  getChatHistory() {
    const userId = store.state.user?.id || 'anonymous';
    const chatHistory = ChatRasaServices.getChatHistory(userId);
    
    // Process any existing messages to ensure they have visibleText property
    return chatHistory.map(message => {
      if (message.sender === 'bot' && !message.visibleText) {
        const processedMessage = this.processMessageContent(message.text || '');
        return {
          ...message,
          visibleText: processedMessage.visibleText,
          documentContent: processedMessage.documentContent,
          docFilename: processedMessage.documentContent ? `data_${Date.now()}.docx` : null
        };
      }
      return message.visibleText ? message : { ...message, visibleText: message.text };
    });
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
        text: "Xin chào! Tôi là trợ lý ảo của Trường Đại học Bách Khoa - Đại Học Đà Nẵng. Tôi có thể giúp gì cho bạn về thông tin tuyển sinh?",
        sender: 'bot',
        timestamp: new Date().toISOString(),
        visibleText: "Xin chào! Tôi là trợ lý ảo của Trường Đại học Bách Khoa - Đại Học Đà Nẵng. Tôi có thể giúp gì cho bạn về thông tin tuyển sinh?"
      }];
      ChatRasaServices.saveChatHistory(userId, chatHistory);
    }
    
    return this.getChatHistory();
  }
};