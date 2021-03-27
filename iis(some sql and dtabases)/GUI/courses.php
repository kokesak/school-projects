<?php
    require "common.php";
    require "services.php";
?>
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />

    <link href="http://netdna.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.css" rel="stylesheet">
    <link href="assets/css/bootstrap.min.css" rel="stylesheet" />
    <link href="assets/css/gsdk-bootstrap-wizard.css" rel="stylesheet" />

    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css"  type="text/css">

    
</head>

<body>
    <div class="image-container set-full-height" style="background-image: url('assets/img/main_screen.jpg')">
        <div class="container">
            
            <div class="alert alert-success collapse" id="confirm_subject_alert">   <!-- collapse hide alert ath the begining -->
                <strong> Success!</strong> Changes were saved.
                <input type='button' class='btn-dark btn-fill text-success pull-right' onclick="$('#confirm_subject_alert').hide('fade');" name='hide_alert_btn' value='X'/>
            </div>

            <div class="row">
                <?php if(isset($_SESSION['user']) && (checkUser($_SESSION['type']) >= 2))  {?>
                    <input  type='button' 
                            class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                            style="margin:5px;" 
                            onclick="location.replace('create_course.php');"
                            name='login_btn' 
                            value='ADD new course'/>
                <?php } ?>
            </div>


            <div class="container mb-3 mt-3">
                <table class="table table-striped table-bordered" id="courseTable" style="width:100%">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>abbrev</th>
                            <th>Price [kc]</th>
                            <th>Garant</th>
                            <th>tag1</th>
                            <th>tag2</th>
                            <th>tag3</th>
                            <th>approved</th>
                            <?php if(isset($_SESSION['user'])){?>
                                <th>registered</th>
                                <?php if( (checkUser($_SESSION['type'])) >= 2 ){?>
                                    <th>action</th>
                                <?php }
                            } ?>
                        </tr>
                    </thead>
                    
                    <tbody>
                    <?php
                        $serv = new Service();
                        $rows = $serv->getCourses();

                        while ($row = $rows->fetch())
                        {   
                            
                            if( (($row['Povolen'] == 0) && (checkUser($_SESSION['type']) >= 2)) || ($row['Povolen'] == 1)){

                                $zkr = $row['zkratka'];
                                echo "<tr>";
                                echo "<td> <a href=\"detailed_course.php?zkratka=$zkr\">". $row['Nazev'] ."</a> </td>";
                                echo "<td>" . $row['zkratka'] . "</td>";
                                echo "<td>" . $row['cena'] . "</td>";
                                echo "<td>" . $row['spravuje'] . "</td>";
                                echo "<td>" . $row['tag1'] . "</td>";
                                echo "<td>" . $row['tag2'] . "</td>";
                                echo "<td>" . $row['tag3'] . "</td>";
                                
                                if(isset($_SESSION['user']) && (checkUser($_SESSION['type']) >= 3)){
                                    if( $row['Povolen'] == 0 ){
                                        echo "<td> <button class=\"btn-sm btn-success btn-fill\"
                                            type=\"submit\"
                                            id=\"btn_".$row['zkratka']."\"
                                            onclick=\"location.replace('approveCourse.php?zkratka=".$row['zkratka']."');\">
                                            Approve</button> </td>";
                                    }
                                    else{
                                        echo "<td>Yes</td>";
                                    }
                                    
                                }
                                else{
                                    if ($row['Povolen'] == 0) {
                                        echo "<td>No</td>";
                                    } 
                                    else {
                                        echo "<td>Yes</td>";
                                    }
                                }
                                
                                
                                if(isset($_SESSION['user'])){
                                    if(!$serv->checkRegistration($_SESSION['user'], $row['zkratka'])){
                                        echo "<td> <button class=\"btn-sm btn-success btn-fill\"
                                                        type=\"submit\"
                                                        id=\"btn_".$row['zkratka']."\"
                                                        onclick=\"location.replace('register_student.php?zkratka=".$row['zkratka']."');\">
                                                        Register</button> </td>";
                                    }
                                    else{
                                        $servx = new Service();
                                        $approved = $servx->checkIfStudentApproved($_SESSION['user'], $row['zkratka']);
                                        $x = $approved['schvalen'];
                                        
                                        if($approved['schvalen'] == 1)
                                            echo "<td> Registred </td>";
                                        else
                                            echo "<td> Pending... </td>";
                                    }
                                    if ((checkUser($_SESSION['type']) >= 2)) {
                                        echo '<td class="action">';
                                            echo "<a href=\"edit_course_web.php?zkratka=$zkr\">Edit</a> ";
                                            echo "<a href=\"del_course.php?zkratka=$zkr\">Delete</a> ";
                                        echo "</td>\n";
                                    }
                                }
                                echo "</tr>\n";
                            }
                        }
                    ?>   

                    </tbody>

                    <tfoot>
                    </tfoot>
                </table>

                <div class="row">
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


    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" type="text/javascript"></script>

    <script src="http://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>   <!-- need for searching in table-->
    <script src="http://cdn.datatables.net/1.10.19/js/dataTables.bootstrap4.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
    <script text="text/javascript">
        $(document).ready( function () {
            $('#courseTable').DataTable();
        } );
    </script>

    <script>
        function hide(divId) {
            $("#" + divId).hide();
        }
    </script>


</body>
</html>
