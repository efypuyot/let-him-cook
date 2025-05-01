<template>
  <header class="header-container">
    <div class="header-pill">
      <button v-if="showBackButton" @click="goBack" class="back-segment">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15 18L9 12L15 6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <div class="title-segment">
        <h1 class="header-name">{{ name }}</h1>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderComponent',
  props: {
    name: {
      type: String,
      required: true,
    },
    showBackButton: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.header-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.header-pill {
  width: 60%;
  height: 50%;
  display: flex;
  background-color: #2c3e50;
  border-radius: 20px;
  overflow: hidden;
}

.back-segment {
  flex: 0 0 30%;
  background-color: #3498db;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.back-segment:hover {
  background-color: #2980b9;
}

.title-segment {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-name {
  font-size: x-large;
  font-weight: bold;
  color: white;
  margin: 0;
  padding: 0 20px;
}
</style>