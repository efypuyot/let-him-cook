<template>
  <div class="container">
    <h1>Ingredients Input</h1>
    <div class="home-button">
      <router-link to="/">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          class="w-6 h-6"
        >
          <path
            d="M10.707 17.707a1 1 0 001.414 1.414l4-4a1 1 0 000-1.414l-4-4a1 1 0 00-1.414 1.414L12.586 13H4a1 1 0 000 2h8.586l-2.293 2.293z"
          />
        </svg>
      </router-link>
    </div>
    <div class="ingredients-container">
      <h2>ingredients</h2>
      <div class="ingredient-section">
        <h3>liquid (ml)</h3>
        <div class="ingredient-image">
          <img src="https://www.pngitem.com/pimgs/m/35-355471_cooking-oil-png-transparent-cooking-oil-bottle-png.png" alt="cooking oil" />
        </div>
        <div class="quantity-input">
          <button @click="decreaseQuantity('cookingOil')" class="decrease-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-6 h-6"
            >
              <path
                d="M15 12H9v5l7-7z"
              />
            </svg>
          </button>
          <span>{{ cookingOilQuantity }}</span>
          <button @click="increaseQuantity('cookingOil')" class="increase-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-6 h-6"
            >
              <path
                d="M12 5v14m7-7H5"
              />
            </svg>
          </button>
        </div>
      </div>
      <div class="ingredient-section">
        <h3>water (ml)</h3>
        <div class="ingredient-image">
          <img src="https://www.pngitem.com/pimgs/m/35-355471_cooking-oil-png-transparent-cooking-oil-bottle-png.png" alt="water" />
        </div>
        <div class="quantity-input">
          <button @click="decreaseQuantity('water')" class="decrease-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-6 h-6"
            >
              <path
                d="M15 12H9v5l7-7z"
              />
            </svg>
          </button>
          <span>{{ waterQuantity }}</span>
          <button @click="increaseQuantity('water')" class="increase-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-6 h-6"
            >
              <path
                d="M12 5v14m7-7H5"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cookingOilQuantity: 0, // Initialize quantities
      waterQuantity: 0,
    };
  },
  methods: {
    increaseQuantity(ingredient) {
      if (ingredient === 'cookingOil') {
        this.cookingOilQuantity++;
      } else if (ingredient === 'water') {
        this.waterQuantity++;
      }
    },
    decreaseQuantity(ingredient) {
      if (ingredient === 'cookingOil' && this.cookingOilQuantity > 0) {
        this.cookingOilQuantity--;
      } else if (ingredient === 'water' && this.waterQuantity > 0) {
        this.waterQuantity--;
      }
    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
}

.home-button {
  margin-bottom: 20px;
}

.ingredient-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.ingredient-image img {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.quantity-input {
  display: flex;
  align-items: center;
}

button {
  background: none;
  border: none;
  cursor: pointer;
}

.decrease-button,
.increase-button {
  margin: 0 10px;
}

span {
  font-size: 20px;
  font-weight: bold;
}
</style>
