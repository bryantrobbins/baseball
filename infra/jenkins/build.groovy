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

job('worker-image') {
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
       shell('pushd worker/build; chmod 700 *.sh; now=`date +%Y%m%d%H%M%S`; ./build.sh $now')
    }
    publishers {
    }
}

job('api-image') {
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
       shell('pushd api/build; chmod 700 *.sh; now=`date +%Y%m%d%H%M%S`; ./build.sh $now')
    }
    publishers {
    }
}

job('deploy-DEV') {
    parameters {
      textParam('UI_DESIRED_COUNT', '1', 'Number of UI containers to deploy')
      textParam('UI_VERSION', 'latest', 'Version of UI container to deploy')
      textParam('API_DESIRED_COUNT', '1', 'Number of API containers to deploy')
      textParam('API_VERSION', 'latest', 'Version of API container to deploy')
      textParam('WORKER_VERSION', 'latest', 'Version of Worker container to deploy')
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
       shell('pushd infra/stacks; chmod 700 *.sh; echo "UIDesiredCount=${UI_DESIRED_COUNT}" >> dev.properties; echo "UIVersion=${UI_VERSION}" >> dev.properties; echo "APIDesiredCount=${API_DESIRED_COUNT}" >> dev.properties; echo "APIVersion=${API_VERSION}" >> dev.properties; echo "WorkerVersion=${WORKER_VERSION}" >> dev.properties; ./update.sh dev')
    }
    publishers {
    }
}
job('deploy-BASE') {
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
       shell('pushd infra/stacks; chmod 700 *.sh; ./update.sh base')
    }
    publishers {
    }
}
