<template>
    <div class="flex flex-col items-center bg-black h-screen flex items-center justify-center">
        <h1 class="text-white text-6xl font-bold mb-4">Magma 🌋</h1>
        <h4 class="text-white text-2xl mt-4">Please login to continue</h4>

        <form class="flex flex-col items-center mt-4" @submit.prevent="handleSubmit">
            <input v-model="email" name="email" type="email" placeholder="Email" class="input input-borderd px-4 py-2 rounded mt-4">
            <input v-model="token" name="token" id="tokenInput" type="password" placeholder="Login-Token" class="input input-borderd py-2 px-4 rounded mt-4">              
            <div class="flex mt-4"> 
                <button type="submit" class="btn bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2">Login</button>
                <button type="button" class="btn bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded" @click="goToSignUp">Sign Up</button>
            </div> 
        </form>
    </div>
</template>

<script>
import config from '@/config.js';

export default {
    name: 'LoginView',
    data() {
        return {
            email: '',
            token: ''
        }
    },
    mounted() {
        this.checkCookies();
    },
    methods: {
        checkCookies() {
            const emailCookie = this.getCookie('email');
            const tokenCookie = this.getCookie('token');

            if (emailCookie && tokenCookie) {
                this.$router.push('/notes'); // redirect to /notes if either cookie is not present or empty
            }
        },
        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
        goToSignUp() {
            this.$router.push('/signup');
        },
        async handleSubmit() {
            const response = await fetch(`${config.API_ENDPOINT}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: this.email,
                    token: this.token,
                }),
            });
            const data = await response.json();

            // Check if the response is a 200 OK
            if (response.status === 200) {
                document.cookie = `email=${this.email}; path=/`;
                document.cookie = `token=${this.token}; path=/`;
                document.cookie = `theme=${data.theme}; path=/`;
                
                // Get user info 
                const userResponse = await fetch(`${config.API_ENDPOINT}/api/user/getUser`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`
                    }
                });

                const userData = await userResponse.json();
                document.cookie = 'userID=' + userData.userID + '; path=/';

                this.$router.push('/notes');
            } else {
                alert("Invalid email or token. Please try again.");
            }
        },
    }
}
</script>