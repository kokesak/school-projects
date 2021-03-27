<?php
require "common.php";
require "services.php";

$serv = new Service();

$newRoom = array(
    'nazev' => $_GET['Name_input'],
    'typ' => $_GET['Type_input'],
	'kapacita' => $_GET['Capacity_input'],
);

$serv->addRoom($newRoom);

redirect('rooms.php');
?>
