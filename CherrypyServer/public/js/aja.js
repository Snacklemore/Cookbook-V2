var messages;
$(document).ready(function () {
	//create account enter event
	
	
	
	//login enter event
	
       $("#register_btn").click(function (e) {
		   
		  var u = document.getElementById("rusername");
		 
		  console.log(u);
		  document.querySelector('.success').style.display = "none";
		  document.querySelector('.error').style.display = "none";
		  
          $.post("/register", {
			
			passphrase: $("input[id='rusername']").val(),
			
          }).done(function (retval) {
            console.log(retval);
					if (String(retval) === "success")
					{	
						window.location.replace("http://192.168.178.26:8080/content");
						//PASSPHRASE CORRECT
						/*document.querySelector('.success').style.display = "block";
						document.querySelector('.success').innerHTML = "Registration Complete!";
						            		  

						//clear input fields
						var u = document.getElementById("rusername");
						var p = document.getElementById("rpassword");
						var e = document.getElementById("email");
						
						u.value="";
						p.value="";
						e.value="";*/
					}
					else
						{
							//PASSPHRASE INCORRECT
							/*
							document.querySelector('.error').style.display = "block";
							document.querySelector('.error').innerHTML = "Registration Failed!"
							*/ 

						}
            //cherrypy return value
          });
          
        });
		
		
		

		
		
		
		
		
		
	});
	

	
	
 

	 
  