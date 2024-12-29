<script>
import { RouterLink, RouterView } from 'vue-router'

export default {}
</script>
<template>
	<div class="fixed h-screen bg-black">
		<div
			class="flex flex-col text-white mt-[10vh] w-[13vw] pl-[1vw] pr-[1vw] text-[1vw] font-semibold cursor-pointer"
		>
			<RouterLink to="/" class="border-t-2 p-1 hover:bg-gray-700">Главная страница</RouterLink>
			<RouterLink to="/order" class="border-t-2 p-1 hover:bg-gray-700">Журнал заказов</RouterLink>
		</div>
	</div>
</template>
