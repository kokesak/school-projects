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
            $zkr = $_GET['zkr'];
            $data = $serv->getUser($_SESSION['user']);
            $term_id = $_GET['id'];
            $term = $serv->getTerm($term_id);
        ?>
        <div class="row" style="margin-top:2%">
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
        <div class="container mb-4 mt-4">
        <div class="col-md-offset-2 col-md-12" >
            <h1 class="info-text"> <?php echo $term['nazev'] ?> </h1>
        </div>
        <div class="col-sm-7" style="margin-left: 2%;background-color: papayawhip; padding-block: 10px;"> 
        

        <form action="submit_assessments.php?id=<?php echo "$term_id&zkr=$zkr" ?>" method="post" enctype="multipart/form-data">
            <h5>Students enrolled in course:</h5>
            <?php 
                echo "<table>";
                $logins = $serv->getLoginInCourses($zkr);
                foreach ($logins as $tmp) {
                    $value = $tmp['login'];
                    echo "<tr>";
                    echo "<td>$value</td>";
                    echo "<td><input type=\"number\" class=\"form-control\" name=\"$value\" style=\"display: inline; width: 100px; margin-left:15px \" placeholder=\"0\"></td>";
                    echo "<tr>";
                  }
                  echo "</table>";

            
            ?>
            <input type="submit" style="margin-top: 10px" value="Submit assessments">
        </form>
        </div>
        <div class="col-sm-7" style="margin-left: 2%;background-color: papayawhip; padding-block: 10px;">
        </div>
        </div>
        </div>
        

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>

</html>
