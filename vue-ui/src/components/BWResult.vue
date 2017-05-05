<template>
    <figure class="image is-square">
      <img v-if="result" src="http://bulma.io/images/placeholders/128x128.png">
    </figure>
</template>

<script>
export default {
  name: 'bw-result',
  data () {
    return {
      result: false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
