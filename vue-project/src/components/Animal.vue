<script setup>
import { computed } from 'vue';
import { animals, colors } from './constants';

const props = defineProps({
    name: {
        type: String,
        default: null
    },
    color: {
        type: String,
        default: null
    },
    size: {
        type: String,
        default: '50px'
    },
    rounded: {
        type: Boolean,
        default: false
    },
    square: {
        type: Boolean,
        default: false
    },
    dance: {
        type: Boolean,
        default: false
    }
});

const avatarName = computed(() => {
    if (props.name !== null) {
        const lower = props.name.toLowerCase();
        if (animals.includes(lower)) {
            return lower;
        }
        console.error(
            `InvalidAnimal: '${props.name}' is not a valid animal name. Using random animal instead.`
        );
    }
    return animals[(animals.length * Math.random()) << 0];
});

const getAvatar = computed(() => {
    return `animals/${avatarName.value}.png`;
});

const avatarColor = computed(() => {
    if (props.color) {
        const lower = props.color.toLowerCase();
        if (lower in colors) {
            return colors[lower];
        } else if (lower === 'none') {
            return 'transparent';
        } else if (/^#[0-9A-F]{6}$/i.test(lower)) {
            return lower;
        } else {
            console.error(
                `InvalidColor: '${props.color}' is not a valid color. Using random color instead.`
            );
        }
    }
    const keys = Object.keys(colors);
    return colors[keys[(keys.length * Math.random()) << 0]];
});

const altText = computed(() => {
    return `${props.color} ${avatarName.value}`;
});

const avatarSize = computed(() => {
    if (
        props.size.match(
            /(^\d*)(em|ex|%|px|cm|mm|in|pt|pc|ch|rem|vh|vw|vmin|vmax)/
        )
    ) {
        return props.size;
    } else {
        console.error(
            `InvalidSize: '${props.size}' is not a valid CSS width property. Using '70px' instead.`
        );
    }
    return '70px';
});

const borderRadius = computed(() => {
    if (props.rounded) {
        return '10%';
    } else if (props.square) {
        return '0px';
    }
    return '50%';
});

const styleVars = computed(() => {
    return {
        '--a-bg-color': avatarColor.value,
        '--a-size': avatarSize.value,
        '--a-border-radius': borderRadius.value
    };
});
</script>
<template>
    <div class="v-animal-avatar" :style="styleVars">
        <img
            :src="getAvatar"
            :alt="altText"
            class="v-animal-image"
            :class="dance ? 'v-animal-dance' : ''"
        />
    </div>
</template>
<style lang="scss" scoped>
@import url('./animation.css');
.v-animal-avatar {
    height: var(--a-size);
    width: var(--a-size);
    border-radius: var(--a-border-radius);
    background-color: var(--a-bg-color);
    display: flex;
    align-items: center;
    justify-content: center;
    max-height: 200px;
    max-width: 200px;
    .v-animal-image {
        width: 80%;
        height: 80%;
        user-select: none;
    }
}

.v-animal-dance {
    -webkit-animation: v-a-dance 2s infinite;
    -moz-animation: v-a-dance 2s infinite;
    animation: v-a-dance 2s infinite;
}
</style>
