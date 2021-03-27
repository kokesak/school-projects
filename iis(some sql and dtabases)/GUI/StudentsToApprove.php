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
            <table class="table table-striped table-bordered" id="courseTable" style="width:100%">
                <thead>
                <tr>
                    <th scope="col">Login</th>
                    <th scope="col">Course</th>
                    <th scope="col">Action</th>
                </tr>
                </thead>
                        
                <tbody>
                    <?php
                        $serv = new Service();
                        $students = $serv->getNotApprovedStudents();
                        
                        while ($student = $students->fetch()){  
                            echo "<tr> <td>" . $student['login'] ."</td> ";
                            echo "<td>" .$student['kurz']."</td>";
                            echo "<td>  <input type='button' 
                                class='btn btn-fill btn-success  btn-sm'
                                name='Approve' 
                                onclick=\"location.replace('approveStudent_db.php?user=".$student['login']."&course=".$student['kurz']."');\"
                                value='Approve' /> </td>
                                </tr>";
                        }
                    ?>   
                </tbody>

                <tfoot>
                </tfoot>
            </table>

            <input type='button' 
                class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                style="margin:5px;" 
                onclick="location.replace('index.php');"
                name='login_btn' value='Back to menu' />
            <?php
            if(checkUser($_SESSION['type']) >= 3){
                echo "<input type='button' 
                    class='btn btn-fill btn-success btn-wd btn-sm pull-right'
                    style=\"margin:5px;\" 
                    onclick=\"location.replace('create_room.php');\"
                    name='login_btn' value='Create room' />";
            }?> 
        </div>                
    </div>

</body>
<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>

</html>
