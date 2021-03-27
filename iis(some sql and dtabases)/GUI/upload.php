<?php
require "common.php";
require "services.php";

$serv = new Service();
$data = $serv->getUser($_SESSION['user']);
$term_id = $_GET['id'];
$zkr=$_GET['zkr'];  
$term = $serv->getTerm($term_id);

$target_dir = "uploads/".$term_id."/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

if(!file_exists($target_dir))
    mkdir($target_dir, 0777);

    // Check if file already exists
if (file_exists($target_file)) {
    echo "Sorry, file already exists.";
    $uploadOk = 0;
}
// Check file size

$uploadOk = 1;
if ($_FILES["fileToUpload"]["size"] > 500000) {
    echo "Sorry, your file is too large.";
    $uploadOk = 0;
}

if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        chmod($target_file, 0644);
        chmod($target_dir, 0777);
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
redirect("files_in_term.php?id=$term_id&zkr=$zkr");
?>
