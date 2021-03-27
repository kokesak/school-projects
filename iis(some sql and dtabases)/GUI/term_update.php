<?php
require "common.php";
require "services.php";


$serv = new Service();
$id = $_GET['id_input'];
$zkr = $_GET['usr_save_btn'];

$updatedTerm = array(
	'id' => $id,
	'nazev' => $_GET['Name_input'],
    'typ' => $_GET['Type_input'],
    'datum' => $_GET['Date_input'],
	'popis' => $_GET['Desc_input'],
    'zacatek' => $_GET['Start_input'],
	'konec' => $_GET['End_input'],
	'lektor' => $_GET['lector_input'],
	'mistnost' => $_GET['mistnost_input']
);

$serv->updateTerm($updatedTerm);

redirect("detailed_course.php?zkratka=$zkr");
?>
