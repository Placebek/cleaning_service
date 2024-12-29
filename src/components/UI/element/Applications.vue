<script setup>
import Accordion from 'primevue/accordion'
import AccordionPanel from 'primevue/accordionpanel'
import AccordionHeader from 'primevue/accordionheader'
import AccordionContent from 'primevue/accordioncontent'
import Dialog from 'primevue/dialog'
import { ref } from 'vue'
import { Clipboard } from 'v-clipboard'
import WorkerTable from './WorkerTable.vue'
import { store } from '@/stores/states'


const product = ref(null)
var tokenData = JSON.parse(localStorage.getItem('user'))['access_token']
const headers = {
	Authorization: 'Bearer ' + tokenData,
}
fetch('http://localhost:8000/auth/admin/workers', { headers })
	.then(response => response.json())
	.then(data => (product.value = data))

const visible = ref(false)
const visibleDeleteDialog = ref(false)
</script>

<script>
export default {
	props: ['articledata'],
	data() {
		return {
			articleData: this.articledata,
		}
	},

	methods: {
		requestToOrder(request_id) {
			const request = ref(null)
			var tokenData = JSON.parse(localStorage.getItem('user'))['access_token']
			const requestOptions = {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + tokenData,
				},
				body: JSON.stringify({
					worker_id: store.worker_id,
					request_id: request_id,
				}),
			}


			fetch('http://localhost:8000/auth/admin/requests', requestOptions)
				.then(response => response.json())
				.then(data => (request.value = data))
		},

		deleteRequest(request_id) {
			const response = ref(null)
			var tokenData = JSON.parse(localStorage.getItem('user'))['access_token']
			const requestOptions = {
				method: 'DELETE',
				headers: {
					'Authorization': 'Bearer ' + tokenData,
				},
			}
			fetch(
				`http://localhost:8000/auth/admin/request/${request_id}`,
				requestOptions
			)
				.then(response => response.json())
				.then(data => (response.value = data))
		},

		success() {
			alert('Успешно скопировано')
		},
		copy() {
			Clipboard.copy('TEST')
		},
	},
}
</script>

<template>
	<div class="flex flex-row gap-2 mt-3">
		<div class="w-[60vw] border-[2px] border-green-800">
			<Accordion value="0">
				<AccordionPanel value="0">
					<AccordionHeader class="border-none p-3">
						{{
							articleData['premises_type'] + ' ' + articleData['cleaning_type']
						}}</AccordionHeader
					>
					<AccordionContent class="border-">
						<div class="m-0">
							<div>
								Номер телефона:
								<span
									v-clipboard="articleData['phone_number']"
									@click="success"
									class="cursor-pointer underline"
									>{{ articleData['phone_number'] }}</span
								>
							</div>
							<div class="flex flex-row gap-3">
								<div>
									Город: <strong>{{ articleData['city_name'] }}</strong>
								</div>
								<div>
									Улица: <strong>{{ articleData['street_name'] }}</strong>
								</div>
								<div>
									Дом: <strong>{{ articleData['house_number'] }}</strong>
								</div>
								<div>
									Квартира:
									<strong>{{ articleData['apartment_number'] }}</strong>
								</div>
							</div>
							<div>
								Имя-фамилия:
								{{ articleData['first_name'] + ' ' + articleData['last_name'] }}
							</div>
						</div>
					</AccordionContent>
				</AccordionPanel>
			</Accordion>
		</div>
		<div
			@click="visible = true"
			class="flex justify-center items-center text-[1.2vw] font-medium bg-green-600 px-5 cursor-pointer hover:bg-green-500 h-[7vh]"
		>
			Назначить
			<div class="flex justify-center">
				<Dialog
					v-model:visible="visible"
					modal
					header="Выбрать клинера"
					class="bg-green-200 border-none"
				>
					<div v-for="post in product">
						<WorkerTable
							:worker-data="post"
							class="hover:bg-green-300 cursor-pointer"
						/>
					</div>
					<div class="flex justify-end ml-3">
						<Button
							type="button"
							label="Cancel"
							severity="secondary"
							@click="visible = false"
							class="focus:outline-none"
						></Button>
					</div>
					<div>Вы выбрали: {{ store.worker_name }}</div>
					<div class="flex justify-center mt-[4vh]">
						<button
							@click="requestToOrder(articleData['id']), (visible = false)"
							class="flex justify-center font-semibold bg-green-600 px-2 py-1 rounded-xl hover:bg-green-500"
						>
							Подтвердить
						</button>
					</div>
				</Dialog>
			</div>
		</div>
		<div
			@click="visibleDeleteDialog = true"
			class="flex justify-center items-center text-[1.2vw] font-medium bg-red-600 px-5 cursor-pointer hover:bg-red-500 h-[7vh]"
		>
			Удалить
			<div class="flex justify-center">
				<Dialog
					v-model:visible="visibleDeleteDialog"
					modal
					header="Выбрать клинера"
					class="bg-green-200 border-none"
				>
					<div class="">
						Вы точно хотите удалить заявку
						<i
							><strong>{{
								articleData['first_name'] + ' ' + articleData['last_name']
							}}</strong></i
						>
					</div>
					<div class="flex justify-end ml-3">
						<Button
							type="button"
							label="Cancel"
							severity="secondary"
							@click="visibleDeleteDialog = false"
							class="focus:outline-none"
						></Button>
					</div>

					<div class="flex justify-center mt-[4vh] gap-x-5">
						<button
							@click="visibleDeleteDialog = false"
							class="flex justify-center font-semibold bg-green-600 px-3 py-2 rounded-xl hover:bg-green-500"
						>
							Отменить
						</button>
						<button
							@click="
								deleteRequest(articleData['id']), (visibleDeleteDialog = false)
							"
							class="flex justify-center font-semibold bg-red-600 px-3 py-2 rounded-xl hover:bg-red-500"
						>
							Удалить
						</button>
					</div>
				</Dialog>
			</div>
		</div>
	</div>
</template>
<style></style>
