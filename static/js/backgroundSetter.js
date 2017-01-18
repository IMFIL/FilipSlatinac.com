names = [];


function addBackGroundImages(){
	for(var i=0;i<names.length;i++){

		if(names[i] == "cookR"){
			jQuery("#"+names[i]).css("background","url(/static/"+names[i]+"Picture"+".png) 50% 50% / 0% 0% no-repeat");
			jQuery("#"+names[i]).css("background-size","50% 100% ");
		}

		else{
			jQuery("#"+names[i]).css("background","url(/static/"+names[i]+"Picture"+".png) no-repeat");
			jQuery("#"+names[i]).css("background-size","100% 100%");
		}

	}
}

jQuery.ajax({
	url:"/repos"
}).done(function(data){
	for(var key in data.names){
		names.push(data.names[key]);
	}
	addBackGroundImages();
});

jQuery(".IntroPage").css("background","url(/static/coding.jpg) no-repeat center center fixed");
jQuery(".LeftSidePicture").css("background","url(/static/workStation.jpg) no-repeat center center fixed");

jQuery(".LeftSidePicture").css("-moz-background-size","cover");
jQuery(".LeftSidePicture").css("-webkit-background-size","cover");
jQuery(".LeftSidePicture").css("background-size","cover");

