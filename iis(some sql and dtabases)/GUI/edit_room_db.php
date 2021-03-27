<?php
require "common.php";
require "services.php";
$serv = new Service();

$updateRoom = array(
    'orig_nazev' => $_GET['Hidden_input'],
    'nazev' => $_GET['Name_input'],
	'typ' => $_GET['Type_input'],
    'kapacita' => $_GET['Capacity_input']
);


$serv->updateRoom($updateRoom);
redirect('rooms.php');

?>
