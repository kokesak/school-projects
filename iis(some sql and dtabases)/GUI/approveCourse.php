<?php
require "common.php";
require "services.php";

$serv = new Service();
$kurz = $_GET['zkratka'];

$editCourse = array(
    'course' => $kurz,
    'povoleno' => 1
);

$serv->approveCourse($editCourse);
redirect("courses.php");
?>
