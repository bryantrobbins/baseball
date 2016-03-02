npm install -g hubot coffee-script
npm install -g yo generator-hubot
rm -rf batboy
mkdir batboy
cd batboy
npm install hubot-slack
npm install jenkins-api
yo hubot --name="batboy" --owner="Nobody" --description="Test bot" --adapter=slack --defaults
export express_port={port used by hubot}
export HUBOT_SLACK_TOKEN={token associated with bot when set up using slack}
export HUBOT_SLACK_TEAM={team name}
export HUBOT_SLACK_BOTNAME={name for bot set up using slack}
export HUBOT_LOG_LEVEL=debug
cp ../scripts/* scripts
./bin/hubot --adapter slack