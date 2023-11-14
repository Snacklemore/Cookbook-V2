function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
    }
    
    var pageNum = 1;
    var pageRendering = false;
    var pageNumPending = null;
    var scale = 1.5;
    var pdfDoc = null;
    var canvas  = null;
    var ctx = null;
    var controls = null;
    

    function renderPage(num) {
        pageRendering = true;
        // Using promise to fetch the page
        pdfDoc.getPage(num).then(function(page) {
          var viewport = page.getViewport({ scale: scale });
          canvas.height = viewport.height*1.6;
          canvas.width = viewport.width;
      
          // Render PDF page into canvas context
          var renderContext = {
            canvasContext: ctx,
            viewport: viewport
          };
          var renderTask = page.render(renderContext);
      
          // Wait for rendering to finish
          renderTask.promise.then(function() 
          {
                pageRendering = false;
                if (pageNumPending !== null) 
                {
                // New page rendering is pending
                renderPage(pageNumPending);
                pageNumPending = null;
                }
          });

        });
      
        // Update page counters
        document.getElementById('page_num').textContent = num;
    }

    function queueRenderPage(num)
    {
        if (pageRendering){
            pageNumPending = num;

        }else
        {
            renderPage(num);
        }
    }


    function prevPage()
    {
        if(pageNum <= 1 )
        {
            return;
        }
        pageNum--;
        queueRenderPage(pageNum);
    }


    function nextPage()
    {
        if ( pageNum >= pdfDoc.numPages)
        {
            return;
        }
        pageNum++;
        queueRenderPage(pageNum);
    }


    function uploadFile() {
        var input = document.getElementById('fileInput');
        var file = input.files[0];
        var formData = new FormData();
        formData.append('file', file);

        // You can use fetch or XMLHttpRequest to send the formData to the server
        // For example, using fetch:
        fetch('/pdf', {
            method: 'POST',
            body: formData
          })
          .then(response => response.json())
          .then(data => {
            console.log('File uploaded successfully', data);
          })
          .catch(error => {
            console.error('Error uploading file', error);
          });
        
    }

$(document).ready(function () {
    
    // Get the button
    var mybutton = document.getElementById("toTopBtn");
    canvas = document.getElementById('the-canvas');
    ctx = canvas.getContext('2d');
    var pdfContainer = document.getElementById('pdfContainer');

    controls = document.getElementById('controls');
    controls.style.textAlign = 'center';
    controls.style.marginBottom = '10px';
    controls.style.padding = '10px';
    controls.style.backgroundColor = '#f2f2f2';
    controls.style.position = 'sticky';
    controls.style.top = '0';

    // Style for the pdf container
    pdfContainer.style.position = 'absolute';
    pdfContainer.style.top = '0';
    pdfContainer.style.left = '0';
    pdfContainer.style.width = '100%';
    pdfContainer.style.height = '100%';
    pdfContainer.style.overflow = 'auto';

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function() {
    scrollFunction();
    };

    function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
    }

    // When the user clicks on the button, scroll to the top of the document
    function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
    }    
    
    
    


    $.get("/pdf", {
        type: "all",
        id: -1,
        
        
    
        }).done(function (retval) {
            var iframe = document.getElementById("iframe1");
            //iframe.hidden  = true;
            var responseList = JSON.parse(retval);
            console.log(retval);
            console.log(responseList[0])
            console.log(responseList[1])
            //build button list with this data 
            //--> Button Click on recept triggers download through REST api 
            //--> NOTE: we should work with recept IDs not names
            function sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
              }
            

            // Creating buttons dynamically
            for (var i = 1; i <= responseList.length; i++) {
                (function (i) {
                    sleep(500).then(()=> {
                        var li = document.createElement("li");
                        li.classList.add("collection-item");

                        var deleteButton = null;
                        var createDeleteButton = true;
                        //check if admin html was served
                        var admin_div = document.getElementById("admin-content");
                        admin_div.innerHTML = "Content" ;
                        if (admin_div === null)
                        {
                            createDeleteButton = true;
                        }
                        
                        if (createDeleteButton)
                        {
                            console.log("Creating delete buttons")
                            deleteButton = document.createElement("a");
                            deleteButton.classList.add("waves-effect", "waves-light", "btn");
                            deleteButton.id = "delete_button" + i;
                            deleteButton.innerHTML = "Delete";
                            var recipeID = responseList[i-1][1]
                            deleteButton.addEventListener("click", function() {

                                //delete request to server (admin auth required)
                                $.ajax({
                                    url: '/pdf' + '?' + $.param({"id": recipeID}),
                                    type: 'DELETE',
                                    success: function(result) {
                                        // Do something with the result
                                        location.reload();
                                    }
                                });

                            });
                            li.appendChild(deleteButton);

                        }

                       
                        var button = document.createElement("a");
                        button.classList.add("waves-effect", "waves-light", "btn");
                        button.id = "button" + i;
                        button.innerHTML = responseList[i-1][0];
                        button.addEventListener("click", function() {
    
                            //alert("Button " + i + " clicked!");
                            //get pdf data
                            //var iframe = document.getElementById("iframe1");
                            pageNum = 1;
                            let xhr = new XMLHttpRequest;
                            xhr.open('get', '/pdf?type=all&id='+ responseList[i-1][1], true);
                            xhr.responseType = 'arraybuffer';
                            xhr.onload = function(e) {
                                let content = this.response;
                                let blob = new Blob([content], {type: 'application/pdf'});
                                let url = URL.createObjectURL(blob);

                                var loadingTask = pdfjsLib.getDocument(url);
                                loadingTask.promise.then(function(pdfDoc_){
                                    pdfDoc = pdfDoc_;
                                    document.getElementById('page_count').textContent = pdfDoc.numPages;
                                    renderPage(pageNum);
                                    
                                },function (reason){
                                    console.error(reason);
                                });
                                
                                //iframe.onload = function(e) {
                               //     console.log(e);
                               // };
                               // iframe.src = url;
                                //iframe.hidden = false;
                            };
                            xhr.send();
    
    
                        });
                        var pdf_list = document.getElementsByClassName("chat");
                        li.appendChild(button);
                        document.querySelector(".collection").appendChild(li);
                        //pdf_list[0].append(button);
                        
                    })
                    
                  })(i);
            }

    
    });

   
		
		
		

		
		
		
		
		
		
	});