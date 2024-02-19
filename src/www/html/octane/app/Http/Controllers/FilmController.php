<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller as BaseController;
use App\Models\Film;

class FilmController extends BaseController
{
    public function index()
    {
        $films = Film::all();
        return response()->json($films);
    }
}
