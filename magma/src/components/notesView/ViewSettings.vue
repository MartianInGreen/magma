<template>
    <div class="flex flex-col items-center rounded-box py-4 px-4 h-full">
        <h1 class="text-4xl font-bold mb-8">Magma 🌋 Settings</h1>
        <div class="w-[80%] flex flex-row justify-center items-center mx-auto h-full">
            <ul class="menu bg-base-200 w-[20%] rounded-box h-full overflow-auto">
                <p class="text-1xl font-bold mb-2">Options</p>
                <li><a @click="changeView('Empty')">General</a></li>
                <li><a @click="changeView('Empty')">Editor</a></li>
                <li><a @click="changeView('Empty')">AI</a></li>
                <li><a @click="changeView('Empty')">Files and links</a></li>
                <li><a @click="changeView('Empty')">Appearance</a></li>
                <li><a @click="changeView('Account')">Account</a></li>
                <li><a @click="changeView('Empty')">Plugins</a></li>
                <div class="divider"></div>
                <div class="flex grow"></div>
                <div class="divider"></div>
                <li><a @click="clearCookies" class="mb-4">Logout</a></li>
            </ul>
            <div class="divider divider-horizontal"></div>
            <div id="settingsView" class="bg-base-200 w-[80%] h-full overflow-auto rounded-lg">
                <component :is="currentView"></component>
            </div>    
        </div>
    </div>
</template>

<script>
import Account from '../settingsViews/Account.vue';
import Empty from '../Empty.vue';
import config from '@/config.js';

export default {
    components: {
        Account,
        Empty
    },
    data() {
        return {
            currentView: '',
        };
    },
    methods: {
        changeView(view) {
            this.currentView = view;
        },
        clearCookies() {
            document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            document.cookie = 'email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            document.cookie = 'theme=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            document.cookie = 'userID=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            window.location.href = '/login';
        }
    },
    mounted() {
        this.changeView('Empty');
    }
}
</script>