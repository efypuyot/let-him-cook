<template>
    <transition name="toast">
      <div v-if="show" :class="['toast', `toast-${type}`]">
        {{ message }}
      </div>
    </transition>
  </template>
  
  <script>
  export default {
    data() {
      return {
        show: false,
        message: '',
        type: 'info' // default type
      }
    },
    methods: {
      toast(message, type = 'info', duration = 3000) {
        this.message = message;
        this.type = type;
        this.show = true;
        
        setTimeout(() => {
          this.show = false;
        }, duration);
      }
    }
  }
  </script>
  
  <style scoped>
  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 24px;
    border-radius: 4px;
    color: white;
    z-index: 1000;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  }
  
  .toast-enter-active,
  .toast-leave-active {
    transition: all 0.3s ease;
  }
  
  .toast-enter-from,
  .toast-leave-to {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  
  /* Toast Types */
  .toast-info {
    background: #2196F3;
  }
  
  .toast-success {
    background: #4CAF50;
  }
  
  .toast-warning {
    background: #FF9800;
  }
  
  .toast-error {
    background: #F44336;
  }
  </style>