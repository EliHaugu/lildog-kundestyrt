<template>
  <div :class="['tag', colorClass]">
    <span v-if="leftIcon" class="icon-left">{{ leftIcon }}</span>
    <span class="label">{{ label }}</span>
    <span v-if="rightIcon" class="icon-right">{{ rightIcon }}</span>
  </div>
</template>

<script>
export default {
  name: 'Tag',
  props: {
    label: {
      type: String,
      required: true
    },
    leftIcon: {
      type: String,
      default: ''
    },
    rightIcon: {
      type: String,
      default: ''
    },
    color: {
      type: String,
      default: 'default'
    }
  },
  computed: {
    colorClass() {
      return `tag--${this.color}`
    }
  }
}
</script>

<style scoped>
.tag {
  display: inline-flex;
  align-items: center;
  padding: 0.5em 1em;
  border-radius: 0.25em;
}

.icon-left,
.icon-right {
  margin: 0 0.5em;
}

.tag--default {
  background-color: #e0e0e0;
  color: #000;
}

/* Add more color classes as needed */
</style>
