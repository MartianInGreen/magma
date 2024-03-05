<script>
import config from '@/config';

export default {
    data() {
        return {
            avatarIcon: '',
            userName: '',
            userDisplayName: '',
            userEmail: '',
            tokens: '',
            emailNotValid: false,
            userNameInput: '',
            userDisplayNameInput: '',
            userEmailInput: '',
            avatarFile: null,
            emailNotValidVisible: false,
            updateSuccess: false
        }
    },
    created() {
        this.fetchUserData();
    },
    methods: {
        async fetchUserData() {
            const token = document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1];
            
            const response = await fetch(`${config.API_ENDPOINT}/api/user/getUser`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();

            if (!data.userIcon || data.userIcon === '' || data.userIcon === 'null' || data.userIcon === 'undefined') {
                this.avatarIcon = config.API_ENDPOINT + '/images/avatar_small.png';
            } else {
                let timestamp = new Date().getTime();
                this.avatarIcon = config.API_ENDPOINT + data.userIcon
                console.log(this.avatarImageSrc)
            }

            this.userName = data.userName;
            this.userDisplayName = data.userDisplayName;
            this.userEmail = data.userEmail;
            this.tokens = data.tokens;

            this.userNameInput = this.userName;
            this.userDisplayNameInput = this.userDisplayName;
            this.userEmailInput = this.userEmail;

            console.log(data)
        },
        updateUser() {
            fetch(config.API_ENDPOINT + '/api/user/updateUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1]
                },
                body: JSON.stringify({
                    'userName': this.userNameInput,
                    'userDisplayName': this.userDisplayNameInput,
                    'userEmail': this.userEmailInput
                })
            })
            .then(response => {
                return response.json().then(data => ({status: response.status, body: data}));
            })
            .then(({status, body}) => {
                if (body.error === 'Error, Invalid email.') {
                    this.emailNotValidVisible = true;

                    setTimeout(() => {
                        this.emailNotValidVisible = false;
                    }, 3000);
                } else {
                    this.emailNotValidVisible = false;
                    if (status === 200) {
                        console.log('Success, updated user info.');
                        this.updateSuccess = true;

                        setTimeout(() => {
                            this.updateSuccess = false;
                        }, 3000);
                    }else{
                        console.log('Error, could not update user info.');
                        this.updateSuccess = false;
                    };
                };
                console.log(body);
            })
            .catch(error => console.error(error));
        },
        changeAvatar(event) {
            this.avatarFile = event.target.files[0];
            var formData = new FormData();
            formData.append('avatar', this.avatarFile);

            fetch(config.API_ENDPOINT + '/api/user/updateAvatar', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1]
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    this.fetchUserData();
                })
                .catch(error => console.error(error));
        },
        deleteChachedAvatarLocal() {

        }
    }
}
</script>

<template>
    <div class="flex flex-col justify-between h-[95%]">
        <div class="flex-1">
            <!-- Icon -->
            <div class="flex justify-start items-center h-10 ml-4 mt-4">
                <h1 class="font-bold text-1xl">Avatar: </h1>
                <div class="avatar h-full ml-4" id="avatar">
                    <img :src="avatarIcon" alt="Avatar" class="rounded-full w-full h-full object-cover">
                </div>
                <div class="flex flex-grow"></div>
                <input id="changeAvatar" type="file" class="file-input file-input-bordered w-full max-w-xs mr-4" @change="changeAvatar" />
            </div>
            <!-- Username -->
            <div class="flex justify-start items-center h-10 ml-4 mt-4">
                <h1 class="font-bold text-1xl">Username: </h1>
                <div class="flex-grow"></div>
                <input id="userNameInput" type="text" v-model="userNameInput" class="input input-bordered w-full max-w-xs mr-4 ml-4" />
            </div>
            <!-- UserDisplayName -->
            <div class="flex justify-start items-center h-10 ml-4 mt-4">
                <h1 class="font-bold text-1xl">Display Name: </h1>
                <div class="flex-grow"></div>
                <input id="userDisplayName" type="text" v-model="userDisplayNameInput" class="input input-bordered w-full max-w-xs mr-4 ml-4" />
            </div>
            <!-- Email -->
            <div class="flex justify-start items-center h-10 ml-4 mt-4">
                <h1 class="font-bold text-1xl">Email: </h1>
                <div class="flex-grow"></div>
                <input id="userEmail" type="text" v-model="userEmailInput" class="input input-bordered w-full max-w-xs mr-4 ml-4" />
            </div>

            <div class="h-20"></div>

            <div class="flex justify-center">
                <div tabindex="0" class="collapse collapse-arrow border border-base-300 bg-base-200 mt-4 w-[80%]">
                    <input type="checkbox" /> 
                    <div class="collapse-title text-xl font-medium">
                        <div class="flex justify-start items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" /></svg>
                                                    
                            <h1 class="ml-2 font-bold"> Tokens </h1>
                        </div>
                    </div>
                    <div class="collapse-content"> 
                        <div class="rounded-box bg-base-100">
                            {{ tokens }}
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div id="emailNotValid" class="flex justify-center items-center" v-if="emailNotValidVisible">
            <div role="alert" class="alert alert-error mb-10 w-full w-[80%]">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>Error! E-Mail not a valid E-Mail!</span>
            </div>
        </div>
        <div id="success" class="flex justify-center items-center" v-if="updateSuccess">
            <div role="alert" class="alert alert-success mb-10 w-full w-[80%]">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                <span>Success!</span>
            </div>
        </div>
        <div class="flex justify-center items-center h-10 mr-4">
            <button id="update" class="btn btn-primary" @click="updateUser">Save</button>
        </div>
    </div>
</template>