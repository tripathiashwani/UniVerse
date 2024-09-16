<template>
  <div class="container mx-auto">
    <h1 class="text-2xl font-bold mb-4">Chat Room</h1>
    <div v-for="message in received_data" :key="message.id" class="mb-2">
      <span class="font-bold">{{ message.sender.name }}:</span> {{ message.message }}
    </div>
    <div v-for="message in messages" :key="message.id" class="mb-2">
      <span class="font-bold">{{ message.message.sender }}:</span> {{ message.message.message  }}
    </div>
    <input v-model="newMessage" placeholder="Type a message" class="border border-gray-300 rounded px-2 py-1 mb-2" />
    <button @click="sendMessage" class="bg-blue-500 text-white px-4 py-2 rounded">Send</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
// import { useQuery, gql } from '@apollo/client';
import axios from 'axios';
// const GET_CONVERSATION = gql`
//   query getConversation($room: String!) {
//     conversation(room: $room) {
//       messages {
//         id
//         message
//         sender {
//           name
//           avatar
//         }
//         createdAt
//       }
//     }
//   }
// `;

export default {
  name: 'ChatView',
  props: {
    roomID: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const userStore = useUserStore();
    const messages = ref([]);
    const received_data = ref([]);
    const newMessage = ref('');
    let socket = null;


    const connectToWebSocket = () => {
      const wsPath = `ws://127.0.0.1:8000/ws/chat/${props.roomID}/`;
      socket = new WebSocket(wsPath);

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received data:', data); 
          
          messages.value.push(data);
        
      };

      socket.onclose = () => {
        console.log('WebSocket closed unexpectedly');
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    };

    const sendMessage = () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        const roomIDParts = props.roomID.split('_');
        const recipientID = roomIDParts.find(id => id !== userStore.user.id); // Assuming the roomID format "user1_user2"
        const messageData = {
          message: newMessage.value,
          sender: userStore.user.email,  // Use email or ID as identifier
          sent_to: recipientID
        };
        console.log('Sending message:', messageData);
        socket.send(JSON.stringify(messageData));
        newMessage.value = '';
      } else {
        console.error('WebSocket is not connected');
      }
    };

    onMounted(() => {
      connectToWebSocket();
      getchats();
      // result.value?.conversation?.messages.forEach(msg => messages.value.push(msg));
    });

    const getchats = () => {
      axios
        .get(`/api/chats/get_room_chat/${props.roomID}/`)
        .then(response => {
          console.log('data of chat', response.data);
          
          if (response.data && response.data.messages) {
            received_data.value = response.data.messages;
          } else {
            console.error('Received messages data is not in expected format');
          }
        })
        .catch(error => {
          console.log('error', error);
        });
    };

    return {
      messages,
      newMessage,
      sendMessage,
      received_data
    };
  }
};
</script> 



<!-- 
<template>
  <div class="container mx-auto">
    <h1 class="text-2xl font-bold mb-4">Chat Room</h1>
    <div v-for="message in received_data" :key="message.id" class="mb-2">
      <span class="font-bold">{{ message.sender.name }}:</span> {{ message.message }}
    </div>
    <div v-for="message in messages" :key="message.id" class="mb-2">
      <span class="font-bold">{{ message.sender.name }}:</span> {{ message.message }}
    </div>
    <input v-model="newMessage" placeholder="Type a message" class="border border-gray-300 rounded px-2 py-1 mb-2" />
    <button @click="sendMessage" class="bg-blue-500 text-white px-4 py-2 rounded">Send</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useQuery, gql } from '@vue/apollo-composable';
import axios from 'axios';

const GET_CONVERSATION = gql`
  query getConversation($room: String!) {
    conversation(room: $room) {
      messages {
        id
        message
        sender {
          name
          avatar
        }
        createdAt
      }
    }
  }
`;

export default {
  name: 'ChatView',
  props: {
    roomID: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const userStore = useUserStore();
    const messages = ref([]);
    const received_data = ref([]);
    const newMessage = ref('');
    let socket = null;

    const { result, loading, error } = useQuery(GET_CONVERSATION, {
      room: props.roomID,
    });

    watchEffect(() => {
      if (result.value && result.value.conversation) {
        received_data.value = result.value.conversation.messages;
      }
    });

    const connectToWebSocket = () => {
      const wsPath = `ws://127.0.0.1:8000/ws/chat/${props.roomID}/`;
      socket = new WebSocket(wsPath);

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received data:', data);
        messages.value.push(data);
      };

      socket.onclose = () => {
        console.log('WebSocket closed unexpectedly');
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    };

    const sendMessage = () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        const roomIDParts = props.roomID.split('_');
        const recipientID = roomIDParts.find(id => id !== userStore.user.id);
        const messageData = {
          message: newMessage.value,
          sender: userStore.user.email,
          sent_to: recipientID
        };
        console.log('Sending message:', messageData);
        socket.send(JSON.stringify(messageData));
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
      received_data,
      loading,
      error,
    };
  }
};
</script> -->
