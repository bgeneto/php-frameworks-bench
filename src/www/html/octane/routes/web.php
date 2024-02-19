<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\BenchController;
use App\Http\Controllers\FilmController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/benchmarking/info', function () {
    return view('info');
});

Route::get('/benchmarking/hello', [BenchController::class, 'hello']);

Route::get('/benchmarking/api', [FilmController::class, 'index']);