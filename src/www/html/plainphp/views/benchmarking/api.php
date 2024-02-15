<?php 

$host = 'mariadb';
$dbname = 'bench';
$username = 'bench';
$password = 'bench';

try {
    // Connect to the database
    $dsn = "mysql:host=$host;dbname=$dbname;charset=utf8mb4";
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ];
    $pdo = new PDO($dsn, $username, $password, $options);

    // Retrieve all rows from a table
    $stmt = $pdo->query('SELECT * FROM films');
    $rows = $stmt->fetchAll();

    // Echo the rows as application/json
    header('Content-Type: application/json');
    echo json_encode($rows);
} catch (PDOException $e) {
    die('Connection failed: ' . $e->getMessage());
}
