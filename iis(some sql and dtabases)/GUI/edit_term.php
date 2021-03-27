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
            $term_id = $_GET['id'];
            $zkr = $_GET['zkr'];
            $term = $serv->getTerm($term_id);
        ?>
        <h1 class="info-text"> Termin <?php echo $term['nazev'] . ", number " . $term_id;  ?></h1>
        <div class="col-sm-7"> 
            <div class="form-group has-success">
                <form action="term_update.php" method="get">
						<input type="hidden" name="id_input" value="<?php echo $term_id; ?>" />
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Name:</span>
                            <!--     FILIP TODO     -->
                            <?php echo "<input type=\"text\" class=\"form-control\" value=\"" . $term['nazev']  . "\" id=\"Name_input\" name=\"Name_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>
                        
                        
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Type:</span>
                            <!--     FILIP TODO     -->
								<?php echo "<input type=\"text\" class=\"form-control\" value=\"" . $term['typ']  . "\" id=\"Type_input\" name=\"Type_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>
                       
                        <div class="input-group">
                            <span class="input-group-addon">Description:</span>
                                
                            <?php echo "<input type=\"text\" class=\"form-control\" value=\"" . $term['popis']  . "\" id=\"Desc_input\" name=\"Desc_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div> 
                        
                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Date:</span>
                            <!--     FILIP TODO     -->
                            <?php echo "<input type=\"date\" class=\"form-control\" value=\"" . $term['datum'] . "\" name=\"Date_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>
						
						<div class="input-group">
                            <span class="input-group-addon">Start:</span>
                            <!--     FILIP TODO     -->
                            <?php echo "<input type=\"time\" class=\"form-control\" value=\"" . $term['zacatek'] . "\" name=\"Start_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>
						
						<div class="input-group">
                            <span class="input-group-addon">End:</span>
                            <!--     FILIP TODO     -->
                            <?php echo "<input type=\"time\" class=\"form-control\" value=\"" . $term['konec'] . "\" name=\"End_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>

                           <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">* Room:</span>
                            <select class="form-control" name="mistnost_input">
							<?php
								$rooms = $serv->getRooms();
								while ($row = $rooms->fetch())
								{
									if ($term['mistnost'] == $row['nazev']){
										echo "<option value=\"" . $row['nazev'] . "\" selected>" . $row['nazev'] . "</option>";
									} else {
										echo "<option value=\"" . $row['nazev'] . "\">" . $row['nazev'] . "</option>";
									}
								}
							?>
                            </select>
                        </div>

                        <?php if(isset($_SESSION['user']) && (checkUser($_SESSION['type']) >= 2))  {?>
						<div class="input-group">
                            <span class="input-group-addon">* Lector:</span>
                            <select class="form-control" name="lector_input">
							<?php
								$users = $serv->getUsers();
								while ($row = $users->fetch())
								{
									if (checkUser($row['typ']) >= 1) 
									{	
										if ($term['lektor'] == $row['login']){
											echo "<option value=\"" . $row['login'] . "\" selected>" . $row['login'] . "</option>";
										} else {
											echo "<option value=\"" . $row['login'] . "\">" . $row['login'] . "</option>";
										}
									}
								}
							?>
                            </select>
                        </div>
                        <?php } ?>
                    
                    <button type='submit'
                        class='btn btn-fill btn-success btn-wd btn-sm pull-right'
                        style="margin:5px;"
                        onclick="$('#creating_alert').show('fade');"
                        name="usr_save_btn"
                        value="<?php echo"$zkr" ?>"
                        id="Save_btn">Save changes
                    </button>

                    
                       
                </form>

                <input type='button' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                        style="margin:5px;" 
                        onclick="location.replace('index.php');"
                        name='login_btn' 
                        value='Back to menu'/>
                <input type='button' 
                        class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                        style="margin:5px;" 
                        onclick='location.replace("detailed_course.php?<?php echo "zkratka=$zkr" ?>");'
                        name='login_btn' 
                        value='Back to course'/> 
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

<script src="assets/js/gsdk-bootstrap-wizard.js"></script>
<script src="assets/js/jquery.validate.min.js"></script>

</html>
