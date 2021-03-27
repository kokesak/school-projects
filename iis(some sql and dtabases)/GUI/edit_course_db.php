<?php
require "common.php";
require "services.php";


$serv = new Service();
$zkr = $_GET['orig_zkratka'];
$newZkr = $_GET['zkratka_input'];

$updatedCourse = array(
	'orig_zkratka' => $zkr,
    'zkratka' => $newZkr,
    'Nazev' => $_GET['Name_input'],
	'popis' => $_GET['popis_input'],
    'tag1' => $_GET['tag1_input'],
	'tag2' => $_GET['tag2_input'],
	'tag3' => $_GET['tag3_input'],
	'cena' => $_GET['cena_input']
);

$serv->updateCourse($updatedCourse);

redirect('courses.php');
?>
