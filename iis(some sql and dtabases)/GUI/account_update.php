<?php
require "common.php";
require "services.php";

$serv = new Service();

$personType = $_GET['Level'];
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
    'login' => $_SESSION['user'],
    'jmeno' => $_GET['Name_input'],
	'prijmeni' => $_GET['Surname_input'],
    'datum_narozeni' => $_GET['Date_input'],
	'typ' => $personType
);

$serv->updateAccount($editedPerson);
$_SESSION['type'] = $personType;

redirect('user_account.php');
?>
