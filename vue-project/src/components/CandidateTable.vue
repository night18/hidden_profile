<script setup>
import { computed, defineProps } from "vue";

// Receive candidates as a prop
const props = defineProps({
  candidates: {
    type: Array,
    required: true,
  },
  highlightedCells: {
    type: Array, // Format: [{ name: "Candidate A", attribute: "attribute A" }]
    default: () => [],
  },
});

// Extract candidate names (used as column headers)
const candidateNames = computed(() => props.candidates.map(candidate => candidate.name));

// Extract all attributes dynamically (used as row headers)
const attributes = computed(() => {
  if (!props.candidates.length) return [];
  return Object.keys(props.candidates[0]).filter(key => key !== "name");
});

// Function to check if a cell should be highlighted
const isHighlighted = (name, attribute) => {
  return props.highlightedCells.some(
    (cell) => cell.name === name && cell.attribute === attribute
  );
};
</script>

<template>
  <div class="container mt-4">
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-primary">
          <tr>
            <th class="text-center fw-bold"> </th>
            <th v-for="name in candidateNames" :key="name" class="text-center fw-bold">
              {{ name }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="attribute in attributes" :key="attribute">
            <td class="fw-bold">{{ attribute }}</td>
            <td 
              v-for="candidate in candidates"
              :key="candidate.name"
              class="text-center"
              :class="{ 'table-danger': isHighlighted(candidate.name, attribute) }"
            >
              {{ candidate[attribute] || '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.table-responsive {
  max-width: 800px;
}
</style>
