<?php
require "common.php";
require "services.php";

$serv = new Service();
$login = $_SESSION['user'];
$kurz = $_GET['zkratka'];

$serv->registerStudent($login, $kurz);

redirect("courses.php");
?>