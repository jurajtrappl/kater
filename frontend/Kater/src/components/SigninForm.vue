<template>
    <form @submit.prevent="handleSubmit">
        <label>Email:</label>
        <input type="email" required v-model="email">

        <label>Password:</label>
        <input type="password" required v-model="password">

        <div class="submit">
            <button>Sign in</button>
        </div>
    </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    name: "SigninForm",
    data() {
        return {
            email: "",
            password: ""
        }
    },
    methods: {
        handleSubmit() {
            console.log("Event submitted")
        }
    }
});
</script>

<style scoped>
form {
    max-width: 420px;
    margin: 30px auto;
    background: white;
    text-align: left;
    padding: 40px;
    border-radius: 10px;
}
label {
    color: black;
    display: inline-block;
    margin: 25px 0 15px;
    font-size: 0.6em;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
}
input {
    display: block;
    padding: 10px 6px;
    width: 100%;
    box-sizing: border-box;
    border: none;
    border-bottom: 1px solid darkgoldenrod;
    color: black;
}
button {
    background: cadetblue;
    border: 0;
    padding: 10px 20px;
    margin-top: 20px;
    color: white;
    border-radius: 20px;
}
.submit {
    text-align: center;
}
</style>