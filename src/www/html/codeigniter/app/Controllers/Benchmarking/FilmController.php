<?php

namespace App\Controllers\Benchmarking;

use CodeIgniter\RESTful\ResourceController;
use App\Models\FilmModel;

class FilmController extends ResourceController
{
    protected $modelName = FilmModel::class;
    protected $format = 'json';

    public function index()
    {
        $data = $this->model->findAll();
        return $this->respond($data);
    }
}