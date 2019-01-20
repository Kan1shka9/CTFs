<?php
$includes = 1;
require_once 'auth.php';

// Define variables and initialize with empty values
$message = "";
$message_err = $general_error = "";
 
// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST"){
	
	// if cancel, go home
	if($_POST["submit"] == "Cancel"){
		header("Location: home.php");
	}
    
    // Check if message is empty
    if(empty(trim($_POST['message']))){
        $message_err = 'Please enter a message.';
    } elseif(strlen($_POST["message"]) > 1000) {
		$message_err = 'Message too long.';
    } else{
        $message = trim($_POST['message']);
    }
    
    // Save Message to file, the direct to home with message sent message
	$path = 'C:\\Users\\tyler\\secnotes_contacts\\';
	$filename = sha1($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT'] . time() . mt_rand()) . ".txt";
	file_put_contents($path . $filename, $message);
	$_SESSION['home-error'] = 'Message Sent';
	header("location: home.php");
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure Notes - Contact Us</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.css">
    <style type="text/css">
        body{ font: 14px sans-serif; }
        .wrapper{ width: 350px; padding: 20px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h2>Contact Us</h2>
        <p>Please enter your message</p>
		<div class="form-group <?php echo (!empty($general_error)) ? 'has-error' : ''; ?>">
            <span class="help-block"><?php echo $general_error; ?></span>
        </div>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="form-group <?php echo (!empty($title_err)) ? 'has-error' : ''; ?>">

            </div>
            <div class="form-group <?php echo (!empty($note_err)) ? 'has-error' : ''; ?>">
                <label><small>To:</small> tyler@secnotes.htb</label><br/>
				<label><small>Message:</small></label>
                <textarea id="note" name="message" class="form-control"><?php echo $message; ?></textarea>
                <span class="help-block"><?php echo $message_err; ?></span>
            </div>
            <div class="form-group">
                <input type="submit" name="submit" class="btn btn-primary" value="Send">
				<input type="submit" name="submit" class="btn btn-primary" value="Cancel">
            </div>
        </form>
    </div>    
</body>
</html>