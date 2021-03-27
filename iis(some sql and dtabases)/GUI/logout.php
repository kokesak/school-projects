<?php
    require "common.php";

    session_unset();
	session_destroy();
        
    redirect('index.php');
?>
