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
  position: relative;
  z-index: 1;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  overflow: hidden;
}

/* Background layer with opacity */
#app::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/background.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.03; /* very low opacity */
  z-index: -1; /* put it behind the app content */
}
</style>