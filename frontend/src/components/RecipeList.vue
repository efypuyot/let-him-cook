<template>
  <div class="body-div">
    <div class="header-div">
      <HeaderComponent name="recipes" :showBackButton="true"/>
    </div>  
    <div class="recipe-list">
      <div 
        v-for="(recipe, index) in recipes" 
        :key="index" 
        class="recipe-item"
        @click="viewRecipe(recipe)"
      >
        <h3>{{ recipe.title }}</h3>
      </div>
      <div v-if="recipes.length === 0" class="empty-state">
        No recipes found.
      </div>
    </div>
    <div class="footer-div-list"> </div>
  </div>
</template>

<script>
import HeaderComponent from './Header.vue';

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      recipes: []
    };
  },
  created() {
    // Retrieve from session storage
    const storedRecipes = sessionStorage.getItem('recipes');
    if (storedRecipes) {
      this.recipes = JSON.parse(storedRecipes);
    }
  },
  methods: {
    viewRecipe(recipe) {
      // Store in session storage
      sessionStorage.setItem(`recipe_${recipe.tempId}`, JSON.stringify(recipe));
      
      // Pass both ways for redundancy
      this.$router.push({
        name: 'RecipeDetail',
        params: { 
          id: recipe.tempId,
          recipe // Pass the whole recipe object as well
        }
      });
    }
  },
}
</script>

<style scoped>
.recipe-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: scroll;
  gap: 1cap;
  margin-top: 1cap;
}

.recipe-item {
  width: 55%;  
  padding: 2%;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.recipe-item:hover {
  background-color: #f5f5f5;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.recipe-item h3 {
  margin: 0;
  color: #333;
  text-transform: capitalize;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #666;
}

.footer-div-list {
  height: 8%!important;
}
</style>