<?php
$includes = 1;
require_once 'auth.php';

// Define variables and initialize with empty values
$title = $note = "";
$title_err = $note_err = $general_error = "";
 
// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST"){
	
	// if cancel, go home
	if($_POST["submit"] == "Cancel"){
		header("Location: home.php");
	}
 
    // Check if title is empty
    if(empty(trim($_POST["title"]))){
        $title_err = 'Please enter a title.';
    } elseif(strlen($_POST["title"]) > 100) {
		$title_err = 'Title too long.';
	} else{
        $title = trim($_POST["title"]);
    }
    
    // Check if note is empty
    if(empty(trim($_POST['note']))){
        $note_err = 'Please enter a note.';
    } elseif(strlen($_POST["note"]) > 2000) {
		$note_err = 'Note too long.';
    } else{
        $note = trim($_POST['note']);
    }
    
    // Submit post
    if(empty($title_err) && empty($note_err)){
		require_once 'db.php';
		
		// check that the user doesn't have 3 posts
		$sql = "SELECT note FROM posts WHERE username = ?";
		if($stmt = mysqli_prepare($link, $sql)) {
			mysqli_stmt_bind_param($stmt, "s", $param_username);
			$param_username = $username;
			if(mysqli_stmt_execute($stmt)){
				mysqli_stmt_store_result($stmt);
				if(mysqli_stmt_num_rows($stmt) < 3){
					mysqli_stmt_close($stmt);
					
					// add note
					$sql = "INSERT INTO posts (username, title, note) VALUES (?, ?, ?)";
					if($stmt = mysqli_prepare($link, $sql)) {
						mysqli_stmt_bind_param($stmt, "sss", $param_username, $param_title, $param_post);
						$param_title = $_REQUEST['title'];
						$param_post = $_REQUEST['note'];
						if(mysqli_stmt_execute($stmt)){
							$_SESSION['home-error'] = "Note Created";
						    header("location: home.php");
						} else {
							mysqli_stmt_close($stmt);
							$general_error = $link->error;
						}
						mysqli_stmt_close($stmt);
						
					} else {
						$general_error = $link->error;
					}
				} else {
					mysqli_stmt_close($stmt);
					$general_error = 'User already has 3 notes. Go <a href="/home.php">home</a> and delete one.';
				}
			} else {
			$general_error = $link->error;
			}
		}

		mysqli_close($link);
	}
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure Notes - Create Note</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.css">
    <style type="text/css">
        body{ font: 14px sans-serif; }
        .wrapper{ width: 350px; padding: 20px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h2>Create New Note</h2>
        <p>Please enter a Title and a Note</p>
		<div class="form-group <?php echo (!empty($general_error)) ? 'has-error' : ''; ?>">
            <span class="help-block"><?php echo $general_error; ?></span>
        </div>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="form-group <?php echo (!empty($title_err)) ? 'has-error' : ''; ?>">
                <label>Title</label>
                <input type="text" name="title" class="form-control" value="<?php echo $title; ?>">
                <span class="help-block"><?php echo $title_err; ?></span>
            </div>
            <div class="form-group <?php echo (!empty($note_err)) ? 'has-error' : ''; ?>">
                <label>Note</label>
                <textarea id="note" name="note" class="form-control"><?php echo $note; ?></textarea>
                <span class="help-block"><?php echo $note_err; ?></span>
            </div>
            <div class="form-group">
                <input type="submit" name="submit" class="btn btn-primary" value="Save">
				<input type="submit" name="submit" class="btn btn-primary" value="Cancel">
            </div>
        </form>
    </div>    
</body>
</html>