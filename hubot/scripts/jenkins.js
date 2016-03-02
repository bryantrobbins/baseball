var jenkinsapi = require('jenkins-api');
var url = process.env.jenkinsUrl;
var jenkins = jenkinsapi.init(url);
var colorMap = {'red':'Failed', 'blue':'Passed', 'yellow':'Unstable', 'notbuilt':'Never built'}

module.exports = function(robot){
	robot.hear(/list jobs/i,function(res){
		jenkins.all_jobs(function(err,data){
			if(err){
				console.log("Err "  + err);
				res.send("bombed out " + err);
			}else{
				var jobs =data;
				var result='';
				jobs.forEach(function(job){
					result+='Job Name: ' + job.name + '\r\n';
					result+='Url: ' + job.url + '\r\n';
					var color = job.color.replace('_anime','');
					result+='Last build status: ' + colorMap[color] + '\r\n';
					if(job.color.indexOf('_anime')>-1){
						result+='**Build in Progress**\r\n';
					}
					result+='\r\n';
				});
				res.send(result);
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