<template>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
        <div class="container-fluid">
            <RouterLink to="/" class="navbar-brand">Kater</RouterLink>

            <div>
                <ul class="navbar-nav me-auto mb-2 mb-md-0">
                    <li class="nav-item">
                        <RouterLink to="/login" class="nav-link">Login</RouterLink>
                    </li>
                    
                    <li class="nav-item">
                        <RouterLink to="/register" class="nav-link">Register</RouterLink>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import RouterLink from 'vue-router'

export default defineComponent({
    name: "Nav",
});
</script>