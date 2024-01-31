<?php
  $datas=[];
  $PRINTEMPS = 240320;
  $ETE = 240620;
  $AUTOMNE = 240920;
  $HIVER = 241220;
  $actualSeason="Hiver";
  $weekend=" weekend";
  
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
        
        if (count($datas[$mois."/".$jour]) >= 1 && in_array($datas[$mois."/".$jour][0], ["Printemps", "Été", "Automne", "Hiver"])) {
          $actualSeason=$datas[$mois."/".$jour][0];
        }
        
        if (date("ymd") > date('ymd', mktime(0, 0, 0, $mois+1, $jour, date("Y")))) {
          // Si la date d'aujourd'hui est supérieure à la date du jour sélectionné
          $specificSeason="before";
        } else {
          $specificSeason=$actualSeason;
        }

        if (date('w', mktime(0, 0, 0, $mois+1, $jour, date("Y"))) > 5 || date('w', mktime(0, 0, 0, $mois+1, $jour, date("Y"))) == 0) {
          $weekend=" weekend";
        } else {
          $weekend="";
        }

        echo "<div class=\"element $specificSeason c". $mois+1 . " r$jour \">\n\t<input class=\"activate\" type=\"radio\" name=\"elements\"/>\n\t<input class=\"deactivate\" type=\"radio\" name=\"elements\"/>\n\t<div class=\"overlay\"></div>\n\t<div class=\"square\">\n\t\t<div class=\"flex$weekend\">\n\t\t\t<div class=\"atomic-number\">" . sprintf("%0d", $jour) . "</div>\n\t\t\t<div class=\"symbol\">" . date('D', mktime(0, 0, 0, $mois+1, $jour, date("Y"))) . "&nbsp;</div>\n\t\t</div>\n\t\t<div class=\"nb_events\">" . count($datas[$mois."/".$jour]) . " events</div>\n\t\t<div class=\"name\">";
        foreach($datas[$mois."/".$jour] as $event) {
          echo "<li><textarea class=\"event\" cols=\"18\" rows=\"" . ceil((strlen($event)+1)/15) . "\">$event</textarea></li>";
        }
        echo "<input type=\"text\" class=\"new_event\" name=\"new_event\"></div>\n\t</div>\n</div>\n\n";
      }
    }
  ?>
    
  </div>
  <script src="js/script.js"></script>
</div>

</body>
</html>
