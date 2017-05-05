<template>
  <div class="main">
    <h1>{{ msg }}</h1>
    <div class="columns">
      <div class="column is-5 is-offset-1">
          <bw-jobtext :text="jobText"></bw-jobtext>
      </div>
      <div class="column is-5">
          <bw-result></bw-result>
      </div>
    </div>
  </div>
</template>

<script>
import BWJobtext from '../components/BWJobtext.vue'
import BWResult from '../components/BWResult.vue'
export default {
  components: {
    'bw-jobtext': BWJobtext,
    'bw-result': BWResult
  },
  name: 'main',
  data () {
    return {
      msg: 'Welcome to the Baseball Workbench',
      jobText: 'Initial Text for Job'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
