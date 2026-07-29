<template>
  <section class="output-section">
    <!-- Loading state -->
    <div
      v-if="loading"
      class="output-card status-container"
    >
      <div class="spinner"></div>

      <p class="status-text">
        Analysing your SuperStore data...
      </p>
    </div>

    <!-- Error state -->
    <div
      v-else-if="error"
      class="output-card error-container"
    >
      <div class="status-icon">
        !
      </div>

      <h3>Unable to generate insight</h3>

      <p class="error-message">
        {{ error }}
      </p>
    </div>

    <!-- Result state -->
    <div
      v-else-if="result"
      class="output-card"
    >
      <div class="question-label">
        Your question
      </div>

      <p class="selected-question">
        {{ question }}
      </p>

      <div class="divider"></div>

      <div class="answer-label">
        Your answer
      </div>

      <h2 class="result-title">
        {{ result.title }}
      </h2>

      <p class="result-answer">
        {{ result.answer }}
      </p>

      <!-- Ranked list for non-chart results -->
      <div
        v-if="hasListData"
        class="result-list"
      >
        <div
          v-for="(item, index) in result.data"
          :key="`${getItemName(item)}-${index}`"
          class="result-item"
        >
          <div class="result-item-left">
            <span class="rank-badge">
              {{ index + 1 }}
            </span>

            <span class="item-name">
              {{ getItemName(item) }}
            </span>
          </div>

          <span class="item-value">
            {{ formatCurrency(getItemValue(item)) }}
          </span>
        </div>
      </div>

      <!-- Chart results -->
      <ResultChart
        v-if="result.chartType"
        :result="result"
      />
    </div>

    <!-- Empty state -->
    <div
      v-else
      class="output-card empty-state"
    >
      Ask a question to view your data insight.
    </div>
  </section>
</template>

<script>
import ResultChart from "./ResultChart.vue";

export default {
  name: "ChatOutput",

  components: {
    ResultChart
  },

  props: {
    question: {
      type: String,
      default: ""
    },

    result: {
      type: Object,
      default: null
    },

    loading: {
      type: Boolean,
      default: false
    },

    error: {
      type: String,
      default: ""
    }
  },

  computed: {
    hasListData() {
      return Boolean(
        this.result &&
        !this.result.chartType &&
        Array.isArray(this.result.data) &&
        this.result.data.length > 0
      );
    }
  },

  methods: {
    getItemName(item) {
      return (
        item.category ||
        item.customer ||
        item.product ||
        "Result"
      );
    },

    getItemValue(item) {
      return (
        item.sales ??
        item.revenue ??
        0
      );
    },

    formatCurrency(value) {
      const number = Number(value);

      if (!Number.isFinite(number)) {
        return "-";
      }

      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
      }).format(number);
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.output-section {
  width: calc(100% - 40px);
  max-width: 900px;
  margin: 30px auto 60px;
}

.output-card {
  width: 100%;
  min-height: 180px;
  padding: 30px;

  background: var(--surface-bg);
  border: 1px solid var(--border-primary);
  border-radius: 20px;
  box-shadow: 0 10px 35px var(--shadow-light);

  text-align: left;

  transition:
    background-color 0.3s ease,
    border-color 0.3s ease,
    color 0.3s ease;
}

.question-label,
.answer-label {
  margin: 0 0 8px;

  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.selected-question {
  margin: 0;

  color: var(--text-primary);
  font-size: 17px;
  font-weight: 600;
}

.divider {
  height: 1px;
  margin: 24px 0;

  background: var(--divider);
}

.result-title {
  margin: 0 0 10px;

  color: var(--text-heading);
  font-size: 26px;
}

.result-answer {
  margin: 0;

  color: var(--text-secondary);
  font-size: 16px;
  line-height: 1.7;
  white-space: pre-line;
}

/* Ranked result list */

.result-list {
  margin-top: 24px;
}

.result-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;

  padding: 18px 4px;

  border-bottom: 1px solid var(--border-primary);
}

.result-item:last-child {
  border-bottom: none;
}

.result-item-left {
  display: flex;
  align-items: center;
  gap: 16px;

  min-width: 0;
}

.rank-badge {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;

  width: 34px;
  height: 34px;

  padding: 8px;

  background: #2563eb;
  border-radius: 10px;

  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
}

.item-name {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 500;
  line-height: 1.5;
}

.item-value {
  flex-shrink: 0;

  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
  text-align: right;
}

/* Status states */

.status-container,
.error-container,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  text-align: center;
}

.status-text,
.error-message,
.empty-state {
  color: var(--text-muted);
}

.error-message {
  margin: 0;
  line-height: 1.6;
  white-space: pre-line;
}

.spinner {
  width: 34px;
  height: 34px;
  margin-bottom: 14px;

  border: 4px solid var(--border-primary);
  border-top-color: #d6bb48;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

.status-icon {
  display: flex;
  width: 38px;
  height: 38px;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;

  background: var(--danger-bg);
  border-radius: 50%;

  color: var(--danger-text);
  font-weight: 700;
}

.error-container h3 {
  margin: 0 0 8px;

  color: var(--text-primary);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 700px) {
  .output-card {
    padding: 22px;
  }

  .result-title {
    font-size: 22px;
  }

  .result-item {
    gap: 14px;
    padding: 16px 0;
  }

  .result-item-left {
    gap: 12px;
  }

  .rank-badge {
    width: 32px;
    height: 32px;
  }

  .item-name,
  .item-value {
    font-size: 14px;
  }
}

@media (max-width: 500px) {
  .result-item {
    align-items: flex-start;
  }

  .item-value {
    max-width: 110px;
  }
}
</style>