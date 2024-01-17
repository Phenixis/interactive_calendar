<?php
  $datas=[];
  
  if (file_exists("datas.json")) {
    $fic=file("datas.json");
    $json="";
    foreach($fic as $line) {
      $json.=$line;
    }
    $datas=json_decode($json, true);
  } else {
    for($mois=0;$mois<12;$mois++) {
      for($jour=1;$jour<date('t', mktime(0, 0, 0, $mois+1, 1, date("Y")))+1;$jour++) {
        $datas[$mois."/".$jour] = [];
      }
    }
    $fic = fopen("datas.json", "w");
    fwrite($fic, json_encode($datas, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));
  }

?>

<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Calendar <?php echo date("Y")?></title>
  <link rel="stylesheet" href="css/normalize.min.css">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="wrapper">
  <div class="periodic-table">
    
  <?php
    for($mois=0;$mois<12;$mois++) {
      for($jour=1;$jour<date('t', mktime(0, 0, 0, $mois+1, 1, date("Y")))+1;$jour++) {
        print_r($datas[$mois."/".$jour]);
      }
    }
  ?>
    
  </div>
  <script src="js/script.js"></script>
</div>

</body>
</html>
