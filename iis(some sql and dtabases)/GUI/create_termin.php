<?php
    require "common.php";
	require "services.php";
	
	$zkr = $_GET['zkratka'];
?>
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

        <h1 class="info-text"> Creating new termin</h1>
        <div class="row">
            <div class="col-sm-7"> 
                <div class="form-group has-success">
                    <form action="termin_insert.php" id="courseForm" method="get">
                        <input type="hidden" name="zkr_input" value="<?php echo $zkr; ?>" />
						<!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">* Name:</span>
                            <input type="text" class="form-control " placeholder="Name" id="Name_input" name="Name_input" required>
                        </div>
                        <div id="name_error" class="text-danger hide">Name is empty.</div>
                        
                        <div class="input-group">
                        <!--     *****************     -->
                            <span class="input-group-addon">Typ:</span>
                            <!--     FILIP TODO     -->
                            <input type="text" placeholder="Lecture, test, demo..." class="form-control" id="termin_typ" name="termin_typ">
                        </div>

                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Description:</span>
                            <input type="text" class="form-control " placeholder="Description..." id="Popis_input" name="Popis_input">

                        </div>

                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Date</span>
                            <input type="date" class="form-control" id="Date_input" name="Date_input">
                        </div>
						
						<div class="input-group">
                            <span class="input-group-addon">Start(time)</span>
                            <input type="time" class="form-control" id="start_input" name="start_input">
                        </div>
						
						<div class="input-group">
                            <span class="input-group-addon">End(time)</span>
                            <input type="time" class="form-control" id="end_input" name="end_input">
                        </div>


                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">* Room:</span>
                            <select class="form-control" name="mistnost_input">
							<?php
								$serv = new Service();
								$rooms = $serv->getRooms();
								while ($row = $rooms->fetch())
								{
									echo "<option value=\"" . $row['nazev'] . "\">" . $row['nazev'] . "</option>";
								}
							?>
                            </select>
                        </div>
						
						<div class="input-group">
                            <span class="input-group-addon">* Lector:</span>
                            <select class="form-control" name="lector_input">
							<?php
								$users = $serv->getUsers();
								while ($row = $users->fetch())
								{
									if (checkUser($row['typ']) >= 1) 
									{
										echo "<option value=\"" . $row['login'] . "\">" . $row['login'] . "</option>";
									}
								}
							?>
                            </select>
                        </div>

                        <input  type='submit' 
                            class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                            style="margin:5px;"
                            name='make_registration_course'
                            value='Create term'/>

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
                        onclick='location.replace("detailed_course.php<?php echo "?zkratka=$zkr" ?>");'
                        name='login_btn' 
                        value='Back to course'/> 
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
