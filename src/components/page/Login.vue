<script setup>
import { onMounted, ref } from 'vue'

const data = ref()
const inputData = ref()
const connection = new WebSocket('ws://localhost:8000/ws')

function submit() {
	connection.send(inputData.value)
}
onMounted(() => {
	connection.onmessage = function (e) {
		data.value = e.data
	}
})
</script>

<template>
	<div class="ml-[20vw]">
		<h1>hello {{ data }}</h1>
		<input type="text" v-model="inputData" @keyup.enter="submit()" />
		<button @click="submit()">submit</button>
		<RouterView />
	</div>
</template>
