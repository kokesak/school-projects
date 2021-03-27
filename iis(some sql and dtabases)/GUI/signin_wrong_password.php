<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
	<meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' name='viewport' />
    <meta name="viewport" content="width=device-width" />

    <link href="http://netdna.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.css" rel="stylesheet">
    <link href="assets/css/bootstrap.min.css" rel="stylesheet" />
	<link href="assets/css/gsdk-bootstrap-wizard.css" rel="stylesheet" />
</head>

<body>
<div class="image-container set-full-height" style="background-image: url('assets/img/main_screen.jpg')">
    <div class="container">
        <div class="row">
            <div class="col-sm-8">  <!--  White screen length  -->
                
                <div class="alert alert-danger" id="log_in_alert">   <!-- collapse hide alert ath the begining -->
                    <strong> Error!</strong> Login or Password is wrong! Please try it again.
                    <input type='button' class='btn-dark btn-fill text-danger pull-right' onclick="$('#log_in_alert').hide('fade');" name='hide_alert_btn' value='X'/>
                </div>
                
                
                <div class="wizard-container">
                    <div class="card wizard-card " data-color="orange" id="wizardProfile" >
                    
                    <form action="login.php" method="post">
                        <div align="left", class="tab-content">
                            <div class="row">
                                <h2 class="info-text"> School information system</h2>
                                <div class="col-sm-1"></div>    <!--     Loging/password shift     -->
                                <div class="col-sm-6">          <!--     Loging/password shift     -->
                                    
                                    <div class="form-group">
                                        <label>* Login</label>
                                        
                                        <input name="login" type="text" class="form-control" placeholder="login" id="Login_input" name="Login_input" required>
                                        <div id="log_in_error" class="text-danger "> <!--     Error login input     -->
                                            Wrong or empty login.
                                        </div>

                                        <label>* Password</label>
                                        
                                        <input name="password" type="password" class="form-control" id="Password_input" placeholder="******" name="Password_input" required>
                                        <div id="password_error" class="text-danger "> <!--     Error password input     -->
                                                Wrong or empty password.
                                        </div>
                                        <input type="checkbox" onclick="myFunction()"> Show Password
                                    </div>

                                </div>
                                <div class="col-sm-10 col-sm-offset-1"></div>
                            </div>
                        </div>
                        <div class="wizard-footer height-wizard">
                            <input type='submit' 
                                   class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                                   style="margin:5px;" 
                                   onclick=""
                                   name='login_btn' value='Login' /> 
                        </div>
                        </form>
                        <div class="wizard-footer height-wizard">
                            <input type='button' 
                                    class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                                    style="margin:5px;"  
                                    onclick="location.replace('registration.php');"
                                    name='make_registration'
                                    value='Create account' />
                                
                            <input type='button' 
                                    class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                                    style="margin:5px;" 
                                    onclick="location.replace('index.php');"
                                    name='login_btn' value='Back to menu' /> 
                        </div>
                    </div>
                </div> 
            </div>
        </div>
    </div> 
</div>

</body>
	<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
	<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
	<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>
    <script>
        function myFunction() {
            var doc = document.getElementById("Password_input");
            if (doc.type === "password") {
                doc.type = "text";
            } 
            else {
                doc.type = "password";
            }
        }
    </script>

    <script>
        function changePage(page_addr){ // check login validity and when ok, move page

            if(login_input.value === "" || Password_input.value === ""){
                $("#log_in_alert").show('fade');    // fade shows alert smoothly
            }
            else{
                location.replace(page_addr);
            }
        }
    </script>

	<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
	<script src="assets/js/jquery.validate.min.js"></script>
</html>
