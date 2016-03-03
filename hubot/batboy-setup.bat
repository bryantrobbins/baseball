call npm install -g hubot coffee-script
call npm install -g yo generator-hubot
call rd /s /q batboy
mkdir batboy
cd batboy
call npm install hubot-slack
call npm install jenkins-api
call yo hubot --name="batboy" --owner="Nobody" --description="Test bot" --adapter=slack --defaults
set express_port={port used by hubot}
set HUBOT_SLACK_TOKEN={token associated with bot when set up using slack}
set HUBOT_SLACK_TEAM={team name}
set HUBOT_SLACK_BOTNAME={name for bot set up using slack}
set HUBOT_LOG_LEVEL=debug
xcopy /s "../scripts" "./scripts" 
./bin/hubot --adapter slack