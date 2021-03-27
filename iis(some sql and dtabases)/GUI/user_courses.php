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
                        <td colspan=10 align="center"> <h3 > Registered courses </h3></td>
                    </tr>
                </thead>
                    
                <tbody>
                    <tr>
                        <?php
                            $serv = new Service();
                            $rows = $serv->getUserCourses($_SESSION['user']);
                            echo "<td>Course</td>"; 
                            echo "<td>Assessment</td>";
                            echo "<td>Action</td>";
                            while ( $row = $rows->fetch() ){
                                if($row['schvalen'] == 1){
                                    echo "<tr>";
                                        echo "<th scope=\"row\"> <a href=detailed_course.php?zkratka=".$row['kurz'].">" . $row['kurz'] . "</a></th>";
                                        $hodnoceni = $serv->getAssessment($_SESSION['user'], $row['kurz']);
                                        $val = $hodnoceni['hodnoceni'];
                                        echo "<th scope=\"row\"> $val Points </th>";
                                        echo "<th scope=\"row\">  <input type='button' 
                                                                        class='btn btn-fill btn-danger  btn-sm'
                                                                        name='Unregister' 
                                                                        onclick=\"location.replace('unregisterCourse.php?kurz=".$row['kurz']."');\"
                                                                        value='Unregister' /> </th>";
                                    echo "</tr>";
                                }
                            }
                            
                        ?>   
                    </tr>
                </tbody>

                <tfoot>
                </tfoot>
            </table>

            <input type='button' 
                class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                style="margin:5px;" 
                onclick="location.replace('index.php');"
                name='login_btn' value='Back to menu' /> 
        </div>                
    </div>

</body>
<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>

</html>
