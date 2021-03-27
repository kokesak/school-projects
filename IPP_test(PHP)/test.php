<?php

$directory = './';
$recursive = FALSE;
$parse_script = 'parse.php';
$int_script = 'interpret.py';
$parse_only = FALSE;
$int_only = FALSE;

$options = getopt("h", array("help", "directory::", "recursive", "parse-script::", "int-script::", "parse-only", "int-only"));
if(array_key_exists("help" , $options) || array_key_exists("h" , $options)){
	if($argc != 2){
        fwrite(STDERR, "too many arguments for --help\n");
        exit(10);
  }
    echo "HELP PROGARMU \n";
    exit(0);
}
if(array_key_exists("directory" , $options)){
    $directory = $options['directory'];
}
if(array_key_exists("recursive" , $options)){
    $recursive = TRUE;
}
if(array_key_exists("parse-script" , $options)){
    $parse_script = $options['parse-script'];
}
if(array_key_exists("int-script" , $options)){
    $int_script = $options['int-script'];
}
if((array_key_exists("parse-only" , $options)) && (array_key_exists("int-only" , $options))){
    fwrite(STDERR, "ERROR --parse-only and --int-only cant be together \n");
    exit(10);
}
if(array_key_exists("parse-only" , $options)){
    $parse_only = TRUE;
}
if(array_key_exists("int-only" , $options)){
    $parse_only = TRUE;
}
$passed_tests = 0;

function file_manager($dir){
    global $parse_script;
    global $passed_tests;
    global $recursive;

    $list_of_files = scandir($dir);

    foreach($list_of_files as $file){

        if($recursive == True && is_dir($dir.'/'.$file)){
            if($file != '.' && $file != '..'){
                file_manager($dir.'/'.$file);
            }
            else{
                continue;
            }
        }
        #tohle cely asi v is file...
        $array = explode('.', $file);
        if(!isset($array[1])){
            continue;
        }
        if($array[1] == 'src'){

            #existence .out
            if(!file_exists($array[0].'.out')){
                fopen($array[0].'.out', 'w');
            }
            #existence .rc
            if(!file_exists($array[0].'.rc')){
                $f = fopen($array[0].'.rc', 'w');
                fwrite($f, '0');
            }
            #var_dump($file);
            exec('php7.3 '.$parse_script.'<'.$file, $output, $return_var);
            #var_dump($output);
            $rc_file = fopen($array[0].'.rc', 'r');

            $navratova_hodnota = fgets($rc_file);
            if($return_var != $navratova_hodnota)
                echo "$file se neshoduje s navratovou hodnotou, dostal jsem $return_var, ocekvam $navratova_hodnota \n";
            else{
                //var_dump($output);
                $passed_tests++;
            }

            if($return_var == 0){
                $tmp_outfile = tmpfile();
                foreach($output as $line){
                    fwrite($tmp_outfile, $line."\n");
                }
                exec('java -jar /pub/courses/ipp/jexamxml/jexamxml.jar '.$array[0].'.out '.$tmp_outfile.' diffs.xml  /D /pub/courses/ipp/jexamxml/options', $output, $xml_return);
                print("$xml_return \n");
            }



        }
    }
return;
}
file_manager($directory);
echo "$passed_tests \n";

?>