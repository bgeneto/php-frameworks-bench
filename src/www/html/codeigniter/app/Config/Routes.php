<?php

use CodeIgniter\Router\RouteCollection;

/**
 * @var RouteCollection $routes
 */
$routes->get('/', 'Home::index');

$routes->get('/benchmarking/info', 'BenchController::info', ['namespace' => 'App\Controllers\Benchmarking']);
$routes->get('/benchmarking/hello', 'BenchController::hello', ['namespace' => 'App\Controllers\Benchmarking']);
$routes->get('benchmarking/api', 'FilmController::index', ['namespace' => 'App\Controllers\Benchmarking']);