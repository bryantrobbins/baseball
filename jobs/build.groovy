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
       shell('pushd ui/build; chmod 700 *.sh; ./build.sh') 
    }
    publishers {
        archiveArtifacts {
            pattern('ui/build/frontend.tar')
            onlyIfSuccessful()
        }
        slackNotifications {
            projectChannel('general')
            notifySuccess()
            notifyBuildStarted()
            notifyAborted()
            notifyFailure()
            notifyNotBuilt()
            notifyUnstable()
            notifyBackToNormal()
        }
    }
}

job('ui-deploy') {
    scm {
        git('git://github.com/bryantrobbins/baseball') { node ->
            node / gitConfigName('Baseball Jenkins Auto')
            node / gitConfigEmail('bryantrobbins@gmail.com')
            wipeOutWorkspace(false)
        }
    }
    steps {
       copyArtifacts('ui-image')
       shell('pushd ui/build; chmod 700 *.sh; ./deploy.sh') 
    }
    publishers {
        slackNotifications {
            projectChannel('general')
            notifySuccess()
            notifyBuildStarted()
            notifyAborted()
            notifyFailure()
            notifyNotBuilt()
            notifyUnstable()
            notifyBackToNormal()
        }
    }
}

job('puppet-update') {
    steps {
       shell('') 
    }
}
