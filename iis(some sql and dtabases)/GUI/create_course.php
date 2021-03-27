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

        <h1 class="info-text"> Creating new course</h1>
        <div class="row">
            <div class="col-sm-7"> 
                <div class="form-group has-success">
                    <form action="course_insert.php" id="courseForm" method="get">
					<?php header('Content-type: text/html; charset=utf-8'); ?>
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">* Name:</span>
                            <input type="text" class="form-control " placeholder="Information Technology" id="Name_input" name="Name_input" required>
                        </div>
                        <div id="name_error" class="text-danger hide">Name is empty.</div>
                        
                        
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">* Abbreviation:</span>
                            <input type="text" class="form-control" placeholder="IT" id="Abbreviation_input" name="Abbreviation_input" required>
                        </div>
                        <div id="abbreviation_error" class="text-danger hide">Abbreviation is empty.</div>


                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Price:</span>
                            <input type="text" class="form-control" placeholder="0 kc" id="Price_input" name="Price_input" required>
                        </div>

                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Tag1:</span>
                            <input type="text" class="form-control" placeholder="Tag_1" id="Tag1_input" name="Tag1_input">
                        </div>


                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Tag2:</span>
                            <input type="text" class="form-control" placeholder="Tag_2" id="Tag2_input" name="Tag2_input">
                        </div>


                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Tag3:</span>
                            <input type="text" class="form-control" placeholder="Tag_3" id="Tag3_input" name="Tag3_input">
                        </div>

                        <input  type='submit' 
                            class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                            style="margin:5px;"
                            name='make_registration_course'
                            value='Create course'/>

                    </form>

                    <div class="wizard-footer height-wizard">
                    <input type='button' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                        style="margin:5px;" 
                        onclick="location.replace('index.php');"
                        name='login_btn' 
                        value='Back to menu'/>
                    <input type='button' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                        style="margin:5px;" 
                        onclick="location.replace('courses.php');"
                        name='login_btn' 
                        value='Back to courses'/> 
                </div>
            </div>    
                </div>
                <div class="col-sm-3">
                    <textarea rows="4" cols="50" name="description" id="desc" form="courseForm" placeholder="Description..."></textarea>
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
