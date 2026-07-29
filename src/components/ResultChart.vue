<template>
  <div
    v-if="hasChartData"
    class="chart-container"
    :class="{
      'horizontal-chart-container': isHorizontalBarChart
    }"
  >
    <Bar
      v-if="chartType === 'bar'"
      :key="`bar-${chartKey}`"
      :data="chartData"
      :options="chartOptions"
    />

    <Line
      v-else-if="chartType === 'line'"
      :key="`line-${chartKey}`"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import {
  Bar,
  Line
} from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: "ResultChart",

  components: {
    Bar,
    Line
  },

  props: {
    result: {
      type: Object,
      default: null
    }
  },

  data() {
    return {
      isDarkMode: false,
      themeVersion: 0,
      themeObserver: null
    };
  },

  computed: {
    hasChartData() {
      return Boolean(
        this.result &&
        this.result.chartType &&
        Array.isArray(this.result.data) &&
        this.result.data.length > 0
      );
    },

    chartType() {
      return this.result?.chartType || null;
    },

    chartKey() {
      const dataKey = this.result?.data
        ?.map((item) => item[this.result.xKey])
        .join("-");

      return [
        this.chartType,
        this.themeVersion,
        dataKey
      ].join("-");
    },

    isHorizontalBarChart() {
      return (
        this.chartType === "bar" &&
        (
          this.result?.orientation === "horizontal" ||
          this.result?.xKey === "product"
        )
      );
    },

    isGroupedBarChart() {
      return (
        this.chartType === "bar" &&
        this.result?.data?.some(
          (item) =>
            Object.prototype.hasOwnProperty.call(
              item,
              "previousSales"
            ) &&
            Object.prototype.hasOwnProperty.call(
              item,
              "latestSales"
            )
        )
      );
    },

    chartColours() {
      if (this.isDarkMode) {
        return {
          text: "#E5E7EB",
          mutedText: "#A1A1AA",
          grid: "rgba(255, 255, 255, 0.10)",

          primary: "#60A5FA",
          secondary: "#FBBF24",

          pointBorder: "#1C1C1E",

          tooltipBackground: "#27272A",
          tooltipText: "#F5F5F7",
          tooltipBorder: "#52525B"
        };
      }

      return {
        text: "#374151",
        mutedText: "#6B7280",
        grid: "rgba(0, 0, 0, 0.08)",

        primary: "#2563EB",
        secondary: "#D97706",

        pointBorder: "#FFFFFF",

        tooltipBackground: "#FFFFFF",
        tooltipText: "#1F2937",
        tooltipBorder: "#D1D5DB"
      };
    },

    chartData() {
      if (!this.hasChartData) {
        return {
          labels: [],
          datasets: []
        };
      }

      const colours = this.chartColours;

      const labels = this.result.data.map(
        (item) => item[this.result.xKey]
      );

      // Declining-products grouped horizontal bar chart
      if (this.isGroupedBarChart) {
        return {
          labels,

          datasets: [
            {
              label:
                this.result.datasetLabels?.[0] ||
                "Previous Period",

              data: this.result.data.map(
                (item) => item.previousSales
              ),

              backgroundColor: colours.primary,
              borderColor: colours.primary,
              borderWidth: 0,
              borderRadius: 6,
              borderSkipped: false
            },

            {
              label:
                this.result.datasetLabels?.[1] ||
                "Latest Period",

              data: this.result.data.map(
                (item) => item.latestSales
              ),

              backgroundColor: colours.secondary,
              borderColor: colours.secondary,
              borderWidth: 0,
              borderRadius: 6,
              borderSkipped: false
            }
          ]
        };
      }

      // Monthly sales line chart
      if (this.chartType === "line") {
        return {
          labels,

          datasets: [
            {
              label:
                this.result.datasetLabel ||
                "Monthly Sales",

              data: this.result.data.map(
                (item) => item[this.result.yKey]
              ),

              borderColor: colours.primary,
              backgroundColor: colours.primary,

              pointBackgroundColor: colours.primary,
              pointBorderColor: colours.pointBorder,
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,

              borderWidth: 3,
              tension: 0.3,
              fill: false
            }
          ]
        };
      }

      // Normal single-dataset bar chart
      return {
        labels,

        datasets: [
          {
            label:
              this.result.datasetLabel ||
              "Result",

            data: this.result.data.map(
              (item) => item[this.result.yKey]
            ),

            backgroundColor: colours.primary,
            borderColor: colours.primary,
            borderWidth: 0,
            borderRadius: 7,
            borderSkipped: false
          }
        ]
      };
    },

    chartOptions() {
      const colours = this.chartColours;
      const isHorizontal = this.isHorizontalBarChart;

      return {
        responsive: true,
        maintainAspectRatio: false,

        indexAxis: isHorizontal ? "y" : "x",

        interaction: {
          mode: "index",
          intersect: false
        },

        plugins: {
          legend: {
            display:
              this.isGroupedBarChart &&
              isHorizontal,

            position: "top",

            labels: {
              color: colours.text,
              usePointStyle: true,
              pointStyle: "rect",
              boxWidth: 12,
              boxHeight: 12,
              padding: 20,

              font: {
                family: "Inter",
                size: 12
              }
            }
          },

          tooltip: {
            backgroundColor:
              colours.tooltipBackground,

            titleColor:
              colours.tooltipText,

            bodyColor:
              colours.tooltipText,

            borderColor:
              colours.tooltipBorder,

            borderWidth: 1,
            padding: 12,
            displayColors: true,

            callbacks: {
              // Product name already appears on the Y-axis
              title: (items) => {
                if (isHorizontal) {
                  return "";
                }

                return items[0]?.label || "";
              },

              label: (context) => {
                const label =
                  context.dataset.label ||
                  "Value";

                const value = isHorizontal
                  ? context.parsed.x
                  : context.parsed.y;

                return (
                  `${label}: ` +
                  `${this.formatNumber(value)}`
                );
              }
            }
          }
        },

        scales: {
          x: {
            type: isHorizontal
              ? "linear"
              : "category",

            beginAtZero: isHorizontal,

            title: {
              display:
                this.chartType === "line" ||
                isHorizontal,

              text: isHorizontal
                ? "Sales"
                : "Month",

              color: colours.text,

              font: {
                family: "Inter",
                size: 12,
                weight: "600"
              }
            },

            ticks: {
              color: colours.mutedText,
              autoSkip: true,

              maxTicksLimit:
                this.chartType === "line"
                  ? 9
                  : undefined,

              maxRotation: 0,
              minRotation: 0,

              callback: isHorizontal
                ? (value) =>
                    this.formatCompactNumber(value)
                : function (value) {
                    return this.getLabelForValue(
                      value
                    );
                  },

              font: {
                family: "Inter",
                size: 11
              }
            },

            grid: {
              color: colours.grid,
              drawBorder: false
            },

            border: {
              color: colours.grid
            }
          },

          y: {
            type: isHorizontal
              ? "category"
              : "linear",

            beginAtZero: !isHorizontal,
            offset: isHorizontal,

            title: {
              display:
                this.chartType === "line" ||
                isHorizontal,

              text: isHorizontal
                ? "Product"
                : "Sales",

              color: colours.text,

              font: {
                family: "Inter",
                size: 12,
                weight: "600"
              }
            },

            ticks: {
              color: colours.mutedText,

              autoSkip: !isHorizontal,

              callback: isHorizontal
                ? function (value) {
                    return this.getLabelForValue(
                      value
                    );
                  }
                : (value) =>
                    this.formatCompactNumber(value),

              font: {
                family: "Inter",
                size: 11
              }
            },

            grid: {
              color: colours.grid,
              drawBorder: false
            },

            border: {
              color: colours.grid
            }
          }
        }
      };
    }
  },

  mounted() {
    this.updateTheme();

    this.themeObserver = new MutationObserver(() => {
      this.updateTheme();
    });

    this.themeObserver.observe(
      document.documentElement,
      {
        attributes: true,
        attributeFilter: ["class"]
      }
    );
  },

  beforeUnmount() {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  },

  methods: {
    updateTheme() {
      const newThemeState =
        document.documentElement.classList.contains(
          "dark"
        );

      if (this.isDarkMode !== newThemeState) {
        this.isDarkMode = newThemeState;
        this.themeVersion += 1;
      }
    },

    formatNumber(value) {
      const number = Number(value);

      if (!Number.isFinite(number)) {
        return value;
      }

      return new Intl.NumberFormat("en-US", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
      }).format(number);
    },

    formatCompactNumber(value) {
      const number = Number(value);

      if (!Number.isFinite(number)) {
        return value;
      }

      return new Intl.NumberFormat("en-US", {
        notation: "compact",
        maximumFractionDigits: 1
      }).format(number);
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 360px;
  margin-top: 26px;
  padding: 18px;

  background: var(--surface-soft);
  border: 1px solid var(--border-secondary);
  border-radius: 16px;

  box-sizing: border-box;

  transition:
    background-color 0.3s ease,
    border-color 0.3s ease;
}

.horizontal-chart-container {
  height: 410px;
}

@media (max-width: 700px) {
  .chart-container {
    height: 320px;
    padding: 12px;
  }

  .horizontal-chart-container {
    height: 440px;
  }
}
</style>