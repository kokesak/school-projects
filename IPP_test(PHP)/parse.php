<?php

#funkce kontrolujici spravnost promenne u instrukce
function check_var($var){
  $var_len = strlen($var);
        if (preg_match('/^(GF|LF|TF)@([A-Z]|[a-z]|(_|-|\$|&|%|\*|\?|!))([A-Z]|[a-z]|[0-9]|(_|-|\$|&|%|\*|\?|!))*/', $var, $matches) && (strlen($matches[0]) == $var_len)){
          return "var";
        } else {
          return "false";
      }

}

#funkce kontrolujici spravnost symbolu u instrukce
function check_symb($symb){
  $var_len = strlen($symb);
  if (preg_match('/^(GF|LF|TF)@([A-Z]|[a-z]|(_|-|\$|&|%|\*|\?|!))([A-Z]|[a-z]|[0-9]|(_|-|\$|&|%|\*|\?|!))*/', $symb, $matches) && (strlen($matches[0]) == $var_len)){
    return "var";
  }
  elseif(preg_match('/^int@(\+|-)?([0-9])+/', $symb, $matches) && (strlen($matches[0]) == $var_len)){
    return "int";
  }
  elseif(preg_match('/^bool@(true|false)$/', $symb, $matches) && (strlen($matches[0]) == $var_len)){
    return "bool";
  }
  elseif(preg_match('/^string@((\\\\\d\d\d)|([^#| \s|\\\\]))*$/', $symb, $matches) && (strlen($matches[0]) == $var_len)){
    return "string";
  }
  elseif(preg_match('/^nil@nil$/', $symb, $matches) && (strlen($matches[0]) == $var_len)){
    return "nil";
  }
  else{
    return "false";
  }
}

#argumenty skriptu
$options = getopt("h", array("help", "stats:", "comments", "loc", "labels", "jumps"));
if(array_key_exists("help" , $options) || array_key_exists("h" , $options)){
	if($argc != 2){
    fwrite(STDERR, "too many arguments for --help\n");
    exit(10);
  }
  echo "PHP script used for Syntax and Lexical analysis of input in IPPcode19\n";
  echo "-h | --help display help for script\n";
  echo "--stats=file - file, where statistics will be stored\n";
  echo "--loc - number of instructions\n";
  echo "--comments - number of commnets in code\n";
  echo "--labels - number of unique labels\n";
  echo "--jumps - number of jumps\n";
  echo "Return value 0 - Analysis OK, output will be shown in XML format on stdout\n";
  echo "Return value 21 - missing header\n";
  echo "Return value 22 - wrong instruction\n";
  echo "Return value 23 - other syntax or lexical errors\n";
  echo "Return value 10 - missing or wrong arguments\n";
  echo "Return value 11 - cant open the file for statistics\n";
	exit(0);
}
elseif(array_key_exists("stats" , $options) == false && $argc != 1){
  fwrite(STDERR, "no stats file set\n");
  exit(10);
}

#promenne pro statistiky
$jumps = 0;
$comentLines = 0;
$labels = array();
$file = fopen('php://stdin', "r");

if($file == false){
  fwrite(STDERR, "problem with opening the file\n");
    exit(11);
}

#kontrola prvniho radku - .ippcode19
do{
  if(feof($file)){
    fwrite(STDERR, "missing header\n");
    exit(21);
  }
  $line = fgets($file);
  
  $comments = $line;
  $line = preg_replace('/#.*/','',$line);
  if($line != $comments){
    $comentLines++;
  }
  $line = trim($line);
  if(strtolower($line) == ".ippcode19"){
    break;
  }
  if($line != ''){
    fwrite(STDERR, "missing header\n");
    exit(21);
  }
}
while(true);

#vytvoreni noveho objektu pro generovani XML
$xml = new XMLWriter();
$xml->openMemory();
$xml->setIndent(1);
$xml->startDocument('1.0', 'UTF-8');
$xml->startElement('program');
$xml->writeAttribute('language', 'IPPcode19');
$instruction_number = 1;
$argument_number = 1;

while(!feof($file)) {
    $line = fgets($file);
    $comments = $line;
    #odstraneni komentare
    $line = preg_replace('/#.*/','',$line);
    if($line != $comments){
        $comentLines++;
    }
    #odstraneni prebytecnych mezer ze zacatku a konce
    $line = trim($line);

    #kdyz bude komentar na samostatnem radku
    if($line == ''){
      continue;
    }

    $line = preg_replace('/\s{2,}/',' ',$line); # nahrazeni prebytecnych mezer z prostredka retezce

    $line_array = explode(' ',$line); # rozdeleni radku po slovech do pole

    $index = array_search('',$line_array); #smazani prazdnych poli
    if($index !== FALSE){
        unset($line_array[$index]);
    }

    #prvni prvek je instrukce
    $line_array[0] = strtoupper($line_array[0]);

    switch($line_array[0]){
      # bez argumentu instrukce
      case "CREATEFRAME":
      case "POPFRAME":
      case "PUSHFRAME":
      case "RETURN":
      case "BREAK":
        if(count($line_array) == 1){
          $xml->startElement('instruction'); # zapis instrukce
          $xml->writeAttribute('order', $instruction_number++); # zapis atributu order
          $xml->writeAttribute('opcode', $line_array[0]); 
          $xml->endElement();
        }
        else{
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        break;
      
      # jeden argument <var>
      case "DEFVAR":
      case "POPS":
        if(count($line_array) == 2 && check_var($line_array[1]) == "var"){
          $argument_number = 1;
          $xml->startElement('instruction'); 
          $xml->writeAttribute('order', $instruction_number++); 
          $xml->writeAttribute('opcode', $line_array[0]);

          $xml->startElement('arg'.$argument_number); 
          $xml->writeAttribute('type', "var");
          $xml->text($line_array[1]);
          $xml->endElement();

          #ukonceni instrukce
          $xml->endElement();
        }
        else{
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        break;

      # jeden argument <symb>
      case "DPRINT":
      case "EXIT":
      case "WRITE":
      case "PUSHS":
        if(count($line_array) != 2){
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        $result_symb = check_symb($line_array[1]);
        if ($result_symb != "false"){
          $argument_number = 1;
          $xml->startElement('instruction'); 
          $xml->writeAttribute('order', $instruction_number++); 
          $xml->writeAttribute('opcode', $line_array[0]);

          $xml->startElement('arg'.$argument_number);
          #kdyz neni promena tak se musi odstrait cast za zavinacem
          if($result_symb != "var"){
            $tmp = explode('@', $line_array[1], 2);
            $xml->writeAttribute('type', $tmp[0]);
            if($result_symb == "bool"){
              $tmp[1] = strtolower($tmp[1]);
            }
            $xml->text($tmp[1]);
            $xml->endElement();

            #ukonceni instrukce
            $xml->endElement();
          }
          else{
            $xml->writeAttribute('type', $result_symb);
            $xml->text($line_array[1]);
            $xml->endElement();

            #ukonceni instrukce
            $xml->endElement();
          }
        }
        elseif($result_symb == "false"){
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        break;

      # jeden argument <label>
      case "CALL":
      case "LABEL":
      case "JUMP":
        if(count($line_array) != 2){
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        $var_len = strlen($line_array[1]);
        if (preg_match('/^([A-Z]|[a-z]|(_|-|\$|&|%|\*|\?|!))([A-Z]|[a-z]|[0-9]|(_|-|\$|&|%|\*|\?|!))*/', $line_array[1], $matches) && (strlen($matches[0]) == $var_len)){
          $argument_number = 1;
          $xml->startElement('instruction'); 
          $xml->writeAttribute('order', $instruction_number++); 
          $xml->writeAttribute('opcode', $line_array[0]);

          $xml->startElement('arg'.$argument_number); 
            $xml->writeAttribute('type', 'label');
            $xml->text($line_array[1]);
            $xml->endElement();

            #ukonceni instrukce
            $xml->endElement();
        } else {
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
      }
        if($line_array[0] == "LABEL"){
          $labels[] = $line_array[1];
        }
        else{
          $jumps++;
        }
        break;

      # dva argumenty <var> <symb>
      case "MOVE":
      case "INT2CHAR":
      case "TYPE":
      case "STRLEN":
      case "NOT":
        if(count($line_array) != 3){
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        $result_var = check_var($line_array[1]);
        $result_symb = check_symb($line_array[2]);
        if($result_var != "false" && $result_symb != "false"){
          $argument_number = 1;
          $xml->startElement('instruction'); 
          $xml->writeAttribute('order', $instruction_number++); 
          $xml->writeAttribute('opcode', $line_array[0]);

          $xml->startElement('arg'.$argument_number++); 
          $xml->writeAttribute('type', "var");
          $xml->text($line_array[1]);
          $xml->endElement();
          
          if($result_symb != "var"){
            $tmp = explode('@', $line_array[2], 2);
            $xml->startElement('arg'.$argument_number++); 
            $xml->writeAttribute('type', $tmp[0]);
            if($result_symb == "bool"){
              $tmp[1] = strtolower($tmp[1]);
            }
            $xml->text($tmp[1]);
            $xml->endElement();
            
            #ukonceni instrukce
            $xml->endElement();
          }
          else{
            $xml->writeAttribute('type', $result_symb);
            $xml->text($line_array[2]);
            $xml->endElement();
            
            #ukonceni instrukce
            $xml->endElement();
          }
        }
        else{
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        break;

      # dva argumenty <var> <type>
      case "READ":
      if(count($line_array) != 3){
        fwrite(STDERR, "other syntax or lexical errors\n");
        exit(23);
      }
      
      $result_var = check_var($line_array[1]);
      if (preg_match('/^(int|string|bool)$/', $line_array[2]) && $result_var != "false"){
        $argument_number = 1;
        $xml->startElement('instruction'); 
        $xml->writeAttribute('order', $instruction_number++); 
        $xml->writeAttribute('opcode', $line_array[0]);

        $xml->startElement('arg'.$argument_number++); 
        $xml->writeAttribute('type', "var");
        $xml->text($line_array[1]);
        $xml->endElement();
        
        $xml->startElement('arg'.$argument_number++); 
        $xml->writeAttribute('type', "type");
        $xml->text($line_array[2]);
        $xml->endElement();
          
          #ukonceni instrukce
          $xml->endElement();
        }
      else{
        fwrite(STDERR, "other syntax or lexical errors\n");
        exit(23);
      }
      break;

      # tri argumenty <var> <symb1> <symb2>
      case "ADD":
      case "SUB":
      case "MUL":
      case "IDIV":
      case "LT":
      case "GT":
      case "EQ":
      case "AND":
      case "OR":
      case "STRI2INT":
      case "CONCAT":
      case "GETCHAR":
      case "SETCHAR":
        if(count($line_array) != 4){
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        $result_var = check_var($line_array[1]);
        $result_symb = check_symb($line_array[2]);
        $result_symb_2 = check_symb($line_array[3]);
        if($result_var != "false" && $result_symb != "false" && $result_symb_2 != "false"){
          $argument_number = 1;
          $xml->startElement('instruction'); 
          $xml->writeAttribute('order', $instruction_number++); 
          $xml->writeAttribute('opcode', $line_array[0]);

          $xml->startElement('arg'.$argument_number++); 
          $xml->writeAttribute('type', "var");
          $xml->text($line_array[1]);
          $xml->endElement();

          $xml->startElement('arg'.$argument_number++); 
          if($result_symb != "var"){
            $tmp = explode('@', $line_array[2], 2);
            $xml->writeAttribute('type', $tmp[0]);
            if($result_symb == "bool"){
              $tmp[1] = strtolower($tmp[1]);
            }
            $xml->text($tmp[1]);
            $xml->endElement();
          }
          else{
            $xml->writeAttribute('type', $result_symb);
            $xml->text($line_array[2]);
            $xml->endElement();
          }

          $xml->startElement('arg'.$argument_number++);
          if($result_symb_2 != "var"){
            $tmp = explode('@', $line_array[3], 2);
            $xml->writeAttribute('type', $tmp[0]);
            if($result_symb == "bool"){
              $tmp[1] = strtolower($tmp[1]);
            }
            $xml->text($tmp[1]);
            $xml->endElement();

            #ukonceni instrukce
            $xml->endElement();
          }
          else{
            $xml->writeAttribute('type', $result_symb_2);
            $xml->text($line_array[2]);
            $xml->endElement();

            #ukonceni instrukce
            $xml->endElement();
          }
        }
        else{
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        break;

      # tri argumenty <label> <symb1> <symb2>
      case "JUMPIFEQ":
      case "JUMPIFNEQ":
        if(count($line_array) != 4){
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        $jumps++;
        $var_len = strlen($line_array[1]);
        if(preg_match('/^([A-Z]|[a-z]|(_|-|\$|&|%|\*|\?|!))([A-Z]|[a-z]|[0-9]|(_|-|\$|&|%|\*|\?|!))*/', $line_array[1], $matches) && (strlen($matches[0]) == $var_len)){
          $result_symb = check_symb($line_array[2]);
          $result_symb_2 = check_symb($line_array[3]);
            if($result_symb != "false" && $result_symb_2 != "false"){
              $argument_number = 1;
              $xml->startElement('instruction'); 
              $xml->writeAttribute('order', $instruction_number++); 
              $xml->writeAttribute('opcode', $line_array[0]);

              $xml->startElement('arg'.$argument_number++); 
              $xml->writeAttribute('type', "label");
              $xml->text($line_array[1]);
              $xml->endElement();

              $xml->startElement('arg'.$argument_number++); 
              if($result_symb != "var"){
                $tmp = explode('@', $line_array[2], 2);
                $xml->writeAttribute('type', $tmp[0]);
                if($result_symb == "bool"){
                  $tmp[1] = strtolower($tmp[1]);
                }
                $xml->text($tmp[1]);
                $xml->endElement();
              }
              else{
                $xml->writeAttribute('type', $result_symb);
                $xml->text($line_array[2]);
                $xml->endElement();
              }

              $xml->startElement('arg'.$argument_number++); 
              if($result_symb_2 != "var"){
                $tmp = explode('@', $line_array[3], 2);
                $xml->writeAttribute('type', $tmp[0]);
                if($result_symb == "bool"){
                  $tmp[1] = strtolower($tmp[1]);
                }
                $xml->text($tmp[1]);
                $xml->endElement();

                #ukonceni instrukce
                $xml->endElement();
              }
              else{
                $xml->writeAttribute('type', $result_symb_2);
                $xml->text($line_array[2]);
                $xml->endElement();

                #ukonceni instrukce
                $xml->endElement();
              }
            }
            else{
              fwrite(STDERR, "other syntax or lexical errors\n");
              exit(23);
            }
          }
        else{
          fwrite(STDERR, "other syntax or lexical errors\n");
          exit(23);
        }
        break;

      default:
        fwrite(STDERR, "wrong instruction\n");
        exit(22);
        break;

    }
      
  }
#ukonceni instrukce program
$xml->endElement();
$xml->endDocument();
#dojde k vypisu bufferu na stdout a k jeho vzprazdneni
echo $xml->flush(true);

#vypis statistik podle, jestli byly zadany
if(array_key_exists("stats" , $options)){
  $stats_file = fopen($options["stats"], "w");
  if($stats_file == false){
    fwrite(STDERR, "problem with opening the file\n");
    exit(11);
  }
  #pro pripad ze bude program bez instrukci
  if($instruction_number == 1){
    $instruction_number = 0;
  }
  var_dump($options);
  exit(0);
  foreach ($options as $key => $value) {
    switch($key){
      case "comments":
        fwrite($stats_file, "$comentLines\n");
        break;
      case "loc":
        fwrite($stats_file, "$instruction_number\n");
        break;
      case "jumps":
        fwrite($stats_file, "$jumps\n");
        break;
      case "labels":
        fwrite($stats_file, count(array_unique($labels))."\n");
        break;
      default:
        break;
    }
  }
  fclose($stats_file);
}
fclose($file);
exit(0);
?>