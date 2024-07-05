<template>
    <div class="welcome-page">
        <h1>Welcome!</h1>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    name: "TheWelcome",
});
</script>

<style scoped>
.welcome-page {
    text-align: center;
    margin-top: 50px;
}

h1 {
    color: black;
    padding-bottom: 10px;
}

button {
    color: black;
    background-color: cornflowerblue;
    text-align: center;
}
</style>