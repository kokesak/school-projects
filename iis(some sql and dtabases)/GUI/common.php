<?php
    session_start();
	header('Content-type: text/html; charset=utf-8');

function redirect($dest)
{
    $script = $_SERVER["PHP_SELF"];
    if (strpos($dest,'/')) {
        $path = $dest;
    } else {
        $path = substr($script, 0, strrpos($script, '/')) . "/$dest";
    }
    $name = $_SERVER["SERVER_NAME"];
    header("HTTP/1.1 301 Moved Permanently");
    header("Location: http://$name$path");
}

function checkUser($type)
    {
        switch ($type) {
            case 'Student':
                return 0;
                break;
            case 'Lektor':
                return 1;
                break;
            case 'Garant':
                return 2;
                break;
            case 'Vedouci':
                return 3;
                break;
            case 'Admin':
                return 4;
                break;
            
            default:
                return -1;
                break;
        }
    }

/*function require_user()
{
    if (!isset($_SESSION['user']))
    {
        echo "<h1>Access forbidden</h1>";
        exit();
    }
} */
?>