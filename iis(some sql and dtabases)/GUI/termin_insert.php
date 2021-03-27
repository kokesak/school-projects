<?php
require "common.php";
require "services.php";

$serv = new Service();
$start_time = $_GET['start_input'] . ":00";
$end_time = $_GET['end_input'] . ":00";
$zkratka = $_GET['zkr_input'];

$newTerm = array(
    'nazev' => $_GET['Name_input'],
    'typ' => $_GET['termin_typ'],
	'popis' => $_GET['Popis_input'],
    'datum' => $_GET['Date_input'],
	'zacatek' => $start_time,
	'konec' => $end_time,
	'mistnost' => $_GET['mistnost_input'],
	'lektor' => $_GET['lector_input'],
	'kurz' => $zkratka
);

if ($serv->addTerm($newTerm))
	redirect("detailed_course.php?zkratka=$zkratka");
else
{
	$err = $serv->getErrorMessage();
	echo $err;
}
?>