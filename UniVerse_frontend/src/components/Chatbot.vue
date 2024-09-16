<template>
  <div class="flex flex-col h-full bg-gray-50 dark:bg-gray-900">
    <div class="bg-purple-600 dark:bg-purple-800 p-4 flex justify-between items-center">
      <h2 class="text-xl font-bold text-white">Chatbot</h2>
      <button @click="$emit('close')" class="text-white hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 rounded-full p-1">
        <XIcon class="h-6 w-6" />
      </button>
    </div>
    <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messageContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['flex', message.isUser ? 'justify-end' : 'justify-start']">
        <div :class="['max-w-[80%] sm:max-w-[70%] md:max-w-[60%] rounded-lg p-3 shadow-md', 
                      message.isUser ? 'bg-purple-500 text-white' : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200']">
          {{ message.text }}
        </div>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="border-t border-gray-200 dark:border-gray-700 p-4 flex">
      <input 
        v-model="userInput" 
        type="text" 
        placeholder="Type your message..."
        class="flex-1 border border-gray-300 dark:border-gray-600 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-white"
      />
      <button 
        type="submit"
        class="bg-purple-500 text-white px-4 py-2 rounded-r-lg hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 transition duration-150 ease-in-out flex items-center justify-center"
      >
        <SendIcon class="h-5 w-5" />
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import axios from 'axios';
import { SendIcon, XIcon } from 'lucide-vue-next';

const messages = ref([
  { text: "Hello! How can I assist you today?", isUser: false },
]);
const userInput = ref('');
const messageContainer = ref(null);

const sendMessage = async () => {
  if (userInput.value.trim() === '') return;

  messages.value.push({ text: userInput.value, isUser: true });

  const userMessage = userInput.value;
  userInput.value = '';

  try {
    const response = await axios.post(
      'http://localhost:8000/api/chatbot/', 
      { message: userMessage }
    );
    const botReply = response.data.response;

    messages.value.push({ text: botReply, isUser: false });
  } catch (error) {
    console.error('Error fetching bot reply:', error);
    messages.value.push({ text: "Error: Unable to fetch response from server.", isUser: false });
  }
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
};

watch(messages, scrollToBottom, { deep: true });

onMounted(scrollToBottom);
</script>

<style scoped>
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.flex-1 > div {
  animation: fadeIn 0.3s ease-out;
}
</style>