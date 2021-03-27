<?php
require "common.php";
require "services.php";

$serv = new Service();

$personType = $_GET['Level'];
$login = $_GET['login'];
switch ($personType) {
    case 'Lecturer':
        $personType = "Lektor";
        break;
    case 'Leader':
        $personType = "Vedouci";
        break;
    default:
        break;
}

$editedPerson = array(
    'login' => $login,
    'jmeno' => $_GET['Name_input'],
	'prijmeni' => $_GET['Surname_input'],
    'datum_narozeni' => $_GET['Date_input'],
	'typ' => $personType
);

$serv->updateUser($editedPerson);
if($_SESSION['user'] == $login){
    $_SESSION['type'] = $personType;
}
redirect("users.php");
?>
