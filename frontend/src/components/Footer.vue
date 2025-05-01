<template>
    <button 
      @click="$emit('clicked')" 
      class="footer"
      :disabled="disabled">
      <footer>
        <h1 v-if="!disabled" class="footer-name">{{ name }}</h1>
        <h1 v-else class="footer-button">generating...</h1>
      </footer>
    </button>
  </template>
  
  <script>
  export default {
    name: 'FooterComponent',
    props: {
      name: {
        type: String,
        required: true,
      },
      disabled: {
        type: Boolean,
        default: false
      }
    },
  };
  </script>
  
  <style scoped>
  .footer {
    width: 60%;
    height: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #3498db;
    color: white;
    border-radius: 20px;
    border: 0cap;
  }
  
  
  .footer:hover {
    background-color: #004675;
  }

  .footer:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .footer-name {
    font-size: x-large;
    font-weight: bold;
  }
  </style>
  