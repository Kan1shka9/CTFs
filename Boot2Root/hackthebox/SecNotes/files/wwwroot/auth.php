<?php

if ($includes != 1) {
	die("ERROR: Should not access directly.");
}

// Initialize the session
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
 
// If session variable is not set it will redirect to login page
if(!isset($_SESSION['username']) || empty($_SESSION['username'])){
  header("location: login.php");
  exit;
}

$username = $_SESSION['username'];
?>