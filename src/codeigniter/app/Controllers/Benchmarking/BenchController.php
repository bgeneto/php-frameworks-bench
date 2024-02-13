<?php

namespace App\Controllers\Benchmarking;

use  App\Controllers\BaseController;

class BenchController extends BaseController
{
	public function hello(): string
	{
		return view('benchmarking/hello', ['title' => 'Hello', 'output' => 'Hello, World!!!']);
	}

	public function info(): string
	{
		return phpinfo();
	}
}

