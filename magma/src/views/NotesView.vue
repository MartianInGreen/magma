<script>
import config from '@/config.js';

import Navbar from '../components/notesView/Navbar.vue'
import LeftSidebarBottom from '../components/notesView/LeftSidebarBottom.vue'
import LeftSidebarTop from '../components/notesView/LeftSidebarTop.vue'

import ViewSettings from '@/components/notesView/ViewSettings.vue';

let userID, token;

try {
    userID = document.cookie.split('; ').find(row => row.startsWith('userID=')).split('=')[1];
    token = document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1];

    if (!token || !userID ) {
        window.location.href = '/login';
    }
} catch (error) {
    window.location.href = '/login';
}

export default {
    components: {
        Navbar,
        LeftSidebarBottom,
        LeftSidebarTop,
        ViewSettings
    },
    data() {
        return {
            userID: userID,
            userDisplayName: '',
            avatarImageSrc: '',
            API_ENDPOINT: config.API_ENDPOINT,
            showViewSettings: false
        }
    },
    methods: {
        // Show the view settings
        showSettings() {
            this.showViewSettings = true;
        }
    },
    async created() {
        // Get the user's avatar image
        const response = await fetch(`${config.API_ENDPOINT}/api/user/getUser`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!data.userIcon || data.userIcon === '' || data.userIcon === 'null' || data.userIcon === 'undefined') {
            this.avatarImageSrc = config.API_ENDPOINT + '/images/avatar_small.png';
        } else {
            this.avatarImageSrc = data.userIcon;
        }

        this.userDisplayName = data.userDisplayName;
    }
}
</script>

<template>
    <div class="h-screen flex flex-col">
        <Navbar/>
        <div class="w-full flex justify-center flex-grow bg-black">
            <div class="flex justify-between w-full h-full">
                <div id="leftcolumn" class="w-[15%] bg-base-100"> 
                    <div class="flex flex-col justify-between h-full">
                        <!-- Left column -->
                        <LeftSidebarTop />
                        <LeftSidebarBottom @settings-button-clicked="showSettings" :imgSrc="avatarImageSrc" :displayName="userDisplayName" />
                    </div>
                </div>
                <div id="centercolumn" class="w-[70%] bg-base-300"> 
                    <ViewSettings v-if="showViewSettings" />
                </div>
                <div id="rightcolumn" class="w-[15%] bg-base-100">
                    <!-- Right column -->
                </div>
            </div>
        </div>
    </div>
</template>