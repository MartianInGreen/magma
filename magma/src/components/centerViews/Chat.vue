<template>
    <div class="flex flex-col items-center justify-between h-[100%]">
        <div id="chatMessages" class="w-[80%] flex justify-start flex-grow">
            <div id="messageContainer" class="w-full"></div>
        </div>
        <div id="attachedFiles"></div>
        <div id="chatInputDiv" class="w-[80%] flex items-center space-x-2 mb-2 mt-auto">
            <button id="fileSelector" class="btn btn-square btn-ghost">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776" /></svg>
            </button>
            <button id="microphoneInput" class="btn btn-square btn-ghost">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" /></svg>
            </button>
            <textarea ref="chatInput" id="chatInput" placeholder="Message Magma AI ✨🤖" class="input input-bordered w-full" style="resize: none; padding-top: 1vh;" v-model="message" @keydown.ctrl.enter="sendMessage" @input="autosize"></textarea>
            <button id="sendButton" class="btn btn-square btn-ghost hover:bg-blue-700" @click="sendMessage">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" /></svg>
            </button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            message: ''
        }
    },
    methods: {
        sendMessage() {
            if (this.message.length > 0) {
                this.message = '';
                this.autosize();
            }
        },
        autosize() {
            this.$nextTick(() => {
                let el = this.$refs.chatInput;
                el.style.cssText = 'height:auto; padding:0; resize: none; padding-top: 1vh;';
                let height = el.scrollHeight + el.offsetHeight - el.clientHeight;
                let text = el.value;
                let lines = text.split('\n').length;
                if (text.length == 0 || lines <= 1) {
                    height = height - 10;
                }
                el.style.cssText = 'height:' + height + 'px; resize: none; padding-top: 1vh;';
            });
        }
    },
    mounted() {
        this.autosize();
    }
}
</script>