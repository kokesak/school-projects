<?php
    require "common.php";
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
            <button class="btn-lg btn-success btn-fill" 
                    onclick="location.replace('courses.php')">
                    Courses</button>
            <?php if(isset($_SESSION['user'])) { ?>
                <button class="btn-lg btn-success btn-fill"  
                        onclick="location.replace('user_timetable.php')">
                        My timetable </button>    
            <?php } ?>
            <?php if( isset($_SESSION['user']) && (checkUser($_SESSION['type']) >= 3)) { ?>
                    <button class="btn-lg btn-success btn-fill"
                            onclick="location.replace('rooms.php')">
                            Edit rooms</button>
            <?php } ?>
            <?php if( isset($_SESSION['user']) && (checkUser($_SESSION['type']) >= 2)) { ?>
                    <button class="btn-lg btn-success btn-fill"
                            onclick="location.replace('StudentsToApprove.php')">
                            Approve students </button>
            <?php } ?>
            
            <?php if( isset($_SESSION['user']) && (checkUser($_SESSION['type']) >= 4)) { ?>
            <button class="btn-lg btn-success btn-fill" 
                    onclick="location.replace('users.php')"
                    id="User_btn">
                    Users</button> 
            <?php } ?>

            <?php if(isset($_SESSION['user'])) { ?>
                <button class="btn-lg btn-success btn-fill pull-right" id="logout_btn" onclick="window.location.href = 'logout.php';"> Log out</button>
            <?php }

           
            
            else { ?>
                <button class="btn-lg btn-success btn-fill pull-right" type="submit" onclick="location.replace('signin.php')">Log in</button>
            <?php } ?> 
                  
            
            <?php if(!isset($_SESSION['user'])) { ?>
                <button class="btn-lg btn-success btn-fill pull-right"
                        type="submit"
                        onclick="location.replace('registration.php')">
                        Register</button>
            <?php }

            else { ?>
                <button class="btn-lg btn-success btn-fill pull-right"
                        type="submit"
                        onclick="location.replace('user_account.php')">
                        My account</button>
                <?php
                echo "<br>";
                echo "<label id='label_label' class='control-label pull-right' style='margin:5px;'><h5>(" . $_SESSION['type'] . ")</h5></label>"; 
                echo "<label id='user_label' class='control-label pull-right ' style='margin:5px;'><h5> user: " . $_SESSION['user'] . ", </h5> </label>";?>
            <?php } ?>
            

            <div class="row">
                <div class="col"></div>
            </div>
        </div>
    </div>

</body>
<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>
</html>
