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
    <div class="container" >
            
        <div class="alert alert-danger collapse" id="creating_alert">   <!-- collapse hide alert ath the begining -->
            <strong> Error!</strong> Some arrays are not filled in.
            <input type='button' class='btn-dark btn-fill text-danger pull-right' onclick="$('#creating_alert').hide('fade');" name='hide_alert_btn' value='X'/>
        </div>

        <h1 class="info-text"> Registrating new user</h1>
        <div class="col-sm-7"> 
            <div class="form-group has-success">
                <form action="account_insert.php" method="get">
				<?php header('Content-type: text/html; charset=utf-8'); ?>
                      
                    <!--     *****************     -->
                    <div class="input-group">
                        <span class="input-group-addon">* Name:</span>
                        <input type="text" class="form-control " placeholder="Insert maximal 30 characters. Longer names will be concatenated."
                               id="Name_input" name="Name_input" required  maxlength="30"/>
                    </div>
                    <div id="name_error" class="text-danger hide">Name is empty.</div>
                    
                    
                    <!--     *****************     -->
                    <div class="input-group">
                        <span class="input-group-addon">* Surname:</span>
                        <input type="text" class="form-control" placeholder="Novak" id="Surname_input" name="Surname_input" required/>
                    </div>
                    <div id="surname_error" class="text-danger hide">Surname is empty.</div>

                    
                    <!--     *****************     -->
                    <div class="input-group">
                        <span class="input-group-addon">Date of birth:</span>
                        <input type="date" class="form-control" id="Date_input" name="Date_input">
                    </div>

                    
                    <!--     *****************     -->
                    <div class="input-group">
                        <span class="input-group-addon">* Login:</span>
                        <input type="text" class="form-control" placeholder="login" id="Login_input" name="Login_input" required/>
                    </div>
                    <div id="login_error" class="text-danger hide ">Login is empty.</div>


                    <!--     *****************     -->
                    <div class="input-group">
                        <span class="input-group-addon">* Password:</span>
                        <input type="text" class="form-control" placeholder="******" id="Password_input" name="Password_input" required/>
                    </div>
                    <div id="password_error" class="text-danger hide ">Password is empty.</div>


                    <!--     *****************     -->
                    <div class="input-group">
                        <span class="input-group-addon">* Conf. password:</span>
                        <input type="text" class="form-control" placeholder="******" id="Conf_password_input" name="Conf_password_input" required/>
                    </div>

                    <div id="conf_password_error" class="text-danger hide "> Password is empty.</div>
                    <div id="no_pass_match_error" class="text-danger hide ">Password are not same.</div>
                    <input  type='submit' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                        style="margin:5px;"
                        onclick="checkData();"
                        name='make_registration'
                        value='Create account'/>
                </form>
            
                <input type='button' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                        style="margin:5px;" 
                        onclick="location.replace('index.php');"
                        name='login_btn' 
                        value='Back to menu'/> 
                </div>
        </div>
    </div>
</div>

</body>
<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>

<script>
    function checkData(){ // check login validity and when ok, move page
        if( Name_input.value === "" || Surname_input.value === ""  || Login_input.value === "" ||
            Password_input.value === ""  || Conf_password_input.value === "" ){
            $("#creating_alert").show('fade');    // fade shows alert smoothly
        }
        
        if(Name_input.value === "" ){
            $("#name_error").removeClass('hide');
        }
        else{
            $("#name_error").addClass('hide');
        }

        if(Surname_input.value === "" ){
            $("#surname_error").removeClass('hide');
        }
        else{
            $("#surname_error").addClass('hide');
        }

        if(Login_input.value === "" ){
            $("#login_error").removeClass('hide');
        }
        else{
            $("#login_error").addClass('hide');
        }

        if(Password_input.value === "" ){
            $("#password_error").removeClass('hide');
        }
        else{
            $("#password_error").addClass('hide');
        }

        if(Conf_password_input.value === "" ){
            $("#conf_password_error").removeClass('hide');
        }
        else{
            if(Conf_password_input.value !== Password_input.value ){
                $("#no_pass_match_error").removeClass('hide');
            }
            else{
                $("#no_pass_match_error").addClass('hide');
                $("#conf_password_error").addClass('hide');
            }
        }
    }
</script>
</html>
