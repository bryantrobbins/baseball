job('r-baseball') {
    scm {
      git('git://github.com/bryantrobbins/r-baseball') { node ->
        node / gitConfigName('Jenkins Auto')
        node / gitConfigEmail('bryantrobbins@gmail.com')
      }
    }
    steps {
       shell('chmod 700 *.sh; ./build.sh') 
    }
}
