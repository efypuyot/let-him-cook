<template>
  <div class="body-div">
    <div class="header-div">
      <HeaderComponent name="ingredients"/>
    </div>  

    <div class="input-div">
      <span class="details"> please input your available ingredients... </span>
      <input v-model="ingr_input" class="input" placeholder="beef, onion, garlic">
      <span v-if="showError" class="error-message">Please enter at least one ingredient.</span>
    </div>

    <div class="footer-div">
      <FooterComponent
        name="generate recipes"
        @clicked="fetchRecommendations"
        :disabled="isLoading"
      />
    </div>
  </div>
</template>

  
  <script>
  import HeaderComponent from './Header.vue';
  import FooterComponent from './Footer.vue';
  import { toast } from 'vue-sonner';
  
  export default {
    name: 'IngredientsInput',
    components: {
      HeaderComponent,
      FooterComponent,
    },
    
    data() {
      return {
        ingr_input: '',
        showError: false,
        recommendations: [],
        isLoading: false
      };
    },

    computed: {
      isInputEmpty() {
        return this.ingr_input.trim().length === 0;
      }
    },

    methods: {
      async fetchRecommendations() {
        if (this.isLoading) return;

        const ingredients = this.ingr_input.split(',')
          .map(i => i.trim())
          .filter(i => i.length > 0);
          
        if (ingredients.length === 0) {
          this.showError = true;
          return;
        }

        this.isLoading = true; // Start loading
        const toastId = toast.loading('generating recipes...', {
          position: 'bottom-center'
        });
        this.showError = false;

        try {
          const API_URL = process.env.VUE_APP_API_URL || "http://localhost:5000";

          const response = await fetch(`${API_URL}/recommend`, {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'bypass-tunnel-reminder': true,
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            },
            body: JSON.stringify({ ingredients }),
          });

          if (!response.ok) throw new Error('Server error');
          
          const data = await response.json();
          
          // Add temporary IDs to each recipe
          const recipesWithIds = data.map((recipe, index) => ({
            ...recipe,
            tempId: index + 1
          }));

          // Store FIRST
          sessionStorage.setItem('recipes', JSON.stringify(recipesWithIds));
          
          // Then navigate - use await to ensure completion
          await this.$router.push({
            name: 'RecipeList',
            query: { count: recipesWithIds.length }
          }).catch(err => {
            console.error('Navigation error:', err);
            throw new Error('Navigation failed');
          });
          
          // Only show success if navigation worked
          toast.success(`found ${recipesWithIds.length} recipes!`, {
            id: toastId,
            position: 'bottom-center'
          });
          
        } catch (error) {
          toast.error(`failed: ${error.message}`, {
            id: toastId,
            position: 'bottom-center'
          });
          console.error('Error:', error);
        } finally {
          this.isLoading = false;
        }
      }
    },
  };
  </script>
  
  <style>
  .body-div {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }

  .header-div {
    height: 15%;
    display: flex;
    justify-content: center;
  }

  .input-div {
    height: 15%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .details {
    font-size: small;
    font-style: italic;
    margin: 2cap;
  }

  .input {
    width: 55%;
    height: 15%;
    padding: 2%;
    border-radius: 10px;
    font-family: 'Inter';
  }

  .error-message {
    color: red;
    font-size: 0.8rem;
    margin-top: 1cap;
  }

  .footer-div {
    height: 15%;
    display: flex;
    justify-content: center;
  }

  </style>
  