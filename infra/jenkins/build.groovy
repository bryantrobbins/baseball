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
    scm {
        git('git://github.com/bryantrobbins/baseball') { node ->
            node / gitConfigName('Baseball Jenkins Auto')
            node / gitConfigEmail('bryantrobbins@gmail.com')
        }
    }
    steps {
       shell('pushd worker; chmod 700 *.sh; ./import.sh') 
    }
}

job('ui-image') {
    wrappers {
        preBuildCleanup()
    }
    scm {
        git('git://github.com/bryantrobbins/baseball') { node ->
            node / gitConfigName('Baseball Jenkins Auto')
            node / gitConfigEmail('bryantrobbins@gmail.com')
            wipeOutWorkspace(false)
        }
    }
    steps {
       shell('pushd ui/build; chmod 700 *.sh; now=`date +%Y%m%d%H%M%S`; ./build.sh $now')
    }
    publishers {
    }
}

job('puppet-update') {
    steps {
       shell('') 
    }
}
