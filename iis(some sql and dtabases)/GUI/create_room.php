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

        <h1 class="info-text"> Creating new room</h1>
        <div class="row">
            <div class="col-sm-7"> 
                <div class="form-group has-success">

                    <form action="add_room_db.php" id="roomCreateForm" method="get">
					<?php header('Content-type: text/html; charset=utf-8'); ?>
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">* Name:</span>
                            <input type="text" class="form-control " placeholder="Name..." id="Name_input" name="Name_input" required>
                        </div>
                        
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">* Type:</span>
                            <input type="text" class="form-control" placeholder="Lecture..." id="Type_input" name="Type_input" required>
                        </div>

                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Capacity:</span>
                            <input type="text" class="form-control" placeholder="50..." id="Capacity_input" name="Capacity_input" required>
                        </div>

                        <input  type='submit' 
                            class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                            style="margin:5px;"
                            onclick="location.replace('rooms.php');"
                            name='make_registration_course'
                            value='Create room'/>

                    </form>

                    <div class="wizard-footer height-wizard">
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
    </div>
</div>

</body>
<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>

<script>
    function checkData(){ // check login validity and when ok, move page
        if( Name_input.value === "" || Abbreviation_input.value === ""  || Garant_input.value === "" ){
            $("#creating_alert").show('fade');    // fade shows alert smoothly
        }
        
        if(Name_input.value === "" ){
            $("#name_error").removeClass('hide');
        }
        else{
            $("#name_error").addClass('hide');
        }

        if(Abbreviation_input.value === "" ){
            $("#abbreviation_error").removeClass('hide');
        }
        else{
            $("#abbreviation_error").addClass('hide');
        }

        if(Garant_input.value === "" ){
            $("#login_error").removeClass('hide');
        }
        else{
            $("#login_error").addClass('hide');
        }
    }
</script>

</html>
