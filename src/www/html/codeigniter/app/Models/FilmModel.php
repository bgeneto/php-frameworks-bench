<?php 

namespace App\Models;

use CodeIgniter\Model;

class FilmModel extends Model
{
    protected $table = 'films';
    protected $primaryKey = 'film_id';
    protected $allowedFields = ['title', 'description', 'release_year', 'rental_duration', 'rental_rate', 'length', 'replacement_cost', 'rating', 'special_features', 'last_update'];
}