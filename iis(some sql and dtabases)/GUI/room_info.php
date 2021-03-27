<?php
    require "common.php";
    require "services.php";
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
        <div class="container mb-4 mt-4">

            <div class="alert alert-success collapse" id="edit_alert">   <!-- collapse hide alert ath the begining -->
                <strong> Success</strong> Changes were saved!
                <input type='button' class='btn-dark btn-fill text-Successfull pull-right' onclick="$('#edit_alert').hide('fade');" name='hide_alert_btn' value='X'/>
            </div>

            <?php 
                $room_name = $_GET['mistnost']; 
                
                $serv = new Service();
                $room = $serv->getRoom($room_name);
                
                echo "<h3 > ". $room_name ." </h3>"; ?>
                
                <?php echo"<form action=\"edit_room_db.php\" method=\"get\">";

                    echo "<input type=\"hidden\" value=\"".$room_name."\" id=\"Hidden_input\" Name=\"Hidden_input\"/>";

                    echo "<div class=\"input-group\">
                        <span class=\"input-group-addon\">* Name:</span>
                        <input type=\"text\" class=\"form-control\" value=\"".$room['nazev']."\" id=\"Name_input\" Name=\"Name_input\"/>
                    </div>";
                    echo "<div class=\"input-group\">
                            <span class=\"input-group-addon\">* Type:</span>
                            <input type=\"text\" class=\"form-control\" value=\"".$room['typ']."\" id=\"Type_input\" name=\"Type_input\"/>
                        </div>";

                    echo "<div class=\"input-group\">
                        <span class=\"input-group-addon\">* Capacity:</span>
                        <input type=\"text\" class=\"form-control\" value=\"".$room['kapacita']."\" id=\"Capacity_input\" name=\"Capacity_input\"/>
                    </div>";
                ?>
                    <input  type='submit' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                        style="margin:5px;"
                        onclick="$('#edit_alert').show('fade');"
                        name='edit_room_btn'
                        value='Save changes'/>
                </form>
            <input type='button' 
                class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                style="margin:5px;" 
                onclick="location.replace('index.php');"
                name='login_btn' 
                value='Back to menu' /> 
            <input type='button' 
                class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                style="margin:5px;" 
                onclick="location.replace('rooms.php');"
                name='login_btn' value='Back to rooms' /> 
        </div>                
    </div>

</body>
<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>

</html>
