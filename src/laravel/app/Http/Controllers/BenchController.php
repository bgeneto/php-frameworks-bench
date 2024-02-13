<?php

namespace App\Http\Controllers;

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;

class BenchController extends BaseController
{
	public function info()
	{
		return view('info');
	}

	public function hello()
	{
		return view('hello', ['title' => 'Hello', 'body' => 'Hello, World!!!']);
	}
}
