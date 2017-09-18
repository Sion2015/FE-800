<?php
$name=htmlspecialchars($_GET['name']);
$name=stripslashes($name);
$age=(int)$_GET['age'];
?>
<span style='color:red'>Welcome <b>
<?php echo $name ?>
</b> to JavaScript Kit. So you're <b> 
<?php echo $age ?>
</b> years old eh?</span>

