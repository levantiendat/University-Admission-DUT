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
      const userId = store.state.user?.email || 'anonymous';
      
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
          const processedContent = ChatRasaServices.processMessageContent(response[0].text || '');
          
          const botMessage = {
            id: Date.now() + Math.random(),
            text: response[0].text || '',
            sender: 'bot',
            timestamp: new Date().toISOString(),
            buttons: response[0].buttons || [],
            image: response[0].image || null,
            custom: response[0].custom || null,
            visibleText: processedContent.visibleText,
            documentContent: processedContent.documentContent,
            docFilename: processedContent.docFilename
          };
          chatHistory.push(botMessage);
        } else {
          // Multiple messages in one response - consolidate them
          let consolidatedText = '';
          let buttons = [];
          let image = null;
          let custom = null;
          let hasDocument = false;
          let documentContent = null;
          let documentVisibleText = '';
          let docFilename = null;
          
          // Check if any message contains a document
          for (const msg of response) {
            if (msg.text && msg.text.includes('<document>')) {
              hasDocument = true;
              const processedContent = ChatRasaServices.processMessageContent(msg.text || '');
              documentContent = processedContent.documentContent;
              documentVisibleText = processedContent.visibleText;
              docFilename = processedContent.docFilename;
              break;
            }
          }
          
          if (hasDocument) {
            // If there's a document, use the processed document message
            const botMessage = {
              id: Date.now() + Math.random(),
              text: documentVisibleText + '<document>' + documentContent,
              sender: 'bot',
              timestamp: new Date().toISOString(),
              buttons: buttons.length > 0 ? buttons : null,
              image: image,
              custom: custom,
              visibleText: documentVisibleText,
              documentContent: documentContent,
              docFilename: docFilename
            };
            chatHistory.push(botMessage);
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
      const chatHistory = ChatRasaServices.getChatHistory(store.state.user?.email || 'anonymous');
      chatHistory.push({
        id: Date.now(),
        text: "I'm sorry, something went wrong. Please try again later.",
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true,
        visibleText: "I'm sorry, something went wrong. Please try again later."
      });
      ChatRasaServices.saveChatHistory(store.state.user?.email || 'anonymous', chatHistory);
      return chatHistory;
    }
  },

  /**
   * Get the current chat history
   * @returns {Array} - Array of message objects
   */
  getChatHistory() {
    const userId = store.state.user?.email || 'anonymous';
    const chatHistory = ChatRasaServices.getChatHistory(userId);
    
    // Process any existing messages to ensure they have visibleText property
    return chatHistory.map(message => {
      if (message.sender === 'bot' && message.text && !message.visibleText) {
        const processedContent = ChatRasaServices.processMessageContent(message.text);
        return {
          ...message,
          visibleText: processedContent.visibleText,
          documentContent: processedContent.documentContent,
          docFilename: processedContent.docFilename
        };
      }
      return message.visibleText ? message : { ...message, visibleText: message.text };
    });
  },

  /**
   * Reset the chat history
   */
  resetChat() {
    const userId = store.state.user?.email || 'anonymous';
    ChatRasaServices.saveChatHistory(userId, []);
    return [];
  },
  
  /**
   * Initialize the chat with a welcome message if history is empty
   * @returns {Array} - Updated chat history
   */
  initializeChat() {
    const userId = store.state.user?.email || 'anonymous';
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