import { defineStore } from 'pinia';

export const useAttributeStore = defineStore('attributes', {
    state: () => ({
        attributes: [],
    }),
    actions: {
        initialAttributes(attributes) {
            this.attributes = attributes;
        },
        addAttribute(attribute) {
            this.attributes.push(attribute);
        },
        removeAttribute(attribute_id) {
            // Remove the attribute from the attributes array
            this.attributes = this.attributes.filter(a => a._id !== attribute_id);
        },
        setAttributeCompleteInitial(attribute_id) {
            // Find the attribute and set complete_initial to true
            const attribute = this.attributes.find(a => a._id === attribute_id);
            if (attribute) {
                attribute.complete_initial = true;
            }
        },
        randomizeAttributes() {
            // Randomize the attributes array
            this.attributes = this.attributes.sort(() => Math.random() - 0.5);
        }
    },
    getters: {
        getAttributes: (state) => {
            return state.attributes;
        },
    }
});