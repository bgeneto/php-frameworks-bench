<?php

// Define path to page views

define('ROOT_PATH', dirname(__DIR__) . '/');
define('PAGE_DIR', ROOT_PATH . 'views/');

// Define available pages
$pages = [
	'api',
	'benchmarking/info',
	'benchmarking/hello',
	'home'
];

// Get requested URI
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Remove leading slash
$uri = ltrim($uri, '/');

// Check if requested page exists
if (in_array($uri, $pages)) {
	// Load requested page based on URI and current directory
	$page = PAGE_DIR . $uri . '.php';
	if (file_exists($page)) {
		include $page;
		exit;
	}
} else {
	if (empty($uri)) {
		// Load the home page
		include PAGE_DIR . 'home.php';
		exit;
	}
}

// Handle not found page
include PAGE_DIR . '404.php';
