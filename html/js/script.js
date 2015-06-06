webiopi().ready(init);

function init(){
		
		//bind mode button to togglemode function
		$("#mode").on("click",toggleMode);
		
		setInterval(updateUI,5000);
			              
       		 };

	function updateUI(){
		setHours();
		//updateAuto();
		getUpdate();
		//getLounge();
		//getHall();
		}
	
	function setHours(){
		webiopi().callMacro("getLightHours",[],updateLightHours);
		}
		
	function updateAuto(){
		var args=[];
		webiopi().callMacro("autoManual",args,modeCallBack);
		}	
	
	function toggleMorning(){
		if($("#morning").is(":checked")){
			var val="true";
			}
		else{
			var val="false";
		}
		webiopi().callMacro("morningLights",val);
	}

	function getUpdate(){
		webiopi().callMacro("update",[],updateReturn)

		}

	function modeCallBack(toggleAuto,args,response){
		if (response=="MANUAL"){
			$("#mode").css("background-color","Blue");
			$("#mode").text("MANUAL");}
		else if (response=="AUTO"){
		$("#mode").css("background-color","Red");
		$("#mode").text("AUTO");}
		}

	function updateReturn(macro, args, response){
		var togs=response.split(":");
		if(togs[0]=='1'){
			$("#morning").prop("checked",true);}
		else{
			$("#morning").prop("checked",false);}
		if (togs[1]=='1'){
			$("#random").prop("checked", true);}
		else{
			$("#random").prop("checked",false);}
		}
		modeCallBack(null,null,togs[2]);
		setLounge(null,null,togs[3]);
		setHall(null,null,togs[4]);
		


	function getLounge(){
		webiopi().callMacro("sendLounge",[],setLounge)}

	function setLounge(sendLounge,args,response){
		if (response=="1"){
			$("#lounge").prop("class","ON");
			}
		else{$("#lounge").prop("class","OFF");}
		}

	function getHall(){
		webiopi().callMacro("sendHall",[],setHall)}

	function setHall(sendHall,args,response){
		if (response=="1"){
			$("#hall").attr("class","ON");}
		else{$("#hall").attr("class","OFF");}
		}


	function toggleRandom(){
		webiopi().callMacro("toggleRandom");
		}


	//define function to update the auto on off times from python and switch to auto after it is run
	function updateLightHours(macro,args,response){
		var hours=response.split(":");
		$("#onTime").text("On:  "+hours[0]+":"+hours[1]);
		$("#offTime").text("Off: "+hours[2]+":"+ hours[3]);
		$("#sendButton").prop("class","STATIC");
					}

	//create sendButton
	function callSendButton(){
		$("#sendButton").attr("class","ON");
		var hours=[$("#inputOn").val(),$("#inputOnMin").val(),$("#inputOff").val(),$("#inputOffMin").val()];
		webiopi().callMacro("setLightHours",hours,updateLightHours);
		}
			

	
	function toggleMode(){
		var args=[]
		webiopi().callMacro("toggleAuto",args,modeCallBack);
		}	

	

	function resetOnOff(){
	$("#all").attr("class","NEUTRAL");
		}

        
	function toggleLounge(){
		if($("#lounge").attr("class")=="ON"){
			var args=[1,1];
			webiopi().callMacro("lightoff",args,offCallBack);
			}
		else{
			var args=[1,1];
			webiopi().callMacro("light",args,onCallBack);
			}
		}

	
	function onCallBack(){
		$("#lounge").attr("class","ON");
		resetOnOff();
}
	function offCallBack(){
		$("#lounge").attr("class","OFF");
		resetOnOff();
}

	function toggleHall(){
		if($("#hall").attr("class")=="ON"){
			var args=[1,2];
			webiopi().callMacro("lightoff",args,hallOffCallBack);
			}
		else{
			var args=[1,2];
			webiopi().callMacro("light",args,hallOnCallBack);
			}
		}

	function hallOnCallBack(){
		$("#hall").attr("class","ON");
		resetOnOff();
}
	function hallOffCallBack(){
		$("#hall").attr("class","OFF");
		resetOnOff();
}

	function toggleAll(){
		if($("#all").attr("class")=="ON"){
			var args=[2];
			webiopi().callMacro("allOff",args,alloffCallBack);
			}
		else{
			var args=[2];
			webiopi().callMacro("allOn",args,allonCallBack);
			}
		}  
	
	function allonCallBack(){
		$("#lounge").attr("class","ON");
		$("#hall").attr("class","ON");
		$("#all").attr("class","ON");
		
			}

	function alloffCallBack(){
		$("#lounge").attr("class","OFF");
		$("#hall").attr("class","OFF");
		$("#all").attr("class","OFF");
		}

