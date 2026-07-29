<template>
  <div
    class="chat-container"
    :class="{ 'dropdown-open': isOpen }"
  >
    <form
      class="chat-form"
      @submit.prevent="submitQuestion"
    >
      <input
        ref="questionInput"
        v-model="question"
        type="text"
        class="chat-input"
        placeholder="Ask something about your SuperStore data..."
        autocomplete="off"
        @focus="openSuggestions"
        @input="openSuggestions"
        @keydown.esc="closeSuggestions"
      />

      <button
        type="submit"
        class="send-button"
        :disabled="!question.trim()"
      >
        Send
      </button>
    </form>

    <div
      v-if="isOpen"
      class="question-dropdown"
    >
      <div class="dropdown-heading">
        Suggested questions
      </div>

      <button
        v-for="suggestedQuestion in filteredQuestions"
        :key="suggestedQuestion"
        type="button"
        class="question-item"
        @mousedown.prevent="selectQuestion(suggestedQuestion)"
      >
        <span class="question-icon">↗</span>

        <span>
          {{ suggestedQuestion }}
        </span>
      </button>

      <p
        v-if="filteredQuestions.length === 0"
        class="no-results"
      >
        No matching suggestions. You can still send your own question.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatInput",

  props: {
    selectedQuestion: {
      type: String,
      default: ""
    }
  },

  emits: [
    "select-question",
    "submit-question"
  ],

  data() {
    return {
      question: this.selectedQuestion,
      isOpen: false,

      questions: [
        "Which category has the highest sales?", // ranked list
        "What is the monthly sales trend?", // line chart
        "Who are the top customers by sales?", // ranked list
        "What are the top products by revenue?", // ranked list
        "Which products have declining sales?", // clustered bar chart
      ]
    };
  },

  computed: {
    filteredQuestions() {
      const searchText = this.question
        .toLowerCase()
        .trim();

      if (!searchText) {
        return this.questions;
      }

      return this.questions.filter((suggestedQuestion) =>
        suggestedQuestion
          .toLowerCase()
          .includes(searchText)
      );
    }
  },

  watch: {
    selectedQuestion(newQuestion) {
      this.question = newQuestion;
    }
  },

  mounted() {
    document.addEventListener(
      "click",
      this.handleOutsideClick
    );
  },

  beforeUnmount() {
    document.removeEventListener(
      "click",
      this.handleOutsideClick
    );
  },

  methods: {
    openSuggestions() {
      this.isOpen = true;
    },

    closeSuggestions() {
      this.isOpen = false;
    },

    selectQuestion(suggestedQuestion) {
      this.question = suggestedQuestion;
      this.isOpen = false;

      this.$emit(
        "select-question",
        suggestedQuestion
      );

      this.$nextTick(() => {
        this.$refs.questionInput.focus();
      });
    },

    submitQuestion() {
      const cleanedQuestion = this.question.trim();

      if (!cleanedQuestion) {
        return;
      }

      this.isOpen = false;

      this.$emit(
        "submit-question",
        cleanedQuestion
      );
    },

    handleOutsideClick(event) {
      if (!this.$el.contains(event.target)) {
        this.closeSuggestions();
      }
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.chat-container {
  width: calc(100% - 40px);
  max-width: 900px;
  margin: 30px auto;
  position: relative;
  z-index: 1;
}

.chat-container.dropdown-open {
  z-index: 1000;
}

/* Input bar */

.chat-form {
  width: 100%;
  min-height: 62px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px;
  background: var(--surface-bg);
  border: 1px solid var(--border-secondary);
  border-radius: 17px;
  box-shadow: 0 6px 20px var(--shadow-light);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background-color 0.3s ease;
}

.chat-form:focus-within {
  border-color: #a8a9aa;
  box-shadow:
    0 0 0 4px rgba(20, 124, 229, 0.1),
    0 8px 24px var(--shadow-light);
}

.chat-input {
  flex: 1;
  min-width: 0;
  height: 46px;
  padding: 0 14px;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 16px;
}

.chat-input::placeholder {
  color: var(--text-muted);
}

/* Send button */

.send-button {
  flex-shrink: 0;
  min-width: 80px;
  height: 46px;
  padding: 0 19px;
  background: gray;
  border: none;
  border-radius: 12px;
  color: white;
  font-family: inherit;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    transform 0.2s ease,
    opacity 0.2s ease;
}

.send-button:hover:not(:disabled) {
  background: blue;
  transform: translateY(-1px);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
}

.send-button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* Suggested question dropdown */

.question-dropdown {
  position: absolute;
  top: calc(100% + 9px);
  left: 0;
  width: 100%;
  max-height: 285px;
  overflow-y: auto;
  padding: 8px;
  background: var(--dropdown-bg);
  border: 1px solid var(--border-secondary);
  border-radius: 15px;
  box-shadow: 0 14px 35px var(--shadow-medium);
  z-index: 1001;
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease;
}

.dropdown-heading {
  padding: 8px 12px 10px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.question-item {
  width: 100%;
  min-height: 48px;
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 11px 12px;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: var(--text-secondary);
  font-family: inherit;
  font-size: 14px;
  text-align: left;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}

.question-item:hover {
  background: var(--hover-bg);
  color: var(--hover-text);
}

.question-icon {
  width: 27px;
  height: 27px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(99, 100, 100, 0.1);
  border-radius: 8px;
  color: #747574;
  font-size: 14px;
  font-weight: 700;
}

.no-results {
  margin: 0;
  padding: 15px 12px;
  color: var(--text-muted);
  font-size: 14px;
  line-height: 1.5;
}

/* Scrollbar */

.question-dropdown::-webkit-scrollbar {
  width: 7px;
}

.question-dropdown::-webkit-scrollbar-thumb {
  background: var(--border-secondary);
  border-radius: 10px;
}

.question-dropdown::-webkit-scrollbar-track {
  background: transparent;
}

/* Mobile */

@media (max-width: 520px) {
  .chat-container {
    width: calc(100% - 28px);
  }

  .chat-form {
    min-height: 58px;
  }

  .chat-input {
    height: 42px;
    padding: 0 9px;
    font-size: 14px;
  }

  .send-button {
    min-width: 68px;
    height: 42px;
    padding: 0 13px;
  }
}
</style>