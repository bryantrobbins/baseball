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

job('deploy-DEV') {
    parameters {
      textParam('UI_DESIRED_COUNT', '1', 'Number of UI containers to deploy')
      textParam('UI_VERSION', 'latest', 'Version of UI container to deploy')
    }
    wrappers {
        preBuildCleanup()
    }
    scm {
        git('git://github.com/bryantrobbins/baseball') { node ->
            node / gitConfigName('Baseball Jenkins Auto')
            node / gitConfigEmail('bryantrobbins@gmail.com')
        }
    }
    steps {
       shell('pushd infra/stacks; chmod 700 *.sh; echo "UIDesiredCount=${UI_DESIRED_COUNT}" >> dev.properties; echo "UIVersion=${UI_VERSION}" >> dev.properties; ./update.sh dev')
    }
    publishers {
    }
}
job('deploy-BASE') {
    parameters {
    }
    wrappers {
        preBuildCleanup()
    }
    scm {
        git('git://github.com/bryantrobbins/baseball') { node ->
            node / gitConfigName('Baseball Jenkins Auto')
            node / gitConfigEmail('bryantrobbins@gmail.com')
        }
    }
    steps {
       shell('pushd infra/stacks; chmod 700 *.sh; ./update.sh ')
    }
    publishers {
    }
}
