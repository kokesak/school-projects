<?php
    require "common.php";
	require "services.php";
	
	$serv = new Service();
	$zkr = $_GET['zkratka'];
	$kurz = $serv->getCourse($zkr);
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
            <input type='button' class='btn-dark btn-fill text-success pull-right' onclick="$('#creating_alert').hide('fade');" name='hide_alert_btn' value='X'/>
        </div>

        <h2 class="info-text"><?php echo $kurz['Nazev']; ?></h2>
        <div class="col-sm-7"> 
            <div class="form-group has-success">
                <form action="<?php echo"edit_course_db.php"; ?>" method="get">
						<input type="hidden" name="orig_zkratka" value="<?=$zkr;?>" />
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Name:</span>
                            <input type="text" class="form-control " value="<?php echo $kurz['Nazev']; ?>" id="Name_input" name="Name_input" onchange="enableSaveChanges()" />
                        </div>
                        
                        
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Abbreviation:</span>
                            <input type="text" class="form-control" value="<?php echo $kurz['zkratka']; ?>"  id="zkratka_input" name="zkratka_input" onchange="enableSaveChanges()" />
                        </div>

                        <div class="input-group">
                            <span class="input-group-addon">Cena:</span>
                            <input type="text" class="form-control" value="<?php echo $kurz['cena']; ?>" id="cena_input" name="cena_input" onchange="enableSaveChanges()" />
                        </div>
						
                        <div class="input-group">
                            <span class="input-group-addon">Description:</span>
                            <input type="text" class="form-control" value="<?php echo $kurz['popis']; ?>" id="popis_input" name="popis_input" onchange="enableSaveChanges()" />
                        </div>
                        <div class="input-group">
                            <span class="input-group-addon">Tag1</span>
                            <input type="text" class="form-control" value="<?php echo $kurz['tag1']; ?>" id="tag1_input" name="tag1_input" onchange="enableSaveChanges()" />
                        </div>
						<div class="input-group">
                            <span class="input-group-addon">Tag2</span>
                            <input type="text" class="form-control" value="<?php echo $kurz['tag2']; ?>" id="tag2_input" name="tag2_input" onchange="enableSaveChanges()" />
                        </div>
						<div class="input-group">
                            <span class="input-group-addon">Tag3</span>
                            <input type="text" class="form-control" value="<?php echo $kurz['tag3']; ?>" id="tag3_input" name="tag3_input" onchange="enableSaveChanges()" />
                        </div>
 


                        <!--     *****************     -->
                    
                    <button type='submit'
                        class='btn btn-fill btn-success btn-wd btn-sm pull-right'
                        style="margin:5px;"
                        onclick="$('#creating_alert').show('fade');"
                        name="usr_save_btn"
                        id="Save_btn">Save changes
                    </button>

                    
                       
                </form>

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

</body>
<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>
<script>
    function enableSaveChanges(){
        document.getElementById('Save_btn').removeClass('disabled');
    }
</script>

<script>
    function promote(){
        var pos = document.getElementById("Level_input"); 
        
        if ( pos.innerHTML === "student"){
            pos.innerHTML = "lecturer";
            $("#User_btn").addClass('hide');
        }
        else if (pos.innerHTML === "lecturer"){
            pos.innerHTML = "garant";
            $("#User_btn").addClass('hide');
        }
        else if (pos.innerHTML === "garant"){
            pos.innerHTML = "leader";
            $("#User_btn").addClass('hide');
        }
        else if (pos.innerHTML === "leader"){
            pos.innerHTML = "admin";
            $("#User_btn").removeClass('hide');
        }
    }
</script>

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>

</html>
