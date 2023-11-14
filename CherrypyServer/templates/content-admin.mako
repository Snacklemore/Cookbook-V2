<%inherit file="base.mako"/>
	


<%block name="PdfView">
	<script src="static/js/pdfView.js"></script>
	<div hidden="hidden" id="admin-content"> </div>
	
	 <!-- <iframe id="iframe1" width="1200" height="600"> </iframe>-->
	 <div id="container">
		<div id="pdfContainer">
			<div id="controls">
				<button onclick="prevPage()">Previous</button>
				<span>Page: <span id="page_num"></span> / <span id="page_count"></span></span>
				<button onclick="nextPage()">Next</button>+
				<form method="post" action="http://192.168.178.26:8080/uploadPDF" enctype="multipart/form-data">
    				<input type="file" name="ufile" />
    				<input type="submit" />
				</form>
				
			</div>
			<canvas id="the-canvas"></canvas>
		</div>

		<div id="other">
			<div class="row">
              <div class="col s12">
                <ul class="collection">
                </ul>
              </div>
            </div>
        </div>

		</div>
	 </div>
</%block>
