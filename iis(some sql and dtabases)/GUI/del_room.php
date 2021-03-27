<?php
require "common.php";
require "services.php";


$serv = new Service();
$name = $_GET['nazev'];

$room = $serv->getRoom($name);
if ($room)
{
	$serv->deleteRoom($name);
	redirect('rooms.php');
}

?>
