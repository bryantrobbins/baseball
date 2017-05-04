<template>
  <div class="bw-textarea">
        <textarea rows="4" cols="50">{{ msg }}</textarea>
  </div>
</template>

<script>
export default {
  name: 'bw-textarea',
  data () {
    return {
      msg: 'Enter your job configuration here.'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
