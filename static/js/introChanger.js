
var wordArray = ["Innovation", "Statistics", "Technology"];

function changeWord (index){
	$("#UpdatedText").fadeOut(function(){
		$(this).text(wordArray[index]).fadeIn();
	});
}

function niceFading(){
	setTimeout(function(){
	$("#UpdatedText").fadeOut();
},2500*(wordArray.length));

setTimeout(function(){
	$("#DrivenByText").fadeOut();
},2500*(wordArray.length));

setTimeout(function(){
	$("#DrivenByText").text("Software Engineering student at Uottawa").fadeIn();
},2500*(wordArray.length) + 900);

}


for(var i=0; i < wordArray.length; i++){
	(function(i){
			setTimeout(function(){changeWord(i)},i*2500);
	})(i);
}

niceFading();