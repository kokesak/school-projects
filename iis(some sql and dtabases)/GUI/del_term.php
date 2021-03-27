<?php
require "common.php";
require "services.php";


$serv = new Service();
$zkr = $_GET['zkr'];
$id = $_GET['id'];

$term = $serv->getTerm($id);
if ($term)
{
	if($serv->deleteTerm($id))
		redirect("detailed_course.php?zkratka=$zkr");
	else
		echo "Failed to delete term";
}


?>
