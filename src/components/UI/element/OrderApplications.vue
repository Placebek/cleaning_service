<script setup>
import Accordion from 'primevue/accordion'
import AccordionPanel from 'primevue/accordionpanel'
import AccordionHeader from 'primevue/accordionheader'
import AccordionContent from 'primevue/accordioncontent'
import Dialog from 'primevue/dialog'
import { ref } from 'vue'
import { Clipboard } from 'v-clipboard'
import { store } from '@/stores/states'


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
		deleteOrder(orders_id) {
			const response = ref(null)
			var tokenData = JSON.parse(localStorage.getItem('user'))['access_token']
			const requestOptions = {
				method: 'DELETE',
				headers: {
					'Authorization': 'Bearer ' + tokenData,
				},
			}
			fetch(
				`http://192.168.193.31:8000/auth/admin/orders/${orders_id}`,
				requestOptions
			)
				.then(response => response.json())
				.then(data => (response.value = data))
		},
	},
}
</script>

<template>
	<div class="flex flex-row gap-2 mt-3">
		<div class="w-[60vw] border-[2px] border-green-800">
			<Accordion value="0">
				<AccordionPanel value="0" class="relative">
					<AccordionHeader class="border-none p-3">
						{{
							articleData['premises_type'] + ' ' + articleData['cleaning_type']
						}}</AccordionHeader
					>
					<AccordionContent class="border ">
						<div class="m-01">
							<div>
								Выбранное время:
								<span>{{ articleData['date'].split('T')[0] }}</span
								>
							</div>
							<div>
								Имя-фамилия клиента:
								{{ articleData['first_name'] + ' ' + articleData['last_name'] }}
							</div>
                            <div>
								Статус заказа:
								{{ articleData['status_name']===null ? 'В обработке': articleData['status_name']}}
							</div>
                            <div class="absolute right-2 bottom-2 ">
                                Клинер:
                                <img :src="articleData['photo']" alt="" class="rounded-lg h-[7vh] w-[7vw]" />
                            </div>
						</div>
					</AccordionContent>
				</AccordionPanel>
			</Accordion>
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
					class="bg-green-200 border-none"
				>
					<div class="">
						Вы точно хотите удалить заказ?
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
								deleteOrder(articleData['id']), (visibleDeleteDialog = false)
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
