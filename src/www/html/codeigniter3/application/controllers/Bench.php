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

    public function api()
    {
        $this->load->database();
        $this->load->model('film_model');
        return $this->output->set_status_header(200)
            ->set_content_type('application/json')
            ->set_output(json_encode($this->film_model->findAll()));
    }
}