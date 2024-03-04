<script>
export default {
  props: ['imgSrc', 'displayName'],
}
</script>

<template>
    <div class="flex flex-row items-center justify-center">
        <button @click="$emit('settings-button-clicked')" class="btn btn-ghost no-animation ml-2 mb-2 mr-2 w-[95%]">
            <div class="avatar h-full" id="avatar">
                <img :src='imgSrc' alt="Avatar" class="rounded-full w-full h-full object-cover">
            </div>
            <p class="font-bold flex-grow truncate" id="userName">{{ displayName }}</p>
        </button>
    </div>
</template>