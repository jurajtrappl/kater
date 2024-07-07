<template>
  <Navigation />

  <RouterView />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import Navigation from '@/components/Navigation.vue'

export default defineComponent({
  name: "App",
  components: { Navigation }
})
</script>

<style>
.form-signin {
  max-width: 330px;
  padding: 1rem;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

</style>
