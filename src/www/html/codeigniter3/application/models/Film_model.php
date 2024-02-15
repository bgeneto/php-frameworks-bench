<?php

defined('BASEPATH') OR exit('No direct script access allowed');

class Film_model extends CI_Model
{
    public function findAll(){
        $query = $this->db->get('films');    
        return $query->result_array();
    }
}