<template>
  <div class="main">
    <h1>{{ msg }}</h1>
    <bw-textarea></bw-textarea>
  </div>
</template>

<script>
import BWTextarea from '../components/BWTextarea.vue'
export default {
  components: {
    'bw-textarea': BWTextarea
  },
  name: 'main',
  data () {
    return {
      msg: 'Welcome to the Baseball Workbench'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
