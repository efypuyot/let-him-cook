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
            <li v-for="(ingredient, index) in parsedIngredients" :key="'ing-'+index">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="checkedIngredients[index]"
                  @change="checkCompletion"
                >
                <span :class="{ 'crossed-out': checkedIngredients[index] }">
                  {{ ingredient }}
                </span>
              </label>
            </li>
          </ul>
        </div>
        
        <div class="section">
          <h3>Directions</h3>
          <ol>
            <li v-for="(step, index) in recipe.directions" :key="'dir-'+index">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="checkedDirections[index]"
                  @change="checkCompletion"
                >
                <span :class="{ 'crossed-out': checkedDirections[index] }">
                  {{ step }}
                </span>
              </label>
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
      <canvas ref="confettiCanvas" class="confetti-canvas"></canvas>
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
        recipe: null,
        checkedIngredients: [],
        checkedDirections: [],
        allCompleted: false,
        confettiAnimation: null
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
      },
      recipeId() {
        return this.$route.params.id;
      }
    },

    created() {
        const recipeId = this.$route.params.id;
        const storedRecipe = sessionStorage.getItem(`recipe_${recipeId}`);
        
        if (storedRecipe) {
          this.recipe = JSON.parse(storedRecipe);
        }
        
        this.loadProgress();
    },

    mounted() {
      this.setupConfetti();
      this.checkCompletion();
    },

    beforeUnmount() {
      if (this.confettiAnimation) {
        cancelAnimationFrame(this.confettiAnimation);
      }
    },

    methods: {
        goToInputPage() {
            this.$router.push('/');
        },
        saveProgress() {
          localStorage.setItem(`recipe_progress_${this.recipeId}_ingredients`, JSON.stringify(this.checkedIngredients));
          localStorage.setItem(`recipe_progress_${this.recipeId}_directions`, JSON.stringify(this.checkedDirections));
        },
        loadProgress() {
          const savedIngredients = localStorage.getItem(`recipe_progress_${this.recipeId}_ingredients`);
          const savedDirections = localStorage.getItem(`recipe_progress_${this.recipeId}_directions`);
          
          if (savedIngredients) {
            this.checkedIngredients = JSON.parse(savedIngredients);
          } else {
            this.checkedIngredients = new Array(this.parsedIngredients.length).fill(false);
          }
          
          if (savedDirections) {
            this.checkedDirections = JSON.parse(savedDirections);
          } else {
            this.checkedDirections = new Array(this.recipe.directions?.length || 0).fill(false);
          }
        },
        checkCompletion() {
          this.saveProgress();
          
          const allIngredientsChecked = this.checkedIngredients.length > 0 && 
                                      this.checkedIngredients.every(Boolean);
          const allDirectionsChecked = this.checkedDirections.length > 0 && 
                                     this.checkedDirections.every(Boolean);
          
          const newCompletedState = allIngredientsChecked && allDirectionsChecked;
          
          if (newCompletedState && !this.allCompleted) {
            this.startConfetti();
          } else if (!newCompletedState && this.allCompleted) {
            this.stopConfetti();
          }
          
          this.allCompleted = newCompletedState;
        },
        setupConfetti() {
          this.canvas = this.$refs.confettiCanvas;
          this.ctx = this.canvas.getContext('2d');
          this.canvas.width = window.innerWidth;
          this.canvas.height = window.innerHeight;
          this.particles = [];
          
          window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
          });
        },
        startConfetti() {
          // Create particles
          const particleCount = 150;
          const blueShades = [
            '#4ab7ff', '#1e90ff', '#00bfff', '#87cefa', 
            '#4682b4', '#5f9ea0', '#6495ed', '#4169e1'
          ];
          
          for (let i = 0; i < particleCount; i++) {
            this.particles.push({
              x: Math.random() * this.canvas.width,
              y: -20,
              size: Math.random() * 10 + 5,
              speed: Math.random() * 3 + 2,
              color: blueShades[Math.floor(Math.random() * blueShades.length)],
              rotation: Math.random() * Math.PI * 2,
              rotationSpeed: Math.random() * 0.2 - 0.1
            });
          }
          
          // Start animation
          if (!this.confettiAnimation) {
            this.animateConfetti();
          }
        },
        animateConfetti() {
          this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
          
          for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            
            this.ctx.save();
            this.ctx.translate(p.x, p.y);
            this.ctx.rotate(p.rotation);
            
            this.ctx.fillStyle = p.color;
            this.ctx.fillRect(-p.size/2, -p.size/2, p.size, p.size);
            
            this.ctx.restore();
            
            p.y += p.speed;
            p.rotation += p.rotationSpeed;
            
            // Reset particles that fall off screen
            if (p.y > this.canvas.height) {
              p.y = -20;
              p.x = Math.random() * this.canvas.width;
            }
          }
          
          this.confettiAnimation = requestAnimationFrame(this.animateConfetti);
        },
        stopConfetti() {
          if (this.confettiAnimation) {
            cancelAnimationFrame(this.confettiAnimation);
            this.confettiAnimation = null;
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.particles = [];
          }
        }
    },
  }
  </script>
  
  <style scoped>
  .recipe-content {
    height: 60vh;
    overflow: scroll;
    position: relative;
    z-index: 1;
  }

  .recipe-detail {
    width: 60%;
    padding: 2%;
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
    list-style-type: none;
    padding-left: 2%;
  }
  
  li {
    margin-bottom: 2%;
    display: flex;
    justify-content: flex-start;
  }
  
  .checkbox-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    width: 100%;
  }
  
  .checkbox-label input[type="checkbox"] {
    margin-right: 10px;
    cursor: pointer;
  }
  
  .crossed-out {
    text-decoration: line-through;
    color: #888;
  }
  
  .external-link {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 15px;
    background: #4ab7ff;
    color: white;
    text-decoration: none;
    border-radius: 10px;
    position: relative;
    z-index: 1;
  }
  
  .external-link:hover {
    background: #0a446b;
  }
  
  .confetti-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 10;
  }
  </style>