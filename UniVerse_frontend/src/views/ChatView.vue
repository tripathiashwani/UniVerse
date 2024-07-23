<template>
    <div class="container mx-auto">
        <h1 class="text-2xl font-bold mb-4">Chat Room</h1>
        <div v-for="message in messages" :key="message.id" class="mb-2">
            <span class="font-bold">{{ message.sender }}:</span> {{ message.message }}
        </div>
        <input v-model="newMessage" placeholder="Type a message" class="border border-gray-300 rounded px-2 py-1 mb-2" />
        <button @click="sendMessage" class="bg-blue-500 text-white px-4 py-2 rounded">Send</button>
    </div>
</template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useUserStore } from '@/stores/user';
  
  export default {
    name: 'ChatView',
    props: {
      roomID: {
        type: String,
        required: true
      }
    },
    setup(props) {
      const userStore = useUserStore()
      const messages = ref([]);
      const sender = ref('');
      const newMessage = ref('');  
      let socket = null;
  
      const connectToWebSocket = () => {
        const wsPath = `ws://127.0.0.1:8000/ws/chat/${props.roomID}/`;
        socket = new WebSocket(wsPath);
  
        socket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          messages.value.push(data);
          
        };
        console.log(messages)
        socket.onclose = () => {
          console.log('WebSocket closed unexpectedly');
        };
  
        socket.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
      };
  
      const sendMessage = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
          const message = {
            message: newMessage.value,
            sender: userStore.name, // replace with actual sender info if available
          };
          socket.send(JSON.stringify(message));
          newMessage.value = '';
        } else {
          console.error('WebSocket is not connected');
        }
      };
  
      onMounted(() => {
        connectToWebSocket();
      });
  
      return {
        messages,
        newMessage,
        sendMessage,
      };
    }
  };
  </script>
  