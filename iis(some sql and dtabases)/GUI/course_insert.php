<?php
require "common.php";
require "services.php";
?>

<?php
$serv = new Service();

$newcourse = array(
    'zkratka' => $_GET['Abbreviation_input'],
    'Nazev' => $_GET['Name_input'],
	'popis' => $_GET['description'],
    'tag1' => $_GET['Tag1_input'],
	'tag2' => $_GET['Tag2_input'],
	'tag3' => $_GET['Tag3_input'],
	'cena' => $_GET['Price_input'],
	'spravuje' => $_SESSION['user']
);

$serv->addCourse($newcourse);

redirect('courses.php');
?>