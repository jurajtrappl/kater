<template>
  <div>
    <Welcome/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Welcome from './components/Welcome.vue';

export default defineComponent({
  components: {
    Welcome
  }
})
</script>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }
}
</style>
