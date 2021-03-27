<?php
require "common.php";
require "services.php";

$serv = new Service();

$newperson = array(
    'login' => $_GET['Login_input'],
    'password' => $_GET['Password_input'],
	'jmeno' => $_GET['Name_input'],
    'prijmeni' => $_GET['Surname_input'],
	'datum_narozeni' => $_GET['Date_input']
);

$serv->addAccount($newperson);

redirect('signin.php');
?>
