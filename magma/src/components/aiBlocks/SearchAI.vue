<script>
export default {
    props: ['searchTitle', 'searchContent'],
}
</script>

<template>
    <div tabindex="0" class="collapse collapse-arrow border border-base-300 bg-base-200">
        <input type="checkbox" /> 
        <div class="collapse-title text-xl font-medium">
            <div class="flex justify-start items-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" /></svg>
            
                <h1 class="ml-2 font-bold"> {{ searchTitle }}? </h1>
            </div>
        </div>
        <div class="collapse-content"> 
            {{ searchContent }}
        </div>
    </div>
</template>