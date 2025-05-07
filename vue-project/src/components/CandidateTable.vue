<script setup>
import { computed, ref, watch } from "vue";
import { useAttributeStore } from "@/stores/attributes";

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

// Pinia store
const attributeStore = useAttributeStore();

// Extract candidate names (used as column headers)
const candidateNames = computed(() => props.candidates.map(candidate => candidate.name));

// Watch for changes in candidates and synchronize attributes with Pinia
watch(
  () => props.candidates,
  (newCandidates) => {
    if (!newCandidates.length) return;

    const newAttributes = Object.keys(newCandidates[0]).filter(key => key !== "name" && key !== "_id");
    const storedAttributes = attributeStore.getAttributes;

    // Compare attributes (ignoring order)
    const areAttributesSame = newAttributes.length === storedAttributes.length &&
      newAttributes.every(attr => storedAttributes.includes(attr));

    if (!areAttributesSame) {
      attributeStore.initialAttributes(newAttributes);
      attributeStore.randomizeAttributes();
    }
  },
  { immediate: true }
);

// Use attributes from Pinia store
const attributes = computed(() => attributeStore.getAttributes);

// Transfer the attribute name to a more readable format. For instance, "conference_organization_roles" to "Conference Organization Roles".
const attributeDisplayName = (attribute) => {
  return attribute
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
};

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
            <td class="fw-bold">{{ attributeDisplayName(attribute) }}</td>
            <td 
              v-for="candidate in candidates"
              :key="candidate._id"
              class="text-center"
              :class="{ 'table-success': isHighlighted(candidate.name, attribute) }"
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
