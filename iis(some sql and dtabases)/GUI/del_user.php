<?php
require "common.php";
require "services.php";


$serv = new Service();
$login = $_GET['login'];

$user = $serv->getUser($login);
if ($user)
{
	if ($login == $_SESSION['user']){
		unset($_SESSION['user']);
		$serv->deleteUser($login);
		redirect('index.php');
	} else {
		$serv->deleteUser($login);
		redirect('users.php');
	}
}


?>
