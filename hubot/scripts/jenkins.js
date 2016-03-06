var jenkinsapi = require('jenkins-api');
var url = process.env.jenkinsUrl;
var jenkins = jenkinsapi.init(url);
var colorMap = {'red':'Failed', 'blue':'Passed', 'yellow':'Unstable', 'notbuilt':'Never built', 'aborted':'Aborted'}

module.exports = function(robot){
	robot.hear(/list jobs/i,function(res){
		jenkins.all_jobs(function(err,data){
			if(err){
				console.log("Err "  + err);
				res.send("bombed out " + err);
			}else{
				var jobs =data;
				var result='\r\n';
				var fields = [];
				var jobNames = {"title":"Jobs", "short":true, "value":""}
				//var urls = {"title":"Urls", "short":true, "value":""}
				var builds = {"title":"Last Build", "short":true, "value":""}
				var inProg = {"title":"Build In Progress?", "short":true, "value":""}
				
			
				jobs.forEach(function(job){
					var color = job.color.replace('_anime','');

					
					jobNames.value+='<' + job.url + '|'+job.name+'>\n';
					builds.value+=colorMap[color]+'\n';
					inProg.value+=(job.color.indexOf('_anime')>-1)+'\n';
					
				});
				fields.push(jobNames);
				fields.push(builds);
				fields.push(inProg);
				var attachments=[];
				var content = {"fallback":"Builds", "color": "#36a64f", "pretext": "Here are all the jobs",
"fields":fields}
				attachments.push(content);
				var payload ={"message":res.message,"content":attachments, "channel":  "#general"
};
				robot.emit('slack-attachment', payload);
			}
		});
		
	});
	
	robot.hear(/build (.*)/i,function(res){
		jenkins.build(res.match[1],function(err,data){
			if(err){
				res.send("Errored on building job: " + err);
			}else{
				res.send(JSON.stringify(data));
			}
		});
	});

}	