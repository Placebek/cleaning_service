import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../stores/auth.store'
import {
	Home,
	Login,
	NewRequests,
	InProcessRequests,
	CompletedRequests,
} from '../components/page'

export const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	linkActiveClass: 'active',
	routes: [
		{ path: '/', component: Home },
		{ path: '/login', component: Login },
		{ path: '/requests/new', component: NewRequests },
		{ path: '/requests/in_process', component: InProcessRequests },
		{ path: '/requests/completed', component: CompletedRequests },
	],
})

router.beforeEach(async to => {
	const publicPages = ['/login']
	const authRequired = !publicPages.includes(to.path)
	const auth = useAuthStore()

	if (authRequired && !auth.user) {
		auth.returnUrl = to.fullPath
		return '/login'
	}
})
