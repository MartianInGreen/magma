<template>
    <div class="bg-black h-screen flex flex-col items-center justify-center">
        <h1 class="text-white text-6xl font-bold mb-4">Magma 🌋</h1>
        <h4 class="text-white text-2xl mt-4">Create your account</h4>

        <form ref="signupForm" class="flex flex-col items-center mt-4" method="post">
            <input name="email" type="email" placeholder="Email" class="input input-borderd px-4 rounded mt-4">
            <input name="name" type="name" placeholder="Name" class="input input-borderd py-2 px-4 rounded mt-4">
            <input name="displayName" type="displayname" placeholder="Display Name" class="input input-borderd py-2 px-4 rounded mt-4">
            <button @click="signUp" type="submit" class="btn bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4">Sign Up</button>
        </form>
        <div role="alert" class="alert alert-error mt-4" v-if="showSignupError">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
        </div>
    </div>
</template>

<script>
import config from '@/config.js';

export default {
    data() {
        return {
            showSignupError: false,
            error: ''
        }
    },
    methods: {
        async signUp(event) {
            event.preventDefault();
            const form = this.$refs.signupForm;
            const formData = new FormData(form);
            const email = formData.get('email');
            const name = formData.get('name');
            const displayName = formData.get('displayName');


            const response = await fetch(`${config.API_ENDPOINT}/api/user/createUser`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "userEmail": email,
                    "userName": name,
                    "userDisplayName": displayName
                })
            });
            const data = await response.json();
            console.log(data);
            if (response.ok) {
                this.showSignupError = false;

                // Set cookies 
                document.cookie = `token=${data.tokens[0]}; path=/`;
                document.cookie = 'theme=light; path=/';
                document.cookie = 'userID=' + data.userID + '; path=/';
                document.cookie = 'email=' + data.userEmail + '; path=/';

                this.$router.push('/login');
            } else {
                this.showSignupError = true;
                this.error = data.message;
            }
        }
    }
}
</script>