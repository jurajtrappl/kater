<template>
  <form @submit.prevent="submit">
    <h1 class="h3 mb-3 fw-normal">Please login</h1>

    <input v-model="data.username" class="form-control" placeholder="Username">

    <input v-model="data.password" type="password" class="form-control" placeholder="Password">

    <button class="btn btn-primary w-100 py-2" type="submit">Log in</button>
  </form>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: "Login",
  setup() {
    const data = reactive({
      username: "",
      password: ""
    })

    const router = useRouter()

    const submit = async () => {
      try {
        const response = await fetch("http://localhost:8000/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify(data)
        })

        if (response.status === 200) {
          await router.push('/main')
        } else {
          console.log("Authentication failed.")
        }
      } catch (error) {
        console.error("An error occured: ", error)
      }
    }

    return {
      data,
      submit
    }
  }
})
</script>