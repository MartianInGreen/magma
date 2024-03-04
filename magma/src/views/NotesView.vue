<script>
import Navbar from '../components/notesView/Navbar.vue'

export default {
    components: {
        Navbar
    }
}
</script>

<template>
    <div class="h-screen flex flex-col">
        <Navbar/>
        <div class="w-full flex justify-center flex-grow bg-black">
            <div class="flex justify-between w-full h-full">
                <div id="leftcolumn" class="w-[15%] bg-base-100"> 
                    <!-- Left column -->
                </div>
                <div id="centercolumn" class="w-[70%] bg-base-300"> 
                    <!-- Center column -->
                </div>
                <div id="rightcolumn" class="w-[15%] bg-base-100">
                    <!-- Right column -->
                </div>
            </div>
        </div>
    </div>
</template>