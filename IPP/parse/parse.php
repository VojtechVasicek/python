<?php /** @noinspection PhpUndefinedVariableInspection */

// Funkce vola funkci count_check a tiskne operacni kod a order instrukce
function xml_zero($xw, $order, $opcode){
    xmlwriter_start_element($xw, 'instruction');
    xmlwriter_start_attribute($xw, 'order');
    xmlwriter_text($xw, $order);
    xmlwriter_end_attribute($xw);
    xmlwriter_start_attribute($xw, 'opcode');
    xmlwriter_text($xw, $opcode);
    xmlwriter_end_attribute($xw);
}
// Funkce vola funkci xml_zero a tiskne 1. argument
function xml_one($xw, $order, $opcode, $type1, $arg1){
    xml_zero($xw, $order, $opcode);
    xmlwriter_start_element($xw, 'arg1');
    xmlwriter_start_attribute($xw, 'type');
    xmlwriter_text($xw, $type1);
    xmlwriter_end_attribute($xw);
    xmlwriter_write_raw($xw, $arg1);
    xmlwriter_end_element($xw);
}
// Funkce vola funkci xml_one a tiskne 2. argument
function xml_two($xw, $order, $opcode, $type1, $arg1, $type2, $arg2){
    xml_one($xw, $order, $opcode, $type1, $arg1);
    xmlwriter_start_element($xw, 'arg2');
    xmlwriter_start_attribute($xw, 'type');
    xmlwriter_text($xw, $type2);
    xmlwriter_end_attribute($xw);
    xmlwriter_write_raw ($xw, $arg2);
    xmlwriter_end_element($xw);
}
// Funkce vola funkci xml_two a tiskne 3. argument
function xml_three($xw, $order, $opcode, $type1, $arg1, $type2, $arg2, $type3, $arg3){
    xml_two($xw, $order, $opcode, $type1, $arg1, $type2, $arg2);
    xmlwriter_start_element($xw, 'arg3');
    xmlwriter_start_attribute($xw, 'type');
    xmlwriter_text($xw, $type3);
    xmlwriter_end_attribute($xw);
    xmlwriter_write_raw ($xw, $arg3);
    xmlwriter_end_element($xw);
}
// Funkce kotroluje zda je argument typu var
function var_check($input){
    if (substr_count($input, '@') != 1){
        exit(23);
    }
    $sub = explode('@', $input);
    if ($sub[0] != 'GF' && $sub[0] != 'LF' && $sub[0] != 'TF'){
        exit(23);
    }
    if (preg_match("/[^a-zA-Z0-9_$&%*!?\x2d]/", $sub[1]) == 1){
        exit(23);
    }
    if (ord(substr($sub[1], 0, 1)) > 47 && ord(substr($sub[1], 0, 1)) < 58 ){
        exit(23);
    }
}
// Funkce kotroluje zda je argument typu symb
function symb_check($input){
    $sub = explode('@', $input);
    if ($sub[0] != 'GF' && $sub[0] != 'LF' && $sub[0] != 'TF'){
        if ($sub[0] == 'nil' && $sub[1] == 'nil'){
            return $input;
        }
        else if ($sub[0] == 'int' && is_numeric($sub[1])){
            return $input;
        }
        else if ($sub[0] == 'bool' && ($sub[1] == 'true' || $sub[1] == 'false')){
            return $input;
        }
        // Ve stringu funkce nahrazuje nektere problemove znaky bud escape sekvenci nebo XML identifikatorem
        else if ($sub[0] == 'string'){
            for ($i = 0; $i < strlen($sub[1]); $i++){
                $s = ord($sub[1][$i]);
                if ($s == 92){
                    if (strlen($sub[1]) < $i + 3){
                        exit(23);
                    }
                    else if (!is_numeric($sub[1][$i+1]) || !is_numeric($sub[1][$i+2]) || !is_numeric($sub[1][$i+3])){
                        exit(23);
                    }
                } else if ($s == 60){
                    $sub[1] = substr_replace($sub[1], '&lt;', $i, 1);
                } else if ($s == 62){
                    $sub[1] = substr_replace($sub[1], '&gt;', $i, 1);
                } else if ($s == 38){
                    $sub[1] = substr_replace($sub[1], '&amp;', $i, 1);
                } else if ($s == 34){
                    $sub[1] = substr_replace($sub[1], '&quot;', $i, 1);
                } else if ($s == 39){
                    $sub[1] = substr_replace($sub[1], '&apos;', $i, 1);
                }
            }
            return $sub[0]."@".$sub[1];

        }
        else{
            exit(23);
        }
    }
    else{
        var_check($input);
        return $input;
    }
}
// Funkce kotroluje zda je argument typu label
function label_check($input){
    if (preg_match("/[^a-zA-Z0-9_$&%*!?\x2d]/", $input) == 1){
        exit(23);
    }
}
// Funkce kontroluje zda je argument typu type
function type_check($input){
    if ($input != 'int' && $input != 'bool' && $input != 'string'){
        exit(23);
    }
}
// Funkce kontroluje pocet argumentu oproti ocekavanemu poctu argumentu
function count_check($sub, $exp_count){
    if (count($sub) != $exp_count){
        exit(23);
    }
}

// Funkce parse kontroluje jednotlive prikazy a jejich argumenty pomoci funkci a nasledne vola funkci na jejich
// prevedeni do XML
function parse($xw, $input, $order){
    $input = preg_replace(" /\s+/ ", " ", $input);
    $sub = explode(" ", $input);
    // Funkce s 0 argumenty
    if (strcasecmp($sub[0], 'createframe') == 0){
        count_check($sub, 1);
        xml_zero($xw, $order, 'CREATEFRAME');
    } else if (strcasecmp($sub[0], 'pushframe') == 0){
        count_check($sub, 1);
        xml_zero($xw, $order, 'PUSHFRAME');
    } else if (strcasecmp($sub[0], 'popframe') == 0){
        count_check($sub, 1);
        xml_zero($xw, $order, 'POPFRAME');
    } else if (strcasecmp($sub[0], 'return') == 0){
        count_check($sub, 1);
        xml_zero($xw, $order, 'RETURN');
    } else if (strcasecmp($sub[0], 'break') == 0){
        count_check($sub, 1);
        xml_zero($xw, $order, 'BREAK');
    // Funkce s 1 argumentem
    }else if (strcasecmp($sub[0], 'defvar') == 0) {
        count_check($sub, 2);
        var_check($sub[1]);
        xml_one($xw, $order, 'DEFVAR', 'var', $sub[1]);
    } else if (strcasecmp($sub[0], 'call') == 0) {
        count_check($sub, 2);
        label_check($sub[1]);
        xml_one($xw, $order, 'CALL', 'label', $sub[1]);
    } else if (strcasecmp($sub[0], 'pushs') == 0) {
        count_check($sub, 2);
        $sub[1] = symb_check($sub[1]);
        xml_one($xw, $order, 'PUSHS', 'symb', $sub[1]);
    } else if (strcasecmp($sub[0], 'pops') == 0) {
        count_check($sub, 2);
        var_check($sub[1]);
        xml_one($xw, $order, 'POPS', 'var', $sub[1]);
    } else if (strcasecmp($sub[0], 'write') == 0) {
        count_check($sub, 2);
        $sub[1] = symb_check($sub[1]);
        xml_one($xw, $order, 'WRITE', 'symb', $sub[1]);
    } else if (strcasecmp($sub[0], 'label') == 0) {
        count_check($sub, 2);
        label_check($sub[1]);
        xml_one($xw, $order, 'LABEL', 'label', $sub[1]);
    } else if (strcasecmp($sub[0], 'jump') == 0) {
        count_check($sub, 2);
        label_check($sub[1]);
        xml_one($xw, $order, 'JUMP', 'label', $sub[1]);
    } else if (strcasecmp($sub[0], 'exit') == 0) {
        count_check($sub, 2);
        $sub[1] = symb_check($sub[1]);
        xml_one($xw, $order, 'EXIT', 'symb', $sub[1]);
    } else if (strcasecmp($sub[0], 'dprint') == 0) {
        count_check($sub, 2);
        $sub[1] = symb_check($sub[1]);
        xml_one($xw, $order, 'DPRINT', 'symb', $sub[1]);
    // Funkce se 2 argumenty
    } else if (strcasecmp($sub[0], 'move') == 0) {
        count_check($sub, 3);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        xml_two($xw, $order, 'MOVE', 'var', $sub[1], 'symb', $sub[2]);
    } else if (strcasecmp($sub[0], 'int2char') == 0) {
        count_check($sub, 3);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        xml_two($xw, $order, 'INT2CHAR', 'var', $sub[1], 'symb', $sub[2]);
    } else if (strcasecmp($sub[0], 'read') == 0) {
        count_check($sub, 3);
        var_check($sub[1]);
        type_check($sub[2]);
        xml_two($xw, $order, 'READ', 'var', $sub[1], 'type', $sub[2]);
    } else if (strcasecmp($sub[0], 'strlen') == 0) {
        count_check($sub, 3);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        xml_two($xw, $order, 'STRLEN', 'var', $sub[1], 'symb', $sub[2]);
    } else if (strcasecmp($sub[0], 'type') == 0) {
        count_check($sub, 3);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        xml_two($xw, $order, 'TYPE', 'var', $sub[1], 'symb', $sub[2]);
    } else if (strcasecmp($sub[0], 'not') == 0) {
        count_check($sub, 3);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        xml_two($xw, $order, 'NOT', 'var', $sub[1], 'symb', $sub[2]);
    // Funkce se 3 argumenty
    }else if (strcasecmp($sub[0], 'add') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'ADD', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'sub') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'SUB', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'mul') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'MUL', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'idiv') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'IDIV', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'lt') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'LT', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'gt') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'GT', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'eq') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'EQ', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'and') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'AND', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'or') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'OR', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'stri2int') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'STRI2INT', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'concat') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'CONCAT', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'getchar') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'GETCHAR', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'setchar') == 0) {
        count_check($sub, 4);
        var_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'SETCHAR', 'var', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'jumpifeq') == 0) {
        count_check($sub, 4);
        label_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'JUMPIFEQ', 'label', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if (strcasecmp($sub[0], 'jumpifneq') == 0) {
        count_check($sub, 4);
        label_check($sub[1]);
        $sub[2] = symb_check($sub[2]);
        $sub[3] = symb_check($sub[3]);
        xml_three($xw, $order, 'JUMPIFNEQ', 'label', $sub[1], 'symb', $sub[2], 'symb', $sub[3]);
    } else if ($sub[0] == ''){
        return;
    } else
        exit(22);
}

// Zpracovani argumentu --help
if ($argc == 2 && $argv[1] == "--help"){
    echo "Tento program preklada vstupni zdrojovy kod v IPPcode21 do XML.\n";
    exit(0);
} else if ($argc != 1){ // Kontrola prebytecnych argumentu, pokud se nevyskytuj --help
    exit(10);
}
$order = 0;
$xw = xmlwriter_open_memory();
// Cyklus ktery postupne nacita vsechny radky a nasledne na ne vola funkci parse
do {
    $input = readline();
    $in = $input;
    $input = trim(explode('#', $input)[0], ' ');
    // Kontrola hlavicky
    if ($order == 0){
        while($input == ''){
            $input = readline();
        }
        if (strcasecmp($input, '.ippcode21') != 0) {
            exit(21);
        }
        else {
            // Nastaveni hlavicky XML souboru
            xmlwriter_set_indent($xw, 1);
            $res = xmlwriter_set_indent_string($xw, ' ');
            xmlwriter_start_document($xw, '1.0','UTF-8');
            xmlwriter_start_element($xw, 'program');
            xmlwriter_start_attribute($xw, 'language');
            xmlwriter_text($xw, 'IPPcode21');
            xmlwriter_end_attribute($xw);
        }
    }
    else {
        // Pokud se nic nenacte, ukonci se cyklus
        if ($in == false) {
            break;
        }
        parse($xw, $input, $order);
        xmlwriter_end_element($xw);
    }
    $order++;
}while(true);
// Zakonceni XML a jeho vytisteni
xmlwriter_end_element($xw);
xmlwriter_end_document($xw);
echo xmlwriter_output_memory($xw);
exit(0);