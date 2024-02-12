#!/usr/bin/sh

composer create-project codeigniter4/appstarter codeigniter
composer create-project symfony/skeleton:"7.0.*" symfony
cd symfony
composer require twig
cd ..
composer create-project laravel/laravel:"11.x-dev" laravel
 
