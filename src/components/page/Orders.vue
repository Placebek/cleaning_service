<script setup>
import { ref, computed, onMounted } from 'vue';
import OrderApplications from '../UI/element/OrderApplications.vue';

const product = ref([]);
const isLoading = ref(true);
const tokenData = JSON.parse(localStorage.getItem('user'))?.access_token;
const headers = { 'Authorization': 'Bearer ' + tokenData };
let websocket = null;

const orders = ref([]);

const setupWebSocket = () => {
  websocket = new WebSocket('ws://localhost:8000/auth/admin/ws');

  websocket.onmessage = event => {
    const data = JSON.parse(event.data);
    product.value = data; 
  };
  websocket.onclose = () => {
    setTimeout(setupWebSocket, 1000); 
  };
  websocket.onerror = error => {
    console.error('WebSocket error:', error);
  };
};


onMounted(async () => {
  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:8000/auth/admin/orders', { headers });
    const data = await response.json();
    product.value = data; 
    
  } catch (error) {
    console.error('Error fetching data:', error);
  } finally {
    isLoading.value = false
  }

  setupWebSocket()
});

const filteredProducts = computed(() => {
  return Array.isArray(product.value)
    ? product.value.filter(post => post.request_id !== null)
    : []
});

</script>

<template>
  <div class="ml-[15vw] mt-[5vh]">
    <h1 class="text-[1.4vw] font-medium">Список заявок:</h1>
    <div v-if="isLoading" class="absolute -translate-x-1/2 left-1/2 mt-8">
      <div class="animate-spin rounded-full h-16 w-16 border-t-[3px] border-green-500"></div>
    </div>
    <div v-else>
      <template v-if="filteredProducts.length > 0">
        <div v-for="post in filteredProducts" :key="post.id">
          <OrderApplications :articledata="post" />
        </div>
      </template>
      <p v-else class="text-[2vw] font-semibold absolute -translate-x-1/2 left-1/2 mt-8">Заявок нет</p>
    </div>
  </div>
</template>
