import { createRouter, createWebHistory } from 'vue-router'
import IngredientsInput from '../components/IngredientsInput.vue'
import RecipeList from '../components/RecipeList.vue'
import RecipeDetail from '../components/RecipeDetail.vue'

const routes = [
    {
        path: '/',
        name: 'IngredientsInput',
        component: IngredientsInput
    },
    {
        path: '/recipes',
        name: 'RecipeList',
        component: RecipeList
    },
    {
        path: '/recipe/:id',
        name: 'RecipeDetail',
        component: RecipeDetail,
        props: true
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router