names = [];


function addBackGroundImages(){
	for(var i=0;i<names.length;i++){

		if(names[i] == "cookR"){
			$("#"+names[i]).css("background","url(/static/"+names[i]+"Picture"+".png) 50% 50% / 0% 0% no-repeat");
			$("#"+names[i]).css("background-size","50% 100% ");
		}

		else{
			$("#"+names[i]).css("background","url(/static/"+names[i]+"Picture"+".png) no-repeat");
			$("#"+names[i]).css("background-size","100% 100%");
		}

	}
}

$.ajax({
	url:"/repos"
}).done(function(data){
	for(var key in data.names){
		names.push(data.names[key]);
	}
	addBackGroundImages();
});