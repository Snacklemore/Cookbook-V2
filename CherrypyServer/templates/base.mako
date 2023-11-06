<html>
    <head>
		<meta charset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title> |CookBook V2 (ALPHA)| </title>
		<link href="/static/css/style.css" rel="stylesheet">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

		<script src="https://code.jquery.com/jquery-2.0.3.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/1.0.0/anime.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    
    <script src="static/js/pdf.js"></script>
		<script src="static/js/aja.js"></script>
    
		<meta http-equiv="cache-control" content="no-cache" />
		
    <style>
    #toTopBtn {
      display: none;
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 99;
    }

    #toTopBtn i {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
    }
  </style>
		
		
		
		
		
    </head>
    <body>
		
		<div class="topnav">
		  <a href="#contact">Contact</a>
		  <a href="#about">About</a>
		</div>
		<!--Index block-->
        <div class="header">
            <%block name="header"/>
        </div>
		<div class="chat">
    <button onclick="topFunction()" id="toTopBtn" class="btn-floating btn-large red">
                  <i class="material-icons">arrow_upward</i>
            </button>
            <%block name="PdfView"/>
            
            
		
	
	
         <footer class="site-footer">
      <div class="container">
        <div class="row">
          <div class="col-sm-12 col-md-6">
            <h6>About</h6>
            <p class="text-justify">github.com/Snacklemore <i>CODE WANTS TO BE SIMPLE </i>.</p>
          </div>

          

          <div class="col-xs-6 col-md-3">
            <h6>Quick Links</h6>
            <ul class="footer-links">
              
              
              <li><a href="">Contribute</a></li>
              <li><a href="">Privacy Policy</a></li>
              
            </ul>
          </div>
        </div>
        <hr>
      </div>
      <div class="container">
        <div class="row">
          <div class="col-md-8 col-sm-6 col-xs-12">
            <p class="copyright-text">Copyright &copy; 2017 All Rights Reserved by 
         <a href="#">Snacklemore</a>.
            
			
			</p>
          </div>

          
        </div>
      </div>
</footer>
		
		
    </body>
	<!-- Site footer -->
   
</html>