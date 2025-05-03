<template>
    <div class="body-div">
        <div class="header-div">
        <HeaderComponent name="recipe" :showBackButton="true"/>
        </div>  
      <div class="recipe-content">
        <h2>{{ recipe.title }}</h2>
        
        <div class="section">
          <h3>Ingredients</h3>
          <ul>
            <li v-for="(ingredient, index) in parsedIngredients" :key="index">
              {{ ingredient }}
            </li>
          </ul>
        </div>
        
        <div class="section">
          <h3>Directions</h3>
          <ol>
            <li v-for="(step, index) in recipe.directions" :key="index">
              {{ step }}
            </li>
          </ol>
        </div>
        
        <a 
            :href="recipe.link ? (recipe.link.startsWith('http') ? recipe.link : `https://${recipe.link}`) : '#'" 
            target="_blank" 
            class="external-link"
            >
            View Original Recipe
        </a>
      </div>
      <div class="footer-div">
        <FooterComponent
            name="input new ingredients"
            @clicked="goToInputPage"
        />
      </div>
    </div>
  </template>
  
  <script>
  import HeaderComponent from './Header.vue';
  import FooterComponent from './Footer.vue';
  
  export default {
    components: {
      HeaderComponent,
      FooterComponent
    },
    data() {
      return {
        recipe: null
      }
    },

    computed: {
      parsedIngredients() {
        try {
          if (Array.isArray(this.recipe.ingredients)) {
            return this.recipe.ingredients;
          }
          return JSON.parse(this.recipe.ingredients.replace(/\\"/g, '"'));
        } catch {
          return [];
        }
      }
    },

    created() {
        const recipeId = this.$route.params.id;
        const storedRecipe = sessionStorage.getItem(`recipe_${recipeId}`);
        
        if (storedRecipe) {
        this.recipe = JSON.parse(storedRecipe);
        // Optional: clear after loading
        // sessionStorage.removeItem(`recipe_${recipeId}`);
        }
    },

    methods: {
        goToInputPage() {
            this.$router.push('/'); // Navigate back to the ingredients input page
        },
    },
  }
  </script>
  
  <style scoped>

  .recipe-content {
    height: 60vh;
    overflow: scroll;
  }

  .recipe-detail {
    width: 60%;
    padding: 5%;
    max-width: 60%;
    margin: 0 auto;
  }
  
  .section {
    margin-bottom: 2%;
  }
  
  h1 {
    color: #333;
  }
  
  h2 {
    border-bottom: 1px solid #eee;
    padding: 5%;
    color: #444;
  }
  
  ul, ol {
    text-align: start;
    padding: 5%;
  }
  
  li {
    margin-bottom: 8px;
    display: flex;
    justify-content: flex-start;
  }
  
  .external-link {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 15px;
    background: #4ab7ff;
    color: white;
    text-decoration: none;
    border-radius: 10px;
  }
  
  .external-link:hover {
    background: #0a446b;
  }
  </style>