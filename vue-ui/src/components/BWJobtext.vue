<template>
<div id="job-config" class="field">
  <p class="control">
    <textarea class="textarea" placeholder="Enter your job configuration here."></textarea>
  </p>
   <a class="button">Submit Job</a>
</div>
</template>

<script>
export default {
  name: 'bw-jobtext',
  props: ['text']
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
