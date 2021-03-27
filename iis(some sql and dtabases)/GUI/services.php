<?php

class Service
{
    private $pdo;
    private $lastError;
    
    function __construct()
    {
        $this->pdo = $this->connect_db();
        $this->lastError = NULL;
    }

    function connect_db()
    {
        $dsn = "mysql:host=localhost;dbname=xhrusk26;port=/var/run/mysql/mysql.sock";
        $username = 'xhrusk26';
        $password = 'humdam2n';
        $options = array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8');
	try {
		$pdo = new PDO($dsn, $username, $password, $options);
	} catch (PDOException $e) {
		echo "Connection error: ".$e->getMessage();
		die();
	}
        return $pdo;
    }

    function getErrorMessage()
    {
        if ($this->lastError === NULL)
            return '';
        else
            return $this->lastError[2]; //the message
    }
    /****************
	USERS, ACCOUNTS
	*****************/
    function addAccount($data)
    {
        $stmt = $this->pdo->prepare('INSERT INTO Uzivatel (login, password, jmeno, prijmeni, datum_narozeni) VALUES (?, ?, ?, ?, ?)');
        $login = $data['login'];
        $pwd = password_hash($data['password'], PASSWORD_DEFAULT);
        if ($stmt->execute([$login, $pwd, $data['jmeno'], $data['prijmeni'], $data['datum_narozeni']]))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }

    function updateAccount($data)
    {
        $stmt = $this->pdo->prepare('UPDATE Uzivatel SET jmeno = :jmeno, prijmeni = :prijmeni, datum_narozeni = :datum_narozeni, typ = :typ WHERE login = :login');
        if ($stmt->execute($data))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	   function isValidAccount($login, $password)
    {
        $data = $this->getUser($login);
        return password_verify($password, $data['password']);
    }
	
	function getUsers(){
		$stmt = $this->pdo->query('SELECT login, jmeno, prijmeni, typ FROM Uzivatel LIMIT 100');
        return $stmt;
    }
    
    function approveStudents($studentData){
        $stmt = $this->pdo->prepare('UPDATE Student_Kurz SET schvalen=:schvalen WHERE login = :login AND kurz = :course');
        if ($stmt->execute($studentData))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }

	function approveCourse($approve){
        $stmt = $this->pdo->prepare("UPDATE Kurz SET Povolen = :povoleno WHERE zkratka = :course");
        if ($stmt->execute($approve)) {
			return TRUE;
		} 
		else
		{
			$this->lastError = $stmt->errorInfo();
			return FALSE;
        }
    }
	
	
    function getNotApprovedStudents(){
        $stmt = $this->pdo->query('SELECT DISTINCT login, kurz FROM Student_Kurz WHERE schvalen = 0 ');
        return $stmt;
        
	}

	function deleteUser($login)
    {
        $stmt = $this->pdo->prepare('DELETE FROM Uzivatel WHERE login = ?');
        if ($stmt->execute([$login]))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	function getUser($login)
	{
		$stmt = $this->pdo->prepare('SELECT login, password, jmeno, prijmeni, datum_narozeni, typ FROM Uzivatel WHERE login = ?');
        $stmt->execute([$login]);
        return $stmt->fetch();
	}
	
	/****************
	COURSES
	*****************/
	
	function updateCourse($data)
    {
        $stmt = $this->pdo->prepare('UPDATE Kurz SET zkratka = :zkratka, Nazev = :Nazev, popis = :popis, tag1 = :tag1, tag2 = :tag2, tag3 = :tag3, cena = :cena WHERE zkratka = :orig_zkratka');
        if ($stmt->execute($data))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	function addCourse($data)
    {
        $stmt = $this->pdo->prepare('INSERT INTO Kurz (zkratka, Nazev, popis, tag1, tag2, tag3, cena, spravuje) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        if ($stmt->execute([$data['zkratka'], $data['Nazev'], $data['popis'], $data['tag1'], $data['tag2'], $data['tag3'], $data['cena'], $data['spravuje']]))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	function getCourses(){
		$stmt = $this->pdo->query('SELECT Nazev, zkratka, tag1, tag2, tag3, cena, spravuje, Povolen FROM Kurz LIMIT 100');
        return $stmt;
	}
	
	function getCourse($zkratka)
	{
		$stmt = $this->pdo->prepare('SELECT zkratka, Nazev, popis, typ, tag1, tag2, tag3, cena, Povolen, spravuje FROM Kurz WHERE zkratka = ?');
        $stmt->execute([$zkratka]);
        return $stmt->fetch();
	}
    
	function deleteCourse($zkratka)
    {
        $stmt = $this->pdo->prepare('DELETE FROM Kurz WHERE zkratka = ?');
        if ($stmt->execute([$zkratka]))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	/****************
	ROOMS
	*****************/
	function getRooms()
	{
		$stmt = $this->pdo->query('SELECT nazev, typ, kapacita FROM Mistnost LIMIT 100');
        return $stmt;
	}
    function getRoom($nazev)
	{
        $stmt = $this->pdo->prepare("SELECT nazev, typ, kapacita FROM Mistnost WHERE nazev = ?");
        $stmt->execute([$nazev]);
        return $stmt->fetch();
    }
	
	function updateRoom($data)
    {
        $stmt = $this->pdo->prepare('UPDATE Mistnost SET nazev = :nazev, typ = :typ, kapacita = :kapacita WHERE nazev = :orig_nazev');
        if ($stmt->execute($data))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	function addRoom($data)
    {
        $stmt = $this->pdo->prepare('INSERT INTO Mistnost (nazev, typ, kapacita) VALUES (?, ?, ?)');
        if ($stmt->execute([$data['nazev'], $data['typ'], $data['kapacita']]))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	function deleteRoom($nazev)
    {
        $stmt = $this->pdo->prepare('DELETE FROM Mistnost WHERE nazev = ?');
        if ($stmt->execute([$nazev]))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	/****************
	TERMS
	*****************/
	function getTerms($kurz)
	{
		$stmt = $this->pdo->prepare('SELECT id, nazev, typ, popis, datum, zacatek, konec, lektor, mistnost FROM Termin WHERE kurz = ?');
        if ($stmt->execute([$kurz])) {
			return $stmt;
		}
		else
        {	
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        } 
	}
	
	function getTerm($id)
	{
		$stmt = $this->pdo->prepare('SELECT id, nazev, typ, popis, datum, zacatek, konec, lektor, mistnost FROM Termin WHERE id = ?');
        $stmt->execute([$id]);
        return $stmt->fetch();
	}
	
	function addTerm($data)
    {
        $stmt = $this->pdo->prepare('INSERT INTO Termin (nazev, typ, popis, datum, zacatek, konec, lektor, kurz, mistnost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
        if ($stmt->execute([$data['nazev'], $data['typ'], $data['popis'], $data['datum'], $data['zacatek'], $data['konec'], $data['lektor'], $data['kurz'], $data['mistnost']]))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	function updateTerm($data)
    {
        $stmt = $this->pdo->prepare('UPDATE Termin SET nazev = :nazev, typ = :typ, popis = :popis, datum = :datum, zacatek = :zacatek, konec = :konec, lektor = :lektor, mistnost = :mistnost WHERE id = :id');
        if ($stmt->execute($data))
        {
            return $data;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }

    function deleteTerm($id)
    {
        $stmt = $this->pdo->prepare('DELETE FROM Termin WHERE id = ?');
        if ($stmt->execute([$id]))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	/****************
	REGISTRATION, APPROVING
	*****************/
	function registerStudent($login, $kurz)
	{
		$stmt = $this->pdo->prepare('INSERT INTO Student_Kurz(login, kurz, schvalen) VALUES (?, ?, ?)');
        if ($stmt->execute([$login, $kurz, 0]))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
    
	function checkIfStudentApproved($login, $kurz) {
		$stmt = $this->pdo->prepare('SELECT * FROM Student_Kurz WHERE login = ? AND kurz = ? AND schvalen = 1');
        if ($stmt->execute([$login, $kurz])) {
			return $stmt->fetch();
		} 
		else
		{
			$this->lastError = $stmt->errorInfo();
			return FALSE;
		}
    }
    
	function checkRegistration($login, $kurz) {
		$stmt = $this->pdo->prepare('SELECT login, kurz, schvalen FROM Student_Kurz WHERE login = ? AND kurz = ?');
        if ($stmt->execute([$login, $kurz])) {
			return $stmt->fetch();
		} 
		else
		{
			$this->lastError = $stmt->errorInfo();
			return FALSE;
		}
    }

	function unregisterStudent($login, $kurz){
        $stmt = $this->pdo->prepare('DELETE FROM Student_Kurz WHERE login = ? AND kurz = ?');
        if ($stmt->execute([$login, $kurz]))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
	}
	
    function getUserCourses($login) {
		$stmt = $this->pdo->prepare('SELECT kurz, schvalen FROM Student_Kurz WHERE login = ?');
        if ($stmt->execute([$login])) {
			return $stmt;
		} 
		else
		{
			$this->lastError = $stmt->errorInfo();
			return FALSE;
		}
    }
    function getLoginInCourses($kurz) {
		$stmt = $this->pdo->prepare('SELECT login FROM Student_Kurz WHERE kurz = ?');
        if ($stmt->execute([$kurz])) {
			return $stmt;
		} 
		else
		{
			$this->lastError = $stmt->errorInfo();
			return FALSE;
		}
    }
    
    function updateUser($data) {
		$stmt = $this->pdo->prepare("UPDATE Uzivatel SET login = :login, jmeno = :jmeno, prijmeni = :prijmeni, datum_narozeni = :datum_narozeni, typ = :typ  WHERE  login= :login");
        if ($stmt->execute($data)) {
			return TRUE;
		} 
		else
		{
			$this->lastError = $stmt->errorInfo();
			return FALSE;
		}
    }
    
    function getAssessment($login, $kurz)
    {
        $stmt = $this->pdo->prepare('SELECT hodnoceni FROM Student_Kurz WHERE login = ? AND kurz = ?');
        if ($stmt->execute([$login, $kurz]))
        {
            return $stmt->fetch();
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }


    }

    function updateAssessment($data)
    {
        $stmt = $this->pdo->prepare('UPDATE Student_Kurz SET hodnoceni = :hodnoceni WHERE login = :login AND kurz = :kurz');
        if ($stmt->execute($data))
        {
            return TRUE;
        }
        else
        {
            $this->lastError = $stmt->errorInfo();
            return FALSE;
        }
    }
	
	/****************
	*****************/
	function getTimeTable($student){
        $stmt = $this->pdo->prepare('SELECT * FROM Termin NATURAL JOIN Student_Kurz WHERE Termin.kurz = Student_Kurz.kurz AND Student_Kurz.schvalen = 1 
                                              AND Student_Kurz.login = ? ORDER BY datum ASC');
        if ($stmt->execute([$student]))
            return $stmt;
        return $stmt;
	}
}
?>
