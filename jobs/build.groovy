job('r-baseball') {
    scm {
        git('git://github.com/bryantrobbins/r-baseball')
    }
    steps {
       shell('chmod *.sh; ./build.sh') 
    }
}
