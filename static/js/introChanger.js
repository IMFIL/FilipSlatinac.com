
var wordArray = ["Innovation", "Statistics", "Technology"];

function changeWord (index){
	jQuery("#UpdatedText").fadeOut(function(){
		jQuery(this).text(wordArray[index]).fadeIn();
	});
}

function niceFading(){
	setTimeout(function(){
	jQuery("#UpdatedText").fadeOut();
},2500*(wordArray.length));

setTimeout(function(){
	jQuery("#DrivenByText").fadeOut();
},2500*(wordArray.length));

setTimeout(function(){
	jQuery("#DrivenByText").text("Software Engineering student at Uottawa").fadeIn();
},2500*(wordArray.length) + 900);

}

function initiateFading(){
	for(var i=0; i < wordArray.length; i++){
	(function(i){
			setTimeout(function(){changeWord(i)},i*2500);
	})(i);
}

	niceFading();
}
