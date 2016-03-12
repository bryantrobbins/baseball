var memes={};
var get_memes='https://api.imgflip.com/get_memes';
var generate_memes='https://api.imgflip.com/caption_image';
var request = require('request');

var get_all_memes = {
		    url: get_memes,
		    method: 'GET'
		  	
		};

var create = {
		url: generate_memes,
		method: 'POST',
		form: {username: 'imgflip_hubot',
       password: 'imgflip_hubot',
       template_id:'?',
       text0:'', text1:''}

};

var responseUrl;
module.exports = function(robot){
	request(get_all_memes, function (error, response, body) {
		    if (!error && response.statusCode == 200) {
		       var stuff = JSON.parse(body);
		       stuff.data.memes.forEach(function(meme){
		       		memes[meme.name]=meme.id;

				});
		    }
		});


	robot.hear(/generate (.*) with top:(.*) and bottom:(.*)/i,function(mes){
		console.log("Match !" + mes.match[1] +'!');
		
		
		create.form.template_id= memes[mes.match[1]];
		create.form.text0= mes.match[2];
		create.form.text1= mes.match[3];

		request(create, function (error, response, body) {
			console.log(create);
		    if (!error && response.statusCode == 200) {
		       var stuff = JSON.parse(body);
		      	robot.messageRoom('#general',stuff.data.url);

		    }
		});
			

	});

	

	

}	

