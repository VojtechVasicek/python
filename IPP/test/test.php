<?php
$rec = false;
$p_only = false;
$i_only = false;
$dir = getcwd();
$p_script = "./parse.php";
$i_script = "./interpret.py";
$j_xml ='/pub/courses/ipp/jexamxml/jexamxml.jar';
$j_cfg = '/pub/courses/ipp/jexamxml/options';
$passed = 0;
$failed = 0;


// Spouští testy pro parse.php
// Funkce očekává parametry $filename, $p_script, $j_xml a $j_cfg
// $filename reprezentuje jméno a adresu testu
// $p_script reprezentuje adresu skriptu parse.php
// $j_xml reprezentuje adresářovou cestu nástroje A7Soft JExamXML
// $j_cfg reprezentuje adresářovou cestu cofiguračního souboru nástroje A7Soft JExamXML
// Funkce vrací 0 při úspěšném testu
// Funkce vrací 1 při neúspěšném testu
function run_p_tests($filename, $p_script, $j_xml, $j_cfg){
    // Smazání předchozího outputu
    $c = "rm output";
    exec($c);
    // Získání parametrů pro spouštění podle toho jestli jejich adresářová adresa začíná v současném adresáři nebo ne
    if (substr($filename, 0, 1) == '.'){
        $command = "php7.4 ". $p_script ." < " . "." . explode(".", $filename)[1] . ".src >> output";
        $file = fopen("." . explode(".", $filename)[1] . ".rc", "r");
        $command2 = "java -jar " . $j_xml . " output " . "." . explode(".", $filename)[1] . ".out delta.xml " . $j_cfg;
    }
    else{
        $command = "php7.4 ". $p_script ." < " . explode(".", $filename)[0] . ".src >> output";
        $file = fopen(explode(".", $filename)[0] . ".rc", "r");
        $command2 = "java -jar " . $j_xml . " output " . explode(".", $filename)[0] . ".out delta.xml " . $j_cfg;
    }
    // Spuštění skriptu parse.php a následně porovnání jeho výstupu pomocí A7Soft JExamXML
    exec($command, $output, $ret);
    exec($command2, $output2, $ret2);
    if ($ret == fgets($file) && $ret2 == 0){
        fclose($file);
        return 0;
    }
    else {
        fclose($file);
        return 1;
    }
}


// Spouští testy pro interpret.py
// Funkce očekává parametry $filename, $i_script a $src
// $filename reprezentuje jméno a adresářovou adresu testu
// $i_script reprezentuje adresářovou adresu skriptu interpret.py
// $src reprezentuje adresářovou adresu vstupního xml interpretu
// Funkce vrací 0 při úspěšném testu
// Funkce vrací 1 při neúspěšném testu
function run_i_tests($filename, $i_script, $src){
    // Získání parametrů pro spouštění podle toho jestli jejich adresářová adresa začíná v současném adresáři nebo ne
    if (substr($filename, 0, 1) == '.'){
        $command = "python3.8 " . $i_script . " --source=" . $src . " --input=" .
            "." . explode(".", $filename)[1] . ".in";
        $file = fopen("." . explode(".", $filename)[1] . ".rc", "r");
        $file2 = fopen("." . explode(".", $filename)[1] . ".out", "r");
    }
    else{
        $command = "python3.8 " . $i_script . " --source=" . $src . " --input=" .
            explode(".", $filename)[0] . ".in";
        $file = fopen(explode(".", $filename)[0] . ".rc", "r");
        $file2 = fopen(explode(".", $filename)[0] . ".out", "r");
    }
    $output = [NAN];
    // Spuštění interpretu
    exec($command, $output, $ret);
    // Porovnávání dodaného a očekávaného výstupu
    if ($ret == fgets($file)){
        fclose($file);
        $t = 'a';
        $tmp = '';
        while($t){
            $t = fgets($file2);
            $tmp = $tmp.$t;
        }
        if ($tmp == '' and $output = [NAN]){
            fclose($file2);
            return 0;
        }
        elseif (count($output) > 1){
            $out = '';
            for ($i = 1; $i < count($output); $i++){
                $out = $out . $output[$i];
            }
            if ($out == $tmp){
                return 0;
            }
            else{
                fclose($file2);
                return 1;
            }
        }
        else {
            fclose($file2);
            return 1;
        }
    }
    else {
        fclose($file);
        fclose($file2);
        return 1;
    }

}


// Spouští testy pro buď interpret, nebo parser nebo pro oba
// Funkce očekává parametry $filename, $p_script, $i_script, $j_xml, $j_cfg, $p_only, $i_only
// $filename reprezentuje jméno a adresářovou adresu testu
// $p_script reprezentuje adresu skriptu parse.php
// $i_script reprezentuje adresářovou adresu skriptu interpret.py
// $j_xml reprezentuje adresářovou cestu nástroje A7Soft JExamXML
// $j_cfg reprezentuje adresářovou cestu cofiguračního souboru nástroje A7Soft JExamXML
// $p_only označuje zda se provádí pouze testy skriptu parse.php
// $i_only označuje zda se provádí pouze testy skriptu interpret.py
// Funkce vrací 0 při úspěšném testu
// Funkce vrací 1 při neúspěšném testu
function run_tests($filename, $p_script, $i_script, $j_xml, $j_cfg, $p_only, $i_only){
    // Dogenerování chybějících prázdných .in a .out souborů
    if (substr($filename, 0, 1) == '.') {
        if (file_exists("." . explode(".", $filename)[1] . ".in") == false) {
            $file = fopen("." . explode(".", $filename)[1] . ".in", "w");
            fclose($file);
        }
        if (file_exists("." . explode(".", $filename)[1] . ".out") == false) {
            $file = fopen("." . explode(".", $filename)[1] . ".out", "w");
            fclose($file);
        }
    }
    else{
        if (file_exists(explode(".", $filename)[0] . ".in") == false) {
            $file = fopen(explode(".", $filename)[0] . ".in", "w");
            fclose($file);
        }
        if (file_exists( explode(".", $filename)[0] . ".out") == false) {
            $file = fopen(explode(".", $filename)[0] . ".out", "w");
            fclose($file);
        }
    }
    // Volání parse only testů
    if ($p_only){
        $ret = run_p_tests($filename, $p_script, $j_xml, $j_cfg);
        return $ret;
    }
    // Volání interpret only testů
    elseif ($i_only){
        if (substr($filename, 0, 1) == '.') {
            $ret = run_i_tests($filename, $i_script, "." . explode(".", $filename)[1] . ".src");
        }
        else{
            $ret = run_i_tests($filename, $i_script, explode(".", $filename)[0] . ".src");
        }
        return $ret;
    }
    // Volání obou testů
    else{
        $ret = run_p_tests($filename, $p_script, $j_xml, $j_cfg);
        if ($ret == 0) {
            $ret = run_i_tests($filename, $i_script, "output");
        }
        if ($ret == 0){
            return 0;
        }
        else {
            return 1;
        }
    }
}


// Zpracování argumentů skriptu test.php
foreach ($argv as $arg){
    if ($arg == '--help'){
        echo "Tento skript slouží k testování skriptů parse.php a interpret.py.\n";
        echo "Pro spouštěcí parametry konzultujte se zadáním projektu.\n";
    }
    elseif ($arg == '--recursive'){
        $rec = true;
    }
    elseif ($arg == '--parse-only'){
        $p_only = true;
        if ($p_only == true && $i_only == true){
            exit(10);
        }
    }
    elseif ($arg == '--int-only'){
        $i_only = true;
        if ($p_only == true && $i_only == true){
            exit(10);
        }
    }
    else {
        $arg = explode("=", $arg);
        if ($arg[0] == '--directory'){
            $dir = $arg[1];
        }
        elseif ($arg[0] == '--parse-script'){
            $p_script = $arg[1];
        }
        elseif ($arg[0] == '--int-script'){
            $i_script = $arg[1];
        }
        elseif ($arg[0] == '--jexamxml'){
            $j_xml = $arg[1];
        }
        elseif ($arg[0] == '--jexamcfg'){
            $j_cfg = $arg[1];
        }
        elseif ($arg[0] != 'test.php') {
            exit(10);
        }
    }
}

$fail = [];
// Rekurzivní procházení souborů v zadaném adresáři a volání testovací funkce
if ($rec) {
    $di = new RecursiveDirectoryIterator($dir);
    foreach (new RecursiveIteratorIterator($di) as $filename) {
        $tmp = explode('/', $filename);
        $file = end($tmp);
        if (count(explode(".", $file)) == 2) {
            if ((substr($filename, 0, 1) == '.' and explode(".", $filename)[2] == 'rc') or
                (substr($filename, 0, 1) != '.' and explode(".", $filename)[1] == 'rc')) {
                $r = run_tests($filename, $p_script, $i_script, $j_xml, $j_cfg, $p_only, $i_only);
                // Počítání udělaných testů nebo jejich selhání. U selhaných testů se také ukládá jeho jméno a lokace v adresáři
                if ($r == 0) {
                    $passed += 1;
                } else {
                    if (substr($filename, 0, 1) == '.') {
                        array_push($fail, "." . explode(".", $filename)[1]);
                    }
                    else {
                        array_push($fail, explode(".", $filename)[0]);
                    }
                    $failed += 1;
                }
            }
        }
    }
}
// Nerekurzivní procházení souborů v daném adresáři a spouštění testové funkce
else {
    foreach (new DirectoryIterator($dir) as $filename){
        $file = $filename;
        $filename = $dir . "/" . $filename;;
        if (count(explode(".", $file)) == 2) {
            if (explode(".", $file)[1] == 'rc') {
                $r = run_tests($filename, $p_script, $i_script, $j_xml, $j_cfg, $p_only, $i_only);
                // Počítání udělaných testů nebo jejich selhání. U selhaných testů se také ukládá jeho jméno a lokace v adresáři
                if ($r == 0) {
                    $passed += 1;
                } else {
                    if (substr($filename, 0, 1) == '.') {
                        array_push($fail, "." . explode(".", $filename)[1]);
                    }
                    else {
                        array_push($fail, explode(".", $filename)[0]);
                    }
                    $failed += 1;
                }
            }
        }
    }
}

// Vypisování HTML na stdout
echo "<!DOCTYPE html>\n";
echo "<html lang=\"en\">\n";
echo "<head>\n";
echo "    <meta charset=\"UTF-8\">\n";
echo "    <title>TestOutput</title>\n";
echo "</head>\n";
echo "<style>\n";
echo "    body {margin:auto; width:100%; background-color: #D8DDEF;}\n";
echo "    h1 {text-align:center; color:#4C5B5C; font-family: Arial}\n";
echo "    h2 {text-align:center; margin-top: 100px; color:#4C5B5C; font-family: Arial}\n";
echo "    h3 {text-align:center; color:#9d0208; font-family: Arial}\n";
echo "</style>\n";
echo "<body>\n";
echo "    <section id=\"Results\">\n";
echo "        <div><h1>Passed: " . $passed . "</h1></div>\n";
echo "        <div><h1>Failed: " . $failed . "</h1></div>\n";
echo "        <div><h2>Failed tests</h2></div>\n";
foreach ($fail as $f){
    echo "        <div><h3>" . $f . "</h3></div>\n";
}
echo "    </section>\n";
echo "</body>\n";
echo "</html>\n";

