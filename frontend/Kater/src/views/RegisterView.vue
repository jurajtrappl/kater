<template>
  <form @submit.prevent="submit">
      <h1 class="h3 mb-3 fw-normal">Please register</h1>

      <input v-model="data.username" class="form-control" placeholder="Username" required>

      <input v-model="data.email" type="email" class="form-control" placeholder="name@example.com">

      <input v-model="data.password" type="password" class="form-control" placeholder="Password">

      <button class="btn btn-primary w-100 py-2" type="submit">Sign up</button>
    </form>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: "Register",
  setup() {
    const data = reactive({
      username: "",
      email: "",
      password: ""
    })

    const router = useRouter()

    const submit = async () => {
      try {
        const response = await fetch("http://localhost:8000/register/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        })

        if (response.status === 201) {
          await router.push("/login")  
        } else {
          console.log("Register failed.")
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