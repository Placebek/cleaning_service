import { ref, onMounted, onBeforeUnmount } from 'vue'

export default function useWebSocket(url) {
	const wss = ref()
	const orders = ref()
    const ws = new WebSocket(url)

	onMounted(() => {
        ws.onopen = () => {
			console.log('WebSocket connect')

        };
        
        ws.onmessage = (event) => {
					const message = JSON.parse(event.data)
                    debugger
                    orders.value.pusdata
				}

		ws.onclose = () => {
			console.log('WebSocket connection closed')
		}
	})

	onBeforeUnmount(() => {
		ws.close()
	})

	return {
		wss,
		orders,
	}
}
