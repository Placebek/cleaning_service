<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Header from './components/main/Header.vue'
import Footer from './components/main/Footer.vue'

import { useAuthStore } from './stores/auth.store'

const authStore = useAuthStore()
</script>

<template>
	<div class="bg-green-100 h-screen">
		<Header />
		<nav
			v-show="authStore.user"
			class="navbar navbar-expand navbar-dark bg-dark"
		>
			<div class="navbar-nav">
				<RouterLink to="/" class="nav-item nav-link">Home</RouterLink>
				<a @click="authStore.logout()" class="nav-item nav-link">Logout</a>
			</div>
		</nav>
		<div class="container pt-4 pb-4">
			<RouterView />
		</div>
	</div>
	<Footer />
</template>
