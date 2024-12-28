import { defineStore } from 'pinia'

import { fetchWrapper } from './fetch'
import { router } from '../router/auth'

const baseUrl = `${import.meta.env.VITE_API_URL}/auth/admin/login`

export const useAuthStore = defineStore({
	id: 'auth',
	state: () => ({
		// initialize state from local storage to enable user to stay logged in
		user: JSON.parse(localStorage.getItem('user')),
		returnUrl: null,
	}),
	actions: {
		async login(tg_id, password) {
			const user = await fetchWrapper.post(`${baseUrl}`, {
				tg_id,
				password,
			})

			// update pinia state
			this.user = user

			// store user details and jwt in local storage to keep user logged in between page refreshes
			localStorage.setItem('user', JSON.stringify(user))

			// redirect to previous url or default to home page
			router.push(this.returnUrl || '/')
		},
		logout() {
			this.user = null
			localStorage.removeItem('user')
			router.push('/login')
		},
	},
})
