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
            
    
        <?php
            $serv = new Service();
            $login = $_GET['login'];
            $data = $serv->getUser($login);
        ?>

        <div class="alert alert-success collapse" id="edit_data">   <!-- collapse hide alert ath the begining -->
            <strong> Success!</strong> Changes were saved.
            <input type='button' class='btn-dark btn-fill text-success pull-right' onclick="$('#edit_data').hide('fade');" name='hide_alert_btn' value='X'/>
        </div>

        <div class="alert alert-success collapse" id="deleting_alert">   <!-- collapse hide alert ath the begining -->
            <strong> Deleting information</strong> Are you sure you want to delete your account?
            <input type='button' class='btn-dark btn-fill text-success pull-right' onclick="" name='confirm_delete_acc' value='YES'/>
            <input type='button' class='btn-dark btn-fill text-danger pull-right' onclick="$('#deleting_alert').hide('fade');" name='decline_delete_acc' value='NO'/>
        </div>

       
        <h1 class="info-text"> Your account</h1>
        <div class="col-sm-7"> 
            <div class="form-group has-success">
            <?php
                echo "<form action=\"user_update.php\" method=\"get\">";
            ?>

                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Name:</span>
                            <?php echo "<input type=\"text\" class=\"form-control\" value=\"" . $data['jmeno']  . "\" id=\"Name_input\" name=\"Name_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>
                        
                        <input type="hidden" name="login" value="<?=$login;?>" />

                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Surname:</span>
                            <?php echo "<input type=\"text\" class=\"form-control\" value=\"" . $data['prijmeni'] . "\"  id=\"Surname_input\" name=\"Surname_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>


                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Date of birth:</span>
                            <?php echo "<input type=\"date\" class=\"form-control\" value=\"" . $data['datum_narozeni'] . "\" name=\"Date_input\" onchange=\"enableSaveChanges()\" />" ?>
                        </div>

                        <!--     *****************     -->
                        <div class="input-group">
                            <span class="input-group-addon">Level:</span> <!--  $_SESSION['type']  -->
                            <select class="form-control" name="Level">
                                <?php
                                    $select_type = checkUser($data['typ']);
                                ?>
                                <option value="Student" <?php if($select_type == 0){echo("selected");}?>>Student</option>
                                <option value="Lecturer" <?php if($select_type == 1){echo("selected");}?>>Lecturer</option>
                                <option value="Garant" <?php if($select_type == 2){echo("selected");}?>>Garant</option>
                                <option value="Leader" <?php if($select_type == 3){echo("selected");}?>>Leader</option>
                                <option value="Admin" <?php if($select_type == 4){echo("selected");}?>>Admin</option>
                            </select>
                        </div>

                    
                    <button type='submit'
                        class='btn btn-fill btn-success btn-wd btn-sm pull-right'
                        style="margin:5px;"
                        onclick="$('#edit_data').show('fade');"
                        name="usr_save_btn"
                        id="Save_btn">Save changes
                    </button>
                </form>

                <Input type='button' 
                    class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                    style="margin:5px;" 
                    onclick="location.replace('index.php');"
                    name='login_btn' 
                    value='Back to menu'/> 
                </div>

                <br>
                <br>    
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
