<template>
  <router-view/>
  <Toaster position="bottom-center" :duration="3000" />
</template>

<script>
import { Toaster } from 'vue-sonner'
export default {
  name: 'App',
  components: { Toaster }
}
</script>

<style>
#app {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>