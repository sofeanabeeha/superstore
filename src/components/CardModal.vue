<template>

<div
  v-if="show"
  class="overlay"
  @click.self="closeModal"
>

  <div class="modal">

    <button 
      class="close"
      @click="closeModal"
    >
      ✕
    </button>

    <h2 class="name">
      {{ category.name }}
    </h2>

    <p class="content">
      {{ category.content }}
    </p>
  
    <div class="stats">
      <div class="stat-card">
        <h4>Subcategory</h4>
        <p>
          {{ category.subcategory }}
        </p>
      </div>

      <div class="stat-card">
        <h4>Top Product</h4>
        <p>
          {{ category.product }}
        </p>
      </div>

      <div class="stat-card">
        <h4>Best For</h4>
        <p>
          {{ category.bestfor }}
        </p>
      </div>

    </div>

  </div>
</div>
</template>


<script>

export default {
props:{
show:Boolean,
category:Object
},

emits:[
"close"
],

methods:{
closeModal(){
this.$emit("close")
}

}

}

</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal {
  width: 700px;
  height: 300px;
  background: var(--surface-bg);
  border: 1px solid var(--border-primary);
  border-radius: 20px;
  padding: 35px;
  position: relative;
  text-align: center;
  color: var(--text-primary);
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease,
    color 0.3s ease;
}

.close {
  position: absolute;
  right: 20px;
  top: 15px;
  border: none;
  border-radius: 8px;
  background: var(--surface-soft);
  color: var(--text-primary);
  font-size: 22px;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}

.close:hover {
  background: var(--highlight-bg);
  color: var(--text-primary);
}

.name {
  color: var(--text-heading);
  line-height: 0.5;
  text-align: left;
}

.content {
  color: var(--text-secondary);
  line-height: 1.5;
  text-align: left;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 25px;
}

.stat-card {
  background: var(--surface-soft);
  border: 1px solid var(--border-primary);
  border-radius: 12px;
  padding: 15px;
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease;
}

.stat-card h4 {
  font-size: 13px;
  color: var(--text-secondary);
}

.stat-card p {
  color: var(--text-primary);
  font-weight: bold;
}
</style>