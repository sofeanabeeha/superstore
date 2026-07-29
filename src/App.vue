<template>
 <div class="app-container">
    <button
      class="theme-toggle"
      type="button"
      :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
      @click="toggleDark()"
    >
      <span>{{ isDark ? "Light" : "Dark" }}</span>
    </button>
 <Header />

  <CategoryCards />

  <ChatInput
  :selectedQuestion="selectedQuestion"
  @select-question="handleSelectQuestion"
  @submit-question="setQuestion"
/>

  <ChatOutput
    :question="selectedQuestion"
    :result="result"
    :loading="loading"
    :error="error"
  />
 </div> 
</template>

<script>
import { useDark, useToggle } from "@vueuse/core";

import Header from "./components/Header.vue";
import CategoryCards from "./components/CategoryCards.vue";
import ChatInput from "./components/ChatInput.vue";
import ChatOutput from "./components/ChatOutput.vue";

export default {
  name: "App",

  components: {
    Header,
    CategoryCards,
    ChatInput,
    ChatOutput
  },

    setup() {
    const isDark = useDark({
      selector: "html",
      attribute: "class",
      valueDark: "dark",
      valueLight: "light"
    });

    const toggleDark = useToggle(isDark);

    return {
      isDark,
      toggleDark
    };
  },

  data() {
    return {
      selectedQuestion: "",
      result: null,
      loading: false,
      error: ""
    };
  },

  methods: {
     handleSelectQuestion(question) {
    this.selectedQuestion = question;
  },

    async setQuestion(question) {
      this.selectedQuestion = question;
      this.result = null;
      this.error = "";
      this.loading = true;

      try {
        const response = await fetch(
          "https://superstore-backend-jcx8.onrender.com/api/ask",
          {
            method: "POST",

            headers: {
              "Content-Type": "application/json"
            },

            body: JSON.stringify({
              question: question
            })
          }
        );

        const data = await response.json();
        console.log(data);

        if (!response.ok || !data.success) {
          throw new Error(
            data.error || "Unable to analyse the data."
          );
        }

        this.result = data;
      } catch (error) {
        console.error("Frontend error:", error);

        if (error instanceof TypeError) {
          this.error =
            "Cannot connect to the backend. Please try again shortly.";
        } else {
          this.error =
            error.message || "Something went wrong.";
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");

/* Light-mode colours */
:root {
  color-scheme: light;

  --page-bg: #fafafa;
  --surface-bg: #ffffff;
  --surface-soft: #f8f9ff;
  --dropdown-bg: #fffefa;

  --text-primary: #1d1d1f;
  --text-heading: #111827;
  --text-secondary: #6b7280;
  --text-muted: #777777;

  --border-primary: #e5e7eb;
  --border-secondary: #dddddd;
  --divider: #ededed;

  --hover-bg: #79776f;
  --hover-text: #fffefa;

  --highlight-bg: #fff3b0;
  --danger-bg: #fff0f0;
  --danger-text: #c74343;

  --shadow-light: rgba(0, 0, 0, 0.06);
  --shadow-medium: rgba(0, 0, 0, 0.14);
}

/* Dark-mode colours */
html.dark {
  color-scheme: dark;

  --page-bg: #111113;
  --surface-bg: #1c1c1e;
  --surface-soft: #27272a;
  --dropdown-bg: #232326;

  --text-primary: #f5f5f7;
  --text-heading: #ffffff;
  --text-secondary: #b0b0b5;
  --text-muted: #99999f;

  --border-primary: #3a3a3c;
  --border-secondary: #444448;
  --divider: #3a3a3c;

  --hover-bg: #f5d96b;
  --hover-text: #1d1d1f;

  --highlight-bg: #4a4020;
  --danger-bg: #422626;
  --danger-text: #ff8080;

  --shadow-light: rgba(0, 0, 0, 0.3);
  --shadow-medium: rgba(0, 0, 0, 0.5);
}

html,
body {
  margin: 0;
  min-height: 100%;
  background: var(--page-bg);
}

body {
  transition:
    background-color 0.3s ease,
    color 0.3s ease;
}

button,
input,
textarea,
select {
  font: inherit;
}

#app {
  min-height: 100vh;

  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Helvetica Neue",
    Arial,
    sans-serif;

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  text-align: center;
  color: var(--text-primary);
}

.app-container {
  position: relative;
  min-height: 100vh;
  padding-top: 60px;
  padding-bottom: 60px;
  background: var(--page-bg);
  color: var(--text-primary);
  transition:
    background-color 0.3s ease,
    color 0.3s ease;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 24px;
  z-index: 2000;
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 10px 16px;
  color: var(--text-primary);
  background: var(--surface-bg);
  border: 1px solid var(--border-primary);
  border-radius: 999px;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    color 0.3s ease,
    background-color 0.3s ease,
    border-color 0.3s ease;
}

.theme-toggle:hover {
  transform: translateY(-2px);
}

.theme-toggle:active {
  transform: scale(0.97);
}
</style>