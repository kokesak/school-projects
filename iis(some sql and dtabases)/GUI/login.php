<?php
require "common.php";
require "services.php";

$serv = new Service();

$login = $_POST['login'];
$password = $_POST['password'];

if ($serv->isValidAccount($login, $password))
{
    $_SESSION['user'] = $login;
    $user = $serv->getUser($login);
    $_SESSION['type'] = $user['typ'];
	redirect('index.php');
}
else
{
    redirect('signin_wrong_password.php');
}

?>


