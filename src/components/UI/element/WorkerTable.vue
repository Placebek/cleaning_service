<script>
import { store } from '@/stores/states'

export default {
	props: ['workerData'],
	data() {
		return {
			workerData: this.workerData,
			color: 'bg-green-300',
		}
	},
	methods: {
		changeColorID(worker, name) {
			store.worker_id = worker
			store.worker_name = name
		},
		isSelect() {
			if (store.worker_id === this.workerData['id']) {
				return this.color
			}
		},
	},
}
</script>

<template>
	<div
		@click="
			changeColorID(
				workerData['id'],
				workerData['first_name'] + ' ' + workerData['last_name']
			)
		"
		v-bind:class="'border-[1px] border-green-400 ' + isSelect()"
	>
		<div class="flex flex-row gap-x-3 p-1">
			{{}}
			<div class="h-[5vh] w-[2.8vw]">
				<img :src="workerData['photo']" alt="" class="rounded-lg" />
			</div>
			<div>
				<div>
					Имя-фамилия:
					{{ workerData['first_name'] + ' ' + workerData['last_name'] }}
				</div>
				<div>Контактный номер: {{ workerData['phone_number'] }}</div>
				<div>Опыт работы: {{ workerData['experience'] }} лет</div>
			</div>
		</div>
	</div>
</template>

<style></style>
