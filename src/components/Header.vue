<template>
  <header class="header">
    <div class="header-content">
      <p class= "welcome">Welcome to</p>
      <h1 class="title">SuperStore Insight</h1>
      <p class="subtitle">
        Analyse your data with simple and business-friendly questions.
      </p>
    </div>
  </header>
</template>

<script>
export default {
  name: "Header"
};
</script>

<style scoped>
.header {
  width: 100%;
  padding: 70px 24px;
  background: var(--surface-bg);
  border-bottom: 1px solid var(--border-primary);
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.welcome {
  margin: 0 0 12px;
  color: var(--text-primary);
  font-size: 28px;
  font-weight: 600;
  transition: color 0.3s ease;
}

.title {
  margin: 0;
  color: var(--text-heading);
  font-size: 56px;
  font-weight: 700;
  line-height: 1.1;
  transition: color 0.3s ease;
}

.subtitle {
  margin-top: 20px;
  color: var(--text-secondary);
  font-size: 20px;
  transition: color 0.3s ease;
}
</style>