<?php
require "common.php";
require "services.php";

$serv = new Service();
$data = $serv->getUser($_SESSION['user']);
$term_id = $_GET['id'];
$zkr=$_GET['zkr'];  

foreach($_POST as $login => $points){
    $hodnoceni = $serv->getAssessment($login, $zkr);
    $update = array(
        'hodnoceni' => $points + $hodnoceni['hodnoceni'],
        'login' => $login,
        'kurz' => $zkr,
    );
    $serv->updateAssessment($update);
}


redirect("detailed_course.php?zkratka=$zkr");
?>
