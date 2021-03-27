<?php
require "common.php";
require "services.php";


$serv = new Service();
$zkratka = $_GET['zkratka'];

$course = $serv->getCourse($zkratka);
if ($course)
{
	$serv->deleteCourse($zkratka);
	redirect('courses.php');
}


?>
