<?php
    require "common.php";
	require "services.php";
	
	$serv = new Service();
	$zkr = $_GET['zkratka'];
    $kurz = $serv->getCourse($zkr);
    $student_is_enrolled = false;
    $is_garant = false;
    if(isset($_SESSION['user'])){
        $tmp = $serv->checkRegistration($_SESSION['user'],$kurz['zkratka']);
        if($tmp){
            if($tmp['schvalen'] == "1"){
                $student_is_enrolled = true;
            }
        }
        if($kurz['spravuje'] == $_SESSION['user']){
            $is_garant = true;
        }
    }
    
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
            
            <div class="row" style="margin-top:2%">

                <?php if(isset($_SESSION['user']) && (checkUser($_SESSION['type']) >= 2))  {?>
                    <input  type='button' 
                            class='btn btn-fill btn-warning btn-wd btn-sm pull-right'
                            style="margin:5px;" 
                            onclick="location.replace('<?php echo "create_termin.php?zkratka=$zkr" ?>');"
                            name='login_btn' 
                            value='ADD new termin'/>
                <?php } ?>

                        <input type='button'    
                            class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                            style="margin:5px;" 
                            onclick="location.replace('courses.php');"
                            name='btn_to_courses' 
                            value='Back to courses'/>
                        <input type='button'    
                            class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                            style="margin:5px;" 
                            onclick="location.replace('index.php');"
                            name='login_btn' 
                            value='Back to menu'/> 
            </div>
			
            <div class="container mb-4 mt-4">
                <div class="row">
                    <div class="col-md-offset-2 col-md-12" >
                        <h1 s><?php echo $kurz['Nazev']; ?></h1>
                    </div>
                    <div class="col-md-offset-3 col-md-12" style="margin-left: 2%;background-color: white">
                        <p style="font-size:160%; color:black;"><?php echo $kurz['zkratka']; ?></p>
                        <p style="font-size:160%; color:black;"> Garant:</p>
                        <div class="col-md-12">
                        <p style="color:black;"> <?php echo $kurz['spravuje']; ?></p> 
                        <br></br>
                        </div>
                        
                        <h3 >Description</h3>
                        
                        <div class="col-md-12">
                            <p style="color:black;"><?php echo $kurz['popis']; ?></p>
                        </div>
                        <br></br>

                        <h3 >Tag1</h3>
                        <div class="col-md-12">
                            <p style="color:black;"><?php echo $kurz['tag1']; ?></p>
                        </div>
                        <br></br>

                        <h3 >Terms</h3>
                        <div class="col-md-12">
                            <table class="table table-striped table-bordered table-responsive" id="terminTable" style="width:100%">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Type</th>
                                        <th>Date</th>
										<th>Start</th>
										<th>Finish</th>
										<th>Lector</th>
                                        <th>Room</th>
                                        <?php
                                        if ( (isset($_SESSION['user'])) && ((checkUser($_SESSION['type']) >= 3) || ($student_is_enrolled) || ($is_garant)) ) 
                                            {
                                                echo '<th>Action</th>';
                                            }
                                        ?>
                                    </tr>
                                </thead>
                                
                                <tbody>
									<?php
										$terms = $serv->getTerms($zkr);
										while ($row = $terms->fetch()) {
											$id = $row['id'];
											
												echo "<tr>";
												echo "<td>" . $row['nazev'] . "</td>";
												echo "<td>" . $row['typ'] . "</td>";
												echo "<td>" . $row['datum'] . "</td>";
												echo "<td>" . $row['zacatek'] . "</td>";
												echo "<td>" . $row['konec'] . "</td>";
												echo "<td>" . $row['lektor'] . "</td>";
												echo "<td>" . $row['mistnost'] . "</td>";
												if(isset($_SESSION['user'])){
													if ( (checkUser($_SESSION['type']) >= 3) || ($row['lektor'] == $_SESSION['user']) || ($is_garant) ) 
													{
                                                        echo "<td class=\"action\">";
                                                        if((checkUser($_SESSION['type']) >= 3) || ($is_garant)){
                                                            echo "<a href=\"del_term.php?id=$id&zkr=$zkr\"> Delete </a> "; echo "|";
                                                        }
                                                        echo "<a href=\"edit_term.php?id=$id&zkr=$zkr\"> Edit </a> "; echo "|";
                                                        echo "<a href=\"files_in_term.php?id=$id&zkr=$zkr\"> Files </a> "; echo "|";
                                                        echo "<a href=\"add_points.php?id=$id&zkr=$zkr\"> Assessment </a> ";
														echo "</td>\n";
                                                    }
                                                    elseif ($student_is_enrolled) // if student 
													{
														echo "<td class=\"action\">";
                                                        echo "<a href=\"files_in_term.php?id=$id&zkr=$zkr\">Files</a> ";
														echo "</td>\n";
													}
												}
												echo "</tr>\n";
										}
									?>  
                                </tbody>

                                <tfoot>
                                </tfoot>
                            </table>
                        </div>
                        <br></br>

                        <br></br>
                        <br></br>
                        <?php if(isset($_SESSION['user']) && $student_is_enrolled){?>
                            <p style="font-size:160%; color:red;"> Assessment: <?php $hodnoceni = $serv->getAssessment($_SESSION['user'], $zkr); echo $hodnoceni["hodnoceni"];?> Points</p>

                            
                        <?php  } ?>
                    </div>
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


</body>
</html>
