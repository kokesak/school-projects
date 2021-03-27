<?php
require "common.php";
require "services.php";

$serv = new Service();
$login = $_GET['user'];
$kurz = $_GET['course'];

$approveStudent = array(
    'login'  => $login,
    'course' => $kurz,
    'schvalen' => 1
);

$serv->approveStudents($approveStudent);
redirect("StudentsToApprove.php");
?>
