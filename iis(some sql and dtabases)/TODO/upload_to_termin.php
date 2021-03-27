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
    <div class="container" >
            
        <div class="alert alert-success collapse" id="creating_alert">   <!-- collapse hide alert ath the begining -->
            <strong> Success!</strong> Changes were saved.
            <<input type='button' class='btn-dark btn-fill text-success pull-right' onclick="$('#creating_alert').hide('fade');" name='hide_alert_btn' value='X'/>
        </div>
        <?php
            $serv = new Service();
            $data = $serv->getUser($_SESSION['user']);
        ?>
        <h1 class="info-text"> Termin kokot</h1>
        <div class="col-sm-7" style="margin-left: 2%;background-color: papayawhip; padding-block: 10px;"> 
        

        <form action="upload.php" method="post" enctype="multipart/form-data">
            Select File to upload:
        <input type="file" name="fileToUpload" id="fileToUpload">
            <input type="submit" value="Upload File" name="submit">
        </form>
        </div>
        <div class="col-sm-7" style="margin-left: 2%;background-color: papayawhip; padding-block: 10px;">
        <h2 class="info-text"> Soubory k terminu</h2>
        <?php
            $dir = "uploads/";
            $a = scandir($dir);
            for($i = 2;$i<count($a);$i++){
                echo "<a href=\"uploads/".$a[$i]."\" download>";
                echo "<img href=\"uploads/".$a[$i]."\" src=\"assets/img/file_logo.jpg\" alt=\"file\" width=\"25\" height=\"25\">";
                echo "</a>";
                echo "<a href=\"uploads/".$a[$i]."\" download>" . $a[$i] . "</a>";
                echo "<br>";
            }
            
            ?>
        </div>
        <div class="col-sm-7" style="margin-left: 2%;">
            <input type='button' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                        style="margin:5px;" 
                        onclick="location.replace('index.php');"
                        name='login_btn' 
                        value='Back to menu'/>   
            <input type='button' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                        style="margin:5px;" 
                        onclick="location.replace('detailed_course.php');"
                        name='login_btn' 
                        value='Back to course'/>   
        </div>

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>

</html>
