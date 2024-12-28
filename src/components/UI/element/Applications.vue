<script setup>
import Accordion from 'primevue/accordion'
import AccordionPanel from 'primevue/accordionpanel'
import AccordionHeader from 'primevue/accordionheader'
import AccordionContent from 'primevue/accordioncontent'
import { Clipboard } from 'v-clipboard'
import { number } from 'yup'
</script>

<script>
export default {
	props: ['articledata'],
	props: {
		name_cleaning: {
			type: String,
			required: true,
		},
		phone_number: {
			type: Number,
			required: true,
		},
		city: {
			type: String,
			required: true,
		},
		street: {
			type: String,
			required: true,
		},
		house: {
			type: Number,
			required: true,
		},
		home: {
			type: Number,
			required: false,
		},
		name_user: {
			type: String,
			required: true,
		},
		last_name_user: {
			type: String,
			required: false,
		},
	},
	methods: {
		success() {
			alert('success')
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
					<AccordionHeader class="border-none p-3"
						>Генеральная уборка чего то {{}}</AccordionHeader
					>
					<AccordionContent class="border-">
						<div class="m-0">
							<div>
								Номер телефона:
								<span
									v-clipboard="phone_number"
									class="cursor-pointer underline"
									>{{ phone_number }}</span
								>
							</div>
							<div class="flex flex-row gap-3">
								<div>Город: {{ city }}</div>
								<div>Улица: {{ street }}</div>
								<div>Дом: {{ house }}</div>
								<div>Квартира: {{ home }}</div>
							</div>
							<div>Дополнительные пожелания: {{}}</div>
							<div>Имя-фамилия: {{ name_user + last_name_user }}</div>
						</div>
					</AccordionContent>
				</AccordionPanel>
			</Accordion>
		</div>
		<div
			class="flex justify-center items-center text-[1.2vw] font-medium bg-green-600 px-5 cursor-pointer hover:bg-green-500 h-[7vh]"
		>
			Назначить&#9660;
		</div>
		<div
			class="flex justify-center items-center text-[1.2vw] font-medium bg-red-600 px-5 cursor-pointer hover:bg-red-500 h-[7vh]"
		>
			Удалить
		</div>
	</div>
</template>
<style></style>
