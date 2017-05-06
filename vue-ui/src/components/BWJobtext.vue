<template>
<div id="job-config" class="field">
  <p class="control">
    <textarea class="textarea" placeholder="Enter your job configuration here." v-model="text"></textarea>
  </p>
   <a class="button" @click="onSubmit">Submit Job</a>
</div>
</template>

<script>
export default {

  name: 'bw-jobtext',

  data () {
    return {
      text: ''
    }
  },

  methods: {

    onSubmit () {
      window.EventBus.$emit('jobComplete', {jobId: 'somefakejob'})
    }

  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
textarea {
  height: 300px;
}
</style>
