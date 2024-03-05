<script>
import config from '@/config.js';

export default {
    data() {
        return {
            llamaLink: config.API_ENDPOINT + '/images/llama.jpg'
        }
    }
}
</script>

<template>
    <div class="flex flex-col items-center justify-center h-full">
        <h1 class="font-bold text-4xl">Ups... nothing here 🤷</h1>
        <h1 class="font-bold">Here's a Llama for your troubles:</h1>
        <img :src="llamaLink" alt="Llama" class="w-1/4 mt-4 rounded-lg">
    </div>
</template>