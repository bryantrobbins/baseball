job('r-baseball') {
    scm {
      git('git://github.com/bryantrobbins/r-baseball') { node ->
        node / gitConfigName('Baseball Jenkins Auto')
        node / gitConfigEmail('bryantrobbins@gmail.com')
      }
    }
    steps {
       shell('chmod 700 *.sh; ./build.sh') 
    }
}

job('worker-image') {
    steps {
       shell('pushd worker; chmod 700 *.sh; ./import.sh') 
    }
}

job('puppet-update') {
    steps {
       shell('') 
    }
}
