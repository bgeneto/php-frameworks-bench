<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Bench extends CI_Controller {

    public function hello()
    {
        $data = ['title' => 'Hello', 'output' => 'Hello, World!!!'];
        $this->load->view('templates/header', $data);
        $this->load->view('hello', $data);
        $this->load->view('templates/footer');
    }

    public function info()
    {
        phpinfo();
    }
}