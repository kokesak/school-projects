<?php
require "common.php";
require "services.php";

$serv = new Service();
$login = $_SESSION['user'];
$kurz = $_GET['kurz'];

$serv->unregisterStudent($login, $kurz);
redirect("user_courses.php");

?>
