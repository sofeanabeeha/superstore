<template>
  <section class="category-section">
    <div class="category-container">
      <div 
        v-for="category in categories" 
        :key="category.name"
        class="category-card"
        @click="openModal(category)"
      > 
        <h3>{{ category.name }}</h3>
        <p>{{ category.description }}</p>
      </div>
    </div>

  <CardModal
    :show="showModal"
    :category="selectedCategory"
    @close="closeModal"
  />

  </section>
</template>


<script>
import CardModal from "./CardModal.vue";

export default {
  name: "CategoryCards",

  components: {
    CardModal
  },

  data() {
    return {
      showModal: false,

      selectedCategory: {},

      categories: [
        {
          name: "Furniture",
          description: "Create functional workspaces with our furniture collection.",
          content: "From ergonomic office chairs to meeting tables and storage solutions, our furniture category supports modern workplace with durable and pratical products.",
          subcategory: "4 types with over 2.1k products",
          product: "Office Chair",
          bestfor:"Office, Meeting Room, Workspace"
        },
        {
          name: "Office Supplies",
          description: "Essential everyday supplies that keep your workplace running smoothly.",
          content: "Browse a wide range of stationery, organization tools and office essentials used across every department.",
          subcategory:"7 types with over 6.0k products",
          product: "Storage",
          bestfor:"Filing, Printing, Organisation"
        },
        {
          name: "Technology",
          description: "Power your business with modern technology products.",
          content:"Discover computers, phones, copiers and accessories designed to improve productivity and everyday business operations.",
          subcategory:"4 types with over 1.8k products",
          product: "Phone",
          bestfor:"Communication and Productivity"
        }
      ]
    };
  },

  methods: {
    openModal(category) {
      this.selectedCategory = category;
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
    }
  }

};
</script>

<style scoped>

.category-section {
  padding: 30px 20px;
}

.category-container {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.category-card {
  width: 320px;
  height: 180px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  background: var(--surface-bg);
  border: 1px solid var(--border-primary);
  border-radius: 28px;
  color: var(--text-primary);
  cursor: pointer;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease,
    background-color 0.3s ease,
    color 0.3s ease,
    border-color 0.3s ease;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 14px 35px var(--shadow-light);
}

h3 {
  margin: 0;
  font-size: 25px;
  font-weight: 700;
  color: var(--text-heading);
}

p {
  margin-top: 8px;
  font-size: 18px;
  color: var(--text-secondary);
  text-align: left;
}

</style>